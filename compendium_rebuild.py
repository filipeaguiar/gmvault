#!/usr/bin/env python3
"""Rebuild the referenced compendium from 5e.tools in a validated staging area."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import unicodedata
import urllib.request
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

from dnd_utils import clean_5etools_tags, extract_spell_mechanics, parse_entries

PROJECT_ROOT = Path(__file__).resolve().parent
CONTENT_ROOT = PROJECT_ROOT / "content"
CAMPAIGN_ROOT = CONTENT_ROOT / "campaigns"
COMPENDIUM_ROOT = CONTENT_ROOT / "compendium"
DEFAULT_MANIFEST = PROJECT_ROOT / "compendium_manifest.json"
DEFAULT_STAGING = PROJECT_ROOT / ".compendium-staging" / "compendium"
DEFAULT_CACHE = PROJECT_ROOT / ".cache" / "5etools"
DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"
REFERENCE_RE = re.compile(r"/compendium/[a-z0-9-]+/[a-z0-9-]+/")
SOURCE_TAG_RE = re.compile(r"\{@(creature|monster|item)\s+([^}]+)\}", re.IGNORECASE)
UNRESOLVED_TAG_RE = re.compile(r"\{@[a-zA-Z]+\s")

ACTION_ALIASES = {
    "action-attack": "Attack",
    "action-dash": "Dash",
    "action-disengage": "Disengage",
    "action-dodge": "Dodge",
    "action-help": "Help",
    "action-hide": "Hide",
    "action-use-object": "Use an Object",
}
RULE_ALIASES = {
    "otherworldly-patron": "Warlock Subclass",
}
CATEGORY_KIND = {
    "classes": "class",
    "feats": "feat",
    "items": "item",
    "magic-items": "magic_item",
    "monsters": "monster",
    "rules": "rule",
    "species": "species",
    "spells": "spell",
}
TYPE_KEYS = {
    "monster": ("monster",),
    "spell": ("spell",),
    "item": ("item", "baseitem"),
    "magic_item": ("item", "baseitem"),
    "feat": ("feat",),
    "species": ("race",),
    "class": ("class", "subclass"),
    "rule": ("action", "classFeature", "subclassFeature", "optionalfeature"),
}
TYPE_FILES = {
    "item": ("items.json", "items-base.json"),
    "magic_item": ("items.json", "items-base.json"),
    "feat": ("feats.json",),
    "species": ("races.json",),
    "rule": ("actions.json", "optionalfeatures.json"),
}


class RebuildError(RuntimeError):
    pass


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    front_matter_raw, body = match.groups()
    try:
        metadata = yaml.safe_load(front_matter_raw) or {}
    except yaml.YAMLError as exc:
        raise RebuildError(f"YAML inválido em {path}: {exc}") from exc
    if not isinstance(metadata, dict):
        raise RebuildError(f"Front matter não é objeto em {path}")
    return metadata, body


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child)


def extract_references(path: Path) -> set[str]:
    metadata, body = parse_markdown(path)
    refs = set(REFERENCE_RE.findall(body))
    for value in iter_strings(metadata):
        refs.update(REFERENCE_RE.findall(value))
    return refs


def entity_url(path: Path, root: Path | None = None) -> str | None:
    root = root or COMPENDIUM_ROOT
    if path.name == "_index.md":
        return None
    rel = path.relative_to(root).with_suffix("")
    return f"/compendium/{rel.as_posix()}/"


def compendium_pages(root: Path | None = None) -> dict[str, Path]:
    root = root or COMPENDIUM_ROOT
    result: dict[str, Path] = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*.md")):
        url = entity_url(path, root)
        if url:
            result[url] = path
    return result


def hash_paths(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        digest.update(path.relative_to(PROJECT_ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def input_paths() -> list[Path]:
    return sorted(CAMPAIGN_ROOT.rglob("*.md")) + sorted(COMPENDIUM_ROOT.rglob("*.md"))


def scan_inventory() -> dict[str, Any]:
    pages = compendium_pages()
    direct_origins: dict[str, set[str]] = defaultdict(set)
    campaign_paths = sorted(CAMPAIGN_ROOT.rglob("*.md"))
    for path in campaign_paths:
        origin = "character" if "/characters/" in path.as_posix() else "campaign"
        for ref in extract_references(path):
            direct_origins[ref].add(origin)

    selected = set(direct_origins)
    dependency_origins: dict[str, set[str]] = defaultdict(set)
    queue = deque(sorted(selected))
    while queue:
        parent = queue.popleft()
        page = pages.get(parent)
        if not page:
            continue
        for ref in extract_references(page):
            dependency_origins[ref].add(parent)
            if ref not in selected:
                selected.add(ref)
                queue.append(ref)

    entries = []
    for ref in sorted(selected):
        parts = ref.strip("/").split("/")
        category, slug = parts[1], parts[2]
        path = pages.get(ref)
        metadata = parse_markdown(path)[0] if path else {}
        kind = CATEGORY_KIND.get(category, category.rstrip("s"))
        name = metadata.get("title") or slug.replace("-", " ").title()
        if category == "rules":
            name = ACTION_ALIASES.get(slug, RULE_ALIASES.get(slug, name))
        entries.append(
            {
                "url": ref,
                "category": category,
                "kind": kind,
                "slug": slug,
                "canonical_name": name,
                "direct_origins": sorted(direct_origins.get(ref, set())),
                "dependency_origins": sorted(dependency_origins.get(ref, set())),
                "selected_source": None,
                "remote_file": None,
                "remote_key": None,
                "selection_reason": None,
                "status": "unresolved",
                "error": None,
            }
        )

    missing = sorted(ref for ref in selected if ref not in pages)
    unused = sorted(set(pages) - selected)
    return {
        "schema_version": 1,
        "provider": "5e.tools",
        "data_base_url": DATA_BASE_URL,
        "input_fingerprint": hash_paths(input_paths()),
        "counts": {
            "direct": len(direct_origins),
            "transitive_dependencies": len(selected - set(direct_origins)),
            "selected": len(selected),
            "unused": len(unused),
            "total_entities": len(pages),
        },
        "selected": entries,
        "unused": unused,
        "missing_local": missing,
    }


@dataclass(frozen=True)
class CatalogRecord:
    kind: str
    name: str
    source: str
    remote_file: str
    remote_key: str
    data: dict[str, Any]
    remote_id: str = ""


def record_remote_id(remote_key: str, entity: dict[str, Any]) -> str:
    identity = {
        "key": remote_key,
        "name": entity.get("name"),
        "source": entity.get("source"),
        "className": entity.get("className"),
        "classSource": entity.get("classSource"),
        "level": entity.get("level"),
        "raceName": entity.get("raceName"),
    }
    return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:16]


class FiveEToolsCatalog:
    def __init__(self, cache_dir: Path = DEFAULT_CACHE, base_url: str = DATA_BASE_URL):
        self.cache_dir = cache_dir
        self.base_url = base_url.rstrip("/") + "/"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._json: dict[str, Any] = {}
        self._records: dict[str, list[CatalogRecord]] = {}

    def get_json(self, remote_file: str) -> Any:
        if remote_file in self._json:
            return self._json[remote_file]
        cache = self.cache_dir / remote_file
        if not cache.exists():
            cache.parent.mkdir(parents=True, exist_ok=True)
            request = urllib.request.Request(self.base_url + remote_file, headers={"User-Agent": "gmvault-compendium-rebuild"})
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    payload = response.read()
            except Exception as exc:
                raise RebuildError(f"Falha ao baixar {remote_file}: {exc}") from exc
            temporary = cache.with_suffix(cache.suffix + ".tmp")
            temporary.write_bytes(payload)
            temporary.replace(cache)
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RebuildError(f"Cache JSON inválido para {remote_file}: {exc}") from exc
        self._json[remote_file] = data
        return data

    def files_for_kind(self, kind: str) -> list[str]:
        if kind == "monster":
            index = self.get_json("bestiary/index.json")
            return [f"bestiary/{name}" for name in index.values()]
        if kind == "spell":
            index = self.get_json("spells/index.json")
            return [f"spells/{name}" for name in index.values()]
        if kind == "class":
            index = self.get_json("class/index.json")
            return [f"class/{name}" for name in index.values()]
        if kind == "rule":
            index = self.get_json("class/index.json")
            return ["actions.json", "optionalfeatures.json", *[f"class/{name}" for name in index.values()]]
        return list(TYPE_FILES.get(kind, ()))

    def records(self, kind: str) -> list[CatalogRecord]:
        if kind in self._records:
            return self._records[kind]
        records: list[CatalogRecord] = []
        for remote_file in self.files_for_kind(kind):
            data = self.get_json(remote_file)
            for key in TYPE_KEYS[kind]:
                for entity in data.get(key, []) or []:
                    name = str(entity.get("name") or "").strip()
                    if not name:
                        continue
                    records.append(
                        CatalogRecord(
                            kind=kind,
                            name=name,
                            source=str(entity.get("source") or "").upper(),
                            remote_file=remote_file,
                            remote_key=key,
                            data=entity,
                            remote_id=record_remote_id(key, entity),
                        )
                    )
        self._records[kind] = records
        return records

    def jttrc_sources(self) -> dict[tuple[str, str], str]:
        data = self.get_json("adventure/adventure-jttrc.json")
        text = json.dumps(data, ensure_ascii=False)
        result: dict[tuple[str, str], str] = {}
        for tag, inner in SOURCE_TAG_RE.findall(text):
            parts = inner.split("|")
            name = parts[0].strip()
            kind = "item" if tag.lower() == "item" else "monster"
            default = "PHB" if kind == "item" else "MM"
            source = parts[1].strip().upper() if len(parts) > 1 and parts[1].strip() else default
            result[(kind, slugify(name))] = source
        return result


def normalized_source(source: str) -> str:
    return source.replace("-", "").upper()


def choose_record(entry: dict[str, Any], records: list[CatalogRecord], jttrc: dict[tuple[str, str], str]) -> tuple[CatalogRecord | None, str | None, str | None]:
    kind = entry["kind"]
    name = str(entry["canonical_name"])
    slug = entry["slug"]
    exact = [record for record in records if record.name.casefold() == name.casefold()]
    if not exact:
        exact = [record for record in records if slugify(record.name) == slug]
    if not exact and kind == "rule" and slug in RULE_ALIASES:
        alias = RULE_ALIASES[slug]
        exact = [record for record in records if record.name.casefold() == alias.casefold()]
    if not exact:
        return None, None, f"Entidade não encontrada no 5e.tools: {kind} {name!r} ({slug})"

    explicit = entry.get("explicit_source")
    if not explicit and "campaign" in entry.get("direct_origins", []):
        source_kind = "item" if kind == "magic_item" else kind
        explicit = jttrc.get((source_kind, slug))
    if explicit:
        matching = [record for record in exact if normalized_source(record.source) == normalized_source(explicit)]
        if matching:
            reason = f"fonte explícita: {explicit}" if entry.get("explicit_source") else f"fonte explícita de JttRC: {explicit}"
            return matching[0], reason, None
        return None, None, f"Fonte explícita {explicit} não encontrada para {name}"

    source_order = ["XPHB", "PHB"]
    if kind == "species" and slug == "goblin":
        source_order += ["MPMM", "VGM"]
    for source in source_order:
        matching = [record for record in exact if normalized_source(record.source) == source]
        if matching:
            return matching[0], f"prioridade de fonte: {source}", None
    if len(exact) == 1:
        return exact[0], f"única fonte disponível: {exact[0].source}", None
    sources = sorted({record.source for record in exact})
    return None, None, f"Fontes ambíguas sem política para {name}: {', '.join(sources)}"


def resolve_manifest(manifest: dict[str, Any], catalog: FiveEToolsCatalog) -> dict[str, Any]:
    jttrc = catalog.jttrc_sources()
    for entry in manifest["selected"]:
        records = catalog.records(entry["kind"])
        record, reason, error = choose_record(entry, records, jttrc)
        if not record:
            entry.update(status="error", error=error, selection_reason=None)
            continue
        entry.update(
            selected_source=record.source,
            remote_file=record.remote_file,
            remote_key=record.remote_key,
            remote_id=record.remote_id,
            selection_reason=reason,
            status="resolved",
            error=None,
        )
        entry["canonical_name"] = record.name
    manifest["resolution"] = dict(Counter(item["status"] for item in manifest["selected"]))
    return manifest


def get_record(entry: dict[str, Any], catalog: FiveEToolsCatalog) -> CatalogRecord:
    matches = [
        record
        for record in catalog.records(entry["kind"])
        if record.remote_file == entry["remote_file"]
        and record.remote_key == entry["remote_key"]
        and record.source == entry["selected_source"]
        and record.name == entry["canonical_name"]
        and (not entry.get("remote_id") or record.remote_id == entry["remote_id"])
    ]
    if len(matches) != 1:
        raise RebuildError(f"Registro remoto não é único para {entry['url']}")
    return matches[0]


def source_metadata(record: CatalogRecord) -> dict[str, Any]:
    return {
        "provider": "5e.tools",
        "book": record.source,
        "entity_type": record.kind,
        "entity_name": record.name,
        "remote_file": record.remote_file,
        "remote_key": record.remote_key,
        "remote_id": record.remote_id,
    }


def format_time(entity: dict[str, Any]) -> str:
    times = entity.get("time") or []
    if not times:
        return ""
    first = times[0]
    unit = {"bonus": "bonus action", "reaction": "reaction"}.get(first.get("unit"), first.get("unit", "action"))
    return f"{first.get('number', 1)} {unit}"


def format_range(entity: dict[str, Any]) -> str:
    data = entity.get("range") or {}
    distance = data.get("distance") or {}
    kind = distance.get("type")
    if kind in {"self", "touch", "sight", "unlimited", "plane", "special"}:
        return str(kind).title()
    amount = distance.get("amount")
    return f"{amount} {kind}" if amount is not None and kind else str(kind or "")


def format_components(entity: dict[str, Any]) -> str:
    components = entity.get("components") or {}
    values = []
    for key in ("v", "s", "m", "r"):
        value = components.get(key)
        if not value:
            continue
        if key == "m":
            material = value.get("text", "") if isinstance(value, dict) else str(value)
            values.append(f"M ({material})" if material else "M")
        else:
            values.append(key.upper())
    return ", ".join(values)


def format_duration(entity: dict[str, Any]) -> str:
    durations = entity.get("duration") or []
    if not durations:
        return ""
    duration = durations[0]
    kind = duration.get("type", "")
    if kind == "instant":
        return "Instantaneous"
    if kind == "permanent":
        return "Until dispelled"
    amount = duration.get("duration") or {}
    text = f"{amount.get('amount', '')} {amount.get('type', '')}".strip()
    if duration.get("concentration"):
        text = f"Concentration, up to {text}"
    return text or str(kind).title()


def render_body_entries(entity: dict[str, Any]) -> str:
    chunks = []
    if entity.get("entries"):
        chunks.append(parse_entries(entity["entries"]))
    if entity.get("entriesHigherLevel"):
        chunks.append("## At Higher Levels\n\n" + parse_entries(entity["entriesHigherLevel"]))
    return clean_5etools_tags("\n\n".join(filter(None, chunks))).strip()


def monster_stats(entity: dict[str, Any]) -> tuple[dict[str, Any], str]:
    size_map = {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}
    sizes = entity.get("size") or []
    creature_type = entity.get("type") or ""
    if isinstance(creature_type, dict):
        creature_type = creature_type.get("type", "")
    alignment = entity.get("alignment") or []
    stats_meta = " ".join(filter(None, [size_map.get(sizes[0], str(sizes[0])) if sizes else "", str(creature_type), "/".join(map(str, alignment))]))
    ac_data = entity.get("ac") or []
    ac = ac_data[0] if ac_data else ""
    if isinstance(ac, dict):
        ac = ac.get("ac", "")
    hp_data = entity.get("hp") or {}
    hp = hp_data.get("average", "")
    if hp_data.get("formula"):
        hp = f"{hp} ({hp_data['formula']})" if hp else hp_data["formula"]
    speed_data = entity.get("speed") or {}
    speed = ", ".join(f"{key} {value if not isinstance(value, dict) else value.get('number', '')} ft." for key, value in speed_data.items() if key != "canHover")
    attributes = {key: entity.get(key) for key in ("str", "dex", "con", "int", "wis", "cha") if entity.get(key) is not None}
    stats = {
        "ac": str(ac), "hp": str(hp), "speed": speed, "attributes": attributes,
        "saves": entity.get("save") or {}, "skills": entity.get("skill") or {},
        "senses": ", ".join(entity.get("senses") or []),
        "languages": ", ".join(entity.get("languages") or []),
        "cr": (entity.get("cr") or {}).get("cr") if isinstance(entity.get("cr"), dict) else entity.get("cr", ""),
    }
    return stats, stats_meta.strip()


def item_info(entity: dict[str, Any]) -> dict[str, Any]:
    raw_type = str(entity.get("type") or entity.get("typeAlt") or "")
    type_code = raw_type.split("|", 1)[0]
    type_map = {
        "M": "Weapon", "R": "Weapon", "LA": "Armor", "MA": "Armor", "HA": "Armor",
        "S": "Shield", "P": "Potion", "SC": "Scroll", "RG": "Ring", "WD": "Wand",
        "RD": "Rod", "ST": "Staff",
    }
    item_type = "Wondrous item" if entity.get("wondrous") else type_map.get(type_code, "Adventuring Gear")
    prop_map = {
        "F": "finesse", "L": "light", "T": "thrown", "V": "versatile", "H": "heavy",
        "2H": "two-handed", "R": "reach", "A": "ammunition", "LD": "loading",
        "RL": "reload", "S": "special", "BF": "burst fire",
    }
    damage_map = {
        "P": "piercing", "S": "slashing", "B": "bludgeoning", "F": "fire", "C": "cold",
        "L": "lightning", "A": "acid", "O": "force", "R": "radiant", "N": "necrotic",
        "T": "thunder", "I": "poison", "Y": "psychic",
    }
    properties = [prop_map.get(str(value).split("|", 1)[0], str(value).split("|", 1)[0].lower()) for value in entity.get("property") or []]
    modifiers: dict[str, Any] = {}
    ability = entity.get("ability") or {}
    if isinstance(ability, dict) and isinstance(ability.get("static"), dict):
        modifiers["stat_override"] = {key: value for key, value in ability["static"].items() if key in {"str", "dex", "con", "int", "wis", "cha"}}
    for source_key, target_key in (("bonusAc", "ac_bonus"), ("bonusArmorClass", "ac_bonus"), ("bonusSavingThrow", "save_bonus")):
        if entity.get(source_key) is not None:
            try:
                modifiers[target_key] = int(str(entity[source_key]).replace("+", "").strip())
            except ValueError:
                pass
    value = entity.get("value")
    info: dict[str, Any] = {
        "type": item_type,
        "cost": f"{value / 100:g} gp" if value else "—",
        "weight": f"{entity['weight']} lb" if entity.get("weight") else "—",
    }
    if entity.get("rarity"):
        info["rarity"] = str(entity["rarity"]).title()
    if entity.get("reqAttune"):
        info["attunement"] = "Requires attunement"
    if item_type == "Weapon":
        info["weapon_type"] = "ranged" if type_code == "R" else "melee"
    if type_code in {"P", "SC"} or entity.get("consumable"):
        info["consumable"] = True
    if properties:
        info["properties"] = properties
    for source_key, target_key in (("range", "range"), ("dmg1", "damage"), ("ac", "armor_class")):
        if entity.get(source_key) is not None:
            info[target_key] = entity[source_key]
    if entity.get("dmgType"):
        info["damage_type"] = damage_map.get(entity["dmgType"], entity["dmgType"])
    if modifiers:
        info["modifiers"] = modifiers
    return info


def class_info(entity: dict[str, Any]) -> dict[str, Any]:
    hd = entity.get("hd") or {}
    primary = entity.get("primaryAbility") or []
    return {
        "hit_dice": f"{hd.get('number', 1)}d{hd.get('faces', '')}" if hd else "",
        "primary_ability": ", ".join(str(item) for item in primary),
    }


def species_info(entity: dict[str, Any]) -> dict[str, Any]:
    speed = entity.get("speed")
    if isinstance(speed, dict):
        speed = speed.get("walk") or speed
    return {
        "ability_score": entity.get("ability") or [],
        "speed": speed or "",
        "languages": entity.get("languageProficiencies") or [],
        "size": entity.get("size") or [],
    }


def render_class_body(record: CatalogRecord, catalog: FiveEToolsCatalog, selected_urls: set[str]) -> str:
    data = catalog.get_json(record.remote_file)
    features = [item for item in data.get("classFeature", []) if item.get("className") == record.name and str(item.get("source", "")).upper() == record.source]
    by_level: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for feature in features:
        by_level[int(feature.get("level", 0))].append(feature)
    lines = []
    for level in sorted(by_level):
        lines.append(f"## Level {level}\n")
        for feature in by_level[level]:
            feature_slug = slugify(feature.get("name", ""))
            aliases = {"warlock-subclass": "otherworldly-patron"}
            target_slug = aliases.get(feature_slug, feature_slug)
            url = f"/compendium/rules/{target_slug}/"
            name = feature.get("name", "Feature")
            lines.append(f"- [{name}]({url})" if url in selected_urls else f"- {name}")
        lines.append("")
    return "\n".join(lines).strip()


def build_document(entry: dict[str, Any], record: CatalogRecord, catalog: FiveEToolsCatalog, selected_urls: set[str]) -> str:
    kind = entry["kind"]
    entity = record.data
    visibility = "gm" if kind in {"monster", "magic_item"} and "campaign" in entry.get("direct_origins", []) else "public"
    metadata: dict[str, Any] = {
        "title": record.name,
        "type": kind,
        "draft": False,
        "weight": 10,
        "tags": ["draft", "importado", "5etools"],
        "visibility": visibility,
        "status": "draft",
        "source": source_metadata(record),
    }
    body = render_body_entries(entity)
    if kind == "spell":
        schools = {"A": "Abjuration", "C": "Conjuration", "D": "Divination", "E": "Enchantment", "V": "Evocation", "I": "Illusion", "N": "Necromancy", "T": "Transmutation"}
        level = int(entity.get("level", 0))
        metadata["spell_info"] = {
            "level": "Cantrip" if level == 0 else f"{level}{'st' if level == 1 else 'nd' if level == 2 else 'rd' if level == 3 else 'th'} level",
            "school": schools.get(entity.get("school"), entity.get("school", "")),
            "cast_time": format_time(entity), "range": format_range(entity),
            "components": format_components(entity), "duration": format_duration(entity),
            **extract_spell_mechanics(entity),
        }
    elif kind == "monster":
        metadata["stats"], metadata["stats_meta"] = monster_stats(entity)
        sections = []
        for key, heading in (("trait", "Traits"), ("action", "Actions"), ("bonus", "Bonus Actions"), ("reaction", "Reactions"), ("legendary", "Legendary Actions")):
            values = entity.get(key) or []
            if values:
                sections.append(f"## {heading}\n\n{parse_entries(values)}")
        body = clean_5etools_tags("\n\n".join(filter(None, [body, *sections]))).strip()
    elif kind in {"item", "magic_item"}:
        metadata["item_info"] = item_info(entity)
    elif kind == "class":
        metadata["class_info"] = class_info(entity)
        body = render_class_body(record, catalog, selected_urls)
    elif kind == "species":
        metadata["species_info"] = species_info(entity)
        metadata["race_info"] = metadata["species_info"]
    elif kind == "feat":
        metadata["feat_info"] = {"prerequisite": entity.get("prerequisite") or []}
    elif kind == "rule":
        body = render_body_entries(entity)
    rendered = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=120)
    return f"---\n{rendered}---\n\n{body.strip()}\n"


def sync_compendium_entity(
    kind: str,
    name: str,
    *,
    slug: str | None = None,
    source: str | None = None,
    output_root: Path | None = None,
    origin: str = "character",
    catalog: FiveEToolsCatalog | None = None,
) -> str | None:
    """Resolve and write one entity with the same serializer used by rebuild."""
    catalog = catalog or FiveEToolsCatalog()
    output_root = output_root or (Path.cwd() / "content" / "compendium")
    slug = slug or slugify(name)
    category = {
        "monster": "monsters", "magic_item": "magic-items", "item": "items",
        "class": "classes", "species": "species", "race": "species",
        "feat": "feats", "spell": "spells", "rule": "rules",
    }.get(kind)
    normalized_kind = "species" if kind == "race" else kind
    if not category:
        return None
    entry = {
        "url": f"/compendium/{category}/{slug}/", "category": category,
        "kind": normalized_kind, "slug": slug, "canonical_name": name,
        "direct_origins": [origin], "dependency_origins": [],
        "explicit_source": source,
    }
    record, _reason, error = choose_record(entry, catalog.records(normalized_kind), catalog.jttrc_sources())
    if error or not record:
        return None
    destination = output_root / category / f"{slug}.md"
    previous = parse_markdown(destination) if destination.exists() else None
    destination.parent.mkdir(parents=True, exist_ok=True)
    selected_urls = {entry["url"]}
    rendered = build_document(entry, record, catalog, selected_urls)
    if previous:
        generated_path = destination.with_suffix(".generated.tmp")
        generated_path.write_text(rendered, encoding="utf-8")
        generated_metadata, generated_body = parse_markdown(generated_path)
        generated_path.unlink()
        previous_metadata, previous_body = previous
        translation = previous_metadata.get("translation") or {}
        preserve_editorial = bool(translation) and bool(previous_body.strip())
        if preserve_editorial:
            generated_body = previous_body
            generated_metadata["translation"] = translation
            for key in ("titulo_pt_br",):
                if previous_metadata.get(key):
                    generated_metadata[key] = previous_metadata[key]
        if preserve_editorial:
            rendered = f"---\n{yaml.safe_dump(generated_metadata, allow_unicode=True, sort_keys=False, width=120)}---{generated_body}"
        else:
            rendered = f"---\n{yaml.safe_dump(generated_metadata, allow_unicode=True, sort_keys=False, width=120)}---\n\n{generated_body.strip()}\n"
    temporary = destination.with_suffix(".md.tmp")
    temporary.write_text(rendered, encoding="utf-8")
    temporary.replace(destination)
    return entry["url"]


def generate_staging(manifest: dict[str, Any], catalog: FiveEToolsCatalog, staging: Path = DEFAULT_STAGING) -> None:
    errors = [item for item in manifest["selected"] if item["status"] != "resolved"]
    if errors:
        raise RebuildError(f"Manifesto possui {len(errors)} entidades não resolvidas")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    source_index = COMPENDIUM_ROOT / "_index.md"
    if source_index.exists():
        shutil.copy2(source_index, staging / "_index.md")
    selected_urls = {item["url"] for item in manifest["selected"]}
    for entry in manifest["selected"]:
        record = get_record(entry, catalog)
        destination = staging / entry["category"] / f"{entry['slug']}.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(build_document(entry, record, catalog, selected_urls), encoding="utf-8")


def validate_staging(manifest: dict[str, Any], staging: Path = DEFAULT_STAGING) -> list[str]:
    errors: list[str] = []
    selected_urls = {item["url"] for item in manifest["selected"]}
    expected = {item["url"]: item for item in manifest["selected"]}
    staged = compendium_pages(staging)
    if set(staged) != selected_urls:
        for ref in sorted(selected_urls - set(staged)):
            errors.append(f"Página ausente no staging: {ref}")
        for ref in sorted(set(staged) - selected_urls):
            errors.append(f"Página extra no staging: {ref}")
    required_blocks = {"spell": "spell_info", "monster": "stats", "item": "item_info", "magic_item": "item_info", "class": "class_info", "species": "species_info", "feat": "feat_info"}
    for ref, path in staged.items():
        try:
            metadata, body = parse_markdown(path)
        except RebuildError as exc:
            errors.append(str(exc)); continue
        entry = expected[ref]
        if metadata.get("source", {}).get("provider") != "5e.tools":
            errors.append(f"Proveniência inválida: {ref}")
        block = required_blocks.get(entry["kind"])
        if block and block not in metadata:
            errors.append(f"Campo {block} ausente: {ref}")
        if UNRESOLVED_TAG_RE.search(body):
            errors.append(f"Tag 5e.tools não resolvida: {ref}")
        for dependency in extract_references(path):
            if dependency not in selected_urls:
                errors.append(f"Referência fora do manifesto em {ref}: {dependency}")
    if manifest.get("missing_local"):
        errors.extend(f"Referência local originalmente ausente: {ref}" for ref in manifest["missing_local"])
    if any(item["status"] != "resolved" for item in manifest["selected"]):
        errors.append("Manifesto contém entidades não resolvidas")
    return errors


def assert_fresh_manifest(manifest: dict[str, Any]) -> None:
    current = hash_paths(input_paths())
    if current != manifest.get("input_fingerprint"):
        raise RebuildError("Manifesto obsoleto: campanhas ou compêndio mudaram após o scan")


def promote(manifest: dict[str, Any], staging: Path = DEFAULT_STAGING) -> None:
    assert_fresh_manifest(manifest)
    errors = validate_staging(manifest, staging)
    if errors:
        raise RebuildError("Staging inválido:\n- " + "\n- ".join(errors))
    backup = PROJECT_ROOT / ".compendium-staging" / "backup"
    if backup.exists():
        shutil.rmtree(backup)
    shutil.copytree(COMPENDIUM_ROOT, backup)
    try:
        selected = {item["url"] for item in manifest["selected"]}
        for ref, path in compendium_pages().items():
            if ref not in selected:
                path.unlink()
        for ref, source in compendium_pages(staging).items():
            destination = COMPENDIUM_ROOT / source.relative_to(staging)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(".md.tmp")
            shutil.copy2(source, temporary)
            temporary.replace(destination)
    except Exception:
        shutil.rmtree(COMPENDIUM_ROOT)
        shutil.copytree(backup, COMPENDIUM_ROOT)
        raise


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RebuildError(f"Manifesto inválido: {exc}") from exc


def save_manifest(manifest: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["scan", "resolve", "generate", "validate", "promote", "rebuild"])
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--staging", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--apply", action="store_true", help="Obrigatório para promover e remover conteúdo ativo.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command in {"scan", "rebuild"}:
            manifest = scan_inventory()
            save_manifest(manifest, args.manifest)
            print(json.dumps(manifest["counts"], ensure_ascii=False))
            if args.command == "scan":
                return 0
        else:
            manifest = load_manifest(args.manifest)
        catalog = FiveEToolsCatalog(args.cache)
        if args.command in {"resolve", "rebuild"}:
            resolve_manifest(manifest, catalog)
            save_manifest(manifest, args.manifest)
            failures = [item for item in manifest["selected"] if item["status"] != "resolved"]
            print(f"Resolvidas: {len(manifest['selected']) - len(failures)}; falhas: {len(failures)}")
            if failures:
                for item in failures:
                    print(f"ERRO {item['url']}: {item['error']}", file=sys.stderr)
                return 2
            if args.command == "resolve":
                return 0
        if args.command in {"generate", "rebuild"}:
            generate_staging(manifest, catalog, args.staging)
            errors = validate_staging(manifest, args.staging)
            if errors:
                raise RebuildError("Staging inválido:\n- " + "\n- ".join(errors))
            print(f"Staging válido: {len(manifest['selected'])} entidades")
            return 0
        if args.command == "validate":
            errors = validate_staging(manifest, args.staging)
            if errors:
                raise RebuildError("Staging inválido:\n- " + "\n- ".join(errors))
            print("Staging válido")
            return 0
        if args.command == "promote":
            if not args.apply:
                raise RebuildError("Promoção é destrutiva; execute novamente com --apply")
            promote(manifest, args.staging)
            print("Compêndio promovido com sucesso")
            return 0
    except RebuildError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
