import urllib.request
import json
import os
import unicodedata
import re
import yaml
class GoBackException(Exception):
    pass



def dump_yaml_indented(data, indent=2):
    if not data:
        return " []" if isinstance(data, list) else " {}"
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    prefix = " " * indent
    return "\n" + "\n".join(prefix + line for line in yaml_str.splitlines())

# Active community 5etools mirror URL for raw data
DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"

# Revisões de regras de personagem são preferidas às versões anteriores.
SOURCE_PRIORITY = ("XPHB", "PHB", "TCE", "XGE", "MPMM", "VGM", "ERLW", "GGR", "DMG")


def source_priority(entry_or_source):
    """Return a stable priority key, preferring the 2024 XPHB revision."""
    source = entry_or_source.get("source", "") if isinstance(entry_or_source, dict) else entry_or_source
    source = str(source or "").replace("-", "").upper()
    try:
        return (SOURCE_PRIORITY.index(source), source)
    except ValueError:
        return (len(SOURCE_PRIORITY), source)


_json_cache = {}

def get_json_data(url):
    """Retorna dados JSON baixados de uma URL com cache em memória."""
    if url in _json_cache:
        return _json_cache[url]
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            _json_cache[url] = data
            return data
    except Exception as e:
        print(f"  [5e.tools] Erro ao baixar {url}: {e}")
        return None


def get_modifier(score):
    return (score - 10) // 2


SPELLCASTING_ABILITY_KEYS = frozenset({"str", "dex", "con", "int", "wis", "cha"})


def normalize_spellcasting_ability(value):
    """Return a supported ability key or ``None`` without guessing."""
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    return normalized if normalized in SPELLCASTING_ABILITY_KEYS else None


def spellcasting_ability_from_class_data(class_data, class_name=None):
    """Resolve one class' declared 5e.tools ``spellcastingAbility`` field."""
    if not isinstance(class_data, dict):
        return None
    entries = class_data.get("class")
    if not isinstance(entries, list):
        return None
    if class_name:
        expected = str(class_name).casefold()
        entries = [
            entry for entry in entries
            if isinstance(entry, dict) and str(entry.get("name", "")).casefold() == expected
        ]
    abilities = {
        normalize_spellcasting_ability(entry.get("spellcastingAbility"))
        for entry in entries if isinstance(entry, dict)
    }
    abilities.discard(None)
    return abilities.pop() if len(abilities) == 1 else None


def _single_class_name(char_info):
    """Return the only class name represented by a character, if unambiguous."""
    if not isinstance(char_info, dict):
        return None
    progression = char_info.get("classes_progression")
    if isinstance(progression, list) and progression:
        names = [
            entry.get("name") for entry in progression
            if isinstance(entry, dict) and isinstance(entry.get("name"), str) and entry["name"].strip()
        ]
        if len(names) != 1:
            return None
        return names[0]
    class_name = char_info.get("class")
    return class_name if isinstance(class_name, str) and class_name.strip() else None


def refresh_character_spellcasting_ability(char_info):
    """Refresh a single-class profile ability from class data without guessing."""
    class_name = _single_class_name(char_info)
    if not class_name:
        return None
    ability = spellcasting_ability_from_class_data(fetch_class_json(class_name), class_name)
    if ability:
        profile = char_info.get("spellcasting")
        if not isinstance(profile, dict):
            profile = {}
            char_info["spellcasting"] = profile
        profile["ability"] = ability
    return ability


def resolve_spell_attack_bonus(char_info):
    """Resolve explicit or single-class derived spell attack bonus, if known."""
    if not isinstance(char_info, dict):
        return None
    explicit = char_info.get("spell_attack_bonus")
    try:
        explicit = int(explicit)
    except (TypeError, ValueError):
        explicit = None
    if explicit not in (None, 0):
        return explicit
    if _single_class_name(char_info) is None:
        return None
    profile = char_info.get("spellcasting")
    ability = normalize_spellcasting_ability(profile.get("ability")) if isinstance(profile, dict) else None
    mods = char_info.get("mods")
    if not ability or not isinstance(mods, dict):
        return None
    try:
        return int(char_info["proficiency_bonus"]) + int(mods[ability])
    except (KeyError, TypeError, ValueError):
        return None


SPELLCASTING_PREPARED_CLASSES = {"cleric", "druid", "paladin", "artificer", "clerigo", "druida", "paladino", "artifice"}
SPELLCASTING_PACT_CLASSES = {"warlock", "bruxo"}
SPELLCASTING_KNOWN_CLASSES = {"bard", "sorcerer", "wizard", "ranger", "bardo", "feiticeiro", "mago", "patrulheiro"}

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '', text.replace(' ', '-'))
    return text


STANDARD_ACTION_REFS = {
    "Ataque": "/compendium/rules/action-attack/",
    "Esconder": "/compendium/rules/action-hide/",
    "Desengajar": "/compendium/rules/action-disengage/",
    "Disparar": "/compendium/rules/action-dash/",
    "Ajudar": "/compendium/rules/action-help/",
    "Esquivar": "/compendium/rules/action-dodge/",
    "Usar Objeto": "/compendium/rules/action-use-object/",
}


def publish_compendium_page(ref):
    """Publica uma nota de regra referenciada por uma ficha de jogador."""
    if not isinstance(ref, str) or not ref.startswith("/compendium/"):
        return
    path = f"content{ref.rstrip('/')}.md"
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()
        updated = content.replace("draft: true", "draft: false", 1).replace("status: \"draft\"", "status: \"ready\"", 1)
        if updated != content:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(updated)
            print(f"  [Compêndio] Nota publicada para ficha de jogador: {path}")
    except OSError:
        return


def ensure_compendium_class_overview(class_name, class_data, subclass_name=None):
    """Preenche páginas de classe/subclasse vazias com a progressão local."""
    if not class_data:
        return None

    is_subclass = bool(subclass_name)
    page_name = subclass_name or class_name
    slug = slugify(page_name)
    dest_path = f"content/compendium/classes/{slug}.md"
    ref_path = f"/compendium/classes/{slug}/"

    existing_has_body = False
    if os.path.exists(dest_path):
        try:
            with open(dest_path, "r", encoding="utf-8") as handle:
                existing = handle.read()
            body = existing.split("---", 2)[-1].strip() if existing.startswith("---") else existing.strip()
            existing_has_body = bool(body)
        except OSError:
            existing_has_body = True

    if is_subclass:
        features = [
            feature for feature in class_data.get("subclassFeature", [])
            if feature.get("subclassShortName", "").lower() == subclass_name.lower()
        ]
        title = page_name
        summary = f"Progressão da subclasse {page_name}."
    else:
        features = [
            feature for feature in class_data.get("classFeature", [])
            if feature.get("className", "").lower() == class_name.lower()
        ]
        class_def = next((item for item in class_data.get("class", []) if item.get("name", "").lower() == class_name.lower()), {})
        title = class_name
        summary = f"Progressão da classe {class_name}."

    if not features:
        return ref_path if existing_has_body else None

    def ensure_feature_page(feature):
        """Garante que uma característica da classe tenha conteúdo público no compêndio."""
        name = feature.get("name")
        if not name:
            return None
        feature_ref = f"/compendium/rules/{slugify(name)}/"
        feature_path = f"content{feature_ref.rstrip('/')}.md"
        description = parse_entries(feature.get("entries", []))

        if os.path.exists(feature_path):
            with open(feature_path, "r", encoding="utf-8") as handle:
                existing = handle.read()
            updated = existing
            if "draft: true" in updated:
                updated = updated.replace("draft: true", "draft: false", 1)
            if re.search(r"^visibility:", updated, re.MULTILINE):
                updated = re.sub(r"^visibility:.*$", 'visibility: "public"', updated, count=1, flags=re.MULTILINE)
            elif "---" in updated:
                updated = updated.replace("\n---", '\nvisibility: "public"\n---', 1)
            if description and updated.rstrip().endswith("---"):
                updated = updated.rstrip() + f"\n\n{description}\n"
            if updated != existing:
                with open(feature_path, "w", encoding="utf-8") as handle:
                    handle.write(updated)
            return feature_ref if description or existing != updated else None

        if not description:
            return None
        os.makedirs(os.path.dirname(feature_path), exist_ok=True)
        markdown = f'''---
title: "{name}"
type: "rule"
draft: false
weight: 10
tags:
  - compendio
  - classe
visibility: "public"
status: "draft"
---

{description}
'''
        with open(feature_path, "w", encoding="utf-8") as handle:
            handle.write(markdown)
        return feature_ref

    lines = []
    seen = set()
    current_level = None
    for feature in sorted(features, key=lambda item: (item.get("level", 0), item.get("name", ""))):
        name = feature.get("name")
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        level = feature.get("level", 1)
        if level != current_level:
            if current_level is not None:
                lines.append("")
            lines.extend([f"### Nível {level}", ""])
            current_level = level
        feature_ref = ensure_feature_page(feature)
        if feature_ref:
            lines.append(f"- [{name}]({feature_ref})")
        else:
            lines.append(f"- {name}")

    if existing_has_body:
        return ref_path

    markdown = f"""---
title: "{title}"
type: "class"
draft: false
weight: 10
tags:
  - compendio
  - classe
visibility: "public"
status: "ready"
---

{chr(10).join(lines)}
"""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    print(f"  [Compêndio] Página de classe preenchida: {dest_path}")
    return ref_path


def clean_5etools_tags(text):
    """Remove 5e.tools inline tags while preserving their visible label.

    The tag syntax is ``{@type name|source|display text}``. The optional source
    is metadata, not text for display; a display label is only present after it.
    """
    def repl(match):
        tag_type = match.group(1).lower()
        parts = match.group(2).split("|")
        value = parts[0]
        # A single suffix is the source (for example, ``|XPHB``). Only a third
        # field or later supplies an explicit visible label. Filter tags are an
        # exception: their remaining fields are query parameters, never labels.
        final_label = value if tag_type == "filter" else (parts[-1] if len(parts) >= 3 else value)

        if tag_type in ["damage", "dice", "scaledamage", "scaledice"]:
            notation = normalize_dice_notation(value)
            # Dice tags use their suffix as a display label, unlike reference
            # tags, whose second field is the source.
            final_label = parts[-1] if len(parts) >= 2 else value
            if tag_type in ["scaledamage", "scaledice"]:
                final_label = notation
            return f'<span class="dice+" data-roll-notation="{notation}">{final_label}</span>'

        return final_label

    return re.sub(r'\{@(\w+)\s+([^}]+)\}', repl, text)

def parse_entries(entries):
    lines = []
    if not entries:
        return ""
    for entry in entries:
        if isinstance(entry, str):
            lines.append(entry)
        elif isinstance(entry, dict):
            name = entry.get("name")
            sub_entries = entry.get("entries")
            if name and sub_entries:
                lines.append(f"\n### {name}")
                lines.append(parse_entries(sub_entries))
            elif entry.get("type") == "list":
                for item in entry.get("items", []):
                    lines.append(f"* {item}")
    return clean_5etools_tags("\n\n".join(lines))


def create_rule_stub(name, entries, *, source=None):
    """Create a class-feature rule through the provenance-aware serializer.

    Existing rule pages are retained for compatibility. New pages are resolved
    from 5e.tools so their front matter records the remote entity required for
    later repairs and synchronizations.
    """
    slug = slugify(name)
    ref = f"/compendium/rules/{slug}/"
    path = os.path.join("content", "compendium", "rules", f"{slug}.md")
    if os.path.exists(path):
        return ref

    try:
        from compendium_rebuild import sync_compendium_entity

        synced = sync_compendium_entity(
            "rule", name, slug=slug, source=str(source or "").upper() or None,
            origin="character",
        )
        if synced:
            return synced
    except Exception as exc:
        print(f"  [Compêndio] Não foi possível sincronizar regra {name!r}: {exc}")

    # Compatibility fallback for a rule that cannot be resolved remotely.
    description = parse_entries(entries) or f"Descrição da característica {name}."
    os.makedirs(os.path.dirname(path), exist_ok=True)
    markdown = f'''---
title: "{name}"
type: "rule"
draft: false
weight: 10
tags:
  - compendio
  - regra
  - classe
visibility: "public"
status: "ready"
---

{description}
'''
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    print(f"  [Compêndio] Criado stub sem proveniência: {path}")
    return ref

def fetch_class_json(class_name):
    url_index = DATA_BASE_URL + "class/index.json"
    try:
        class_index = get_json_data(url_index)
        if not class_index:
            return None
        class_key = class_name.lower()
        filename = class_index.get(class_key)
        if not filename:
            for k, f in class_index.items():
                if k in class_key or class_key in k:
                    filename = f
                    break
        if filename:
            url_class = DATA_BASE_URL + "class/" + filename
            return get_json_data(url_class)
    except Exception as e:
        print(f"  [5e.tools] Erro ao carregar dados de classe para {class_name}: {e}")
    return None

def load_background_data():
    url = DATA_BASE_URL + "backgrounds.json"
    return get_json_data(url)

def load_item_data():
    url = DATA_BASE_URL + "items.json"
    return get_json_data(url)

def extract_background_equipment(bg_name, bg_data):
    """Retorna uma lista de itens concedidos pelo background no formato [{name, quantity}] e o valor em ouro."""
    items = []
    gold = 0
    for bg in bg_data.get("background", []):
        if bg.get("name") == bg_name: # Pegamos a primeira ocorrência ou pode filtrar por source
            equip = bg.get("startingEquipment", [])
            if equip and "A" in equip[0]:
                for entry in equip[0]["A"]:
                    if "item" in entry:
                        raw_item = entry["item"].split("|")[0]
                        items.append({"name": raw_item.title(), "quantity": entry.get("quantity", 1)})
                    elif "equipmentType" in entry:
                        items.append({"name": entry["equipmentType"], "quantity": 1})
                    elif "value" in entry:
                        gold += entry["value"] / 100 # value is in CP usually, so / 100 to get GP. Wait, 1600 = 16 GP?
            break
    return items, gold

def extract_pack_items(pack_name, item_data):
    """Busca um pacote e extrai seus itens componentes."""
    import re
    items = []
    for item in item_data.get("item", []):
        if item.get("name") == pack_name:
            # We must parse entries to find {@item name|source}
            entries = json.dumps(item.get("entries", []))
            # Match {@item name} or {@item name|source} etc.
            matches = re.findall(r'\{@item ([^\|\}]+)', entries)
            # Find quantities (heurística simples: procurar "10 {@item Torch" ou similar)
            # Por simplicidade, assumiremos quantidade 1 se não conseguirmos parear facilmente,
            # ou podemos melhorar. Para o pack, vamos retornar os nomes únicos.
            for m in matches:
                # Basic quantity check by looking right before the match
                items.append({"name": m.title(), "quantity": 1}) # Simplificado
            break
    return items

def search_item_by_name(query, item_data=None):
    """Retorna uma lista de nomes distintos de itens que correspondam à query (case-insensitive)."""
    if not item_data:
        item_data = load_item_data()

    # We also need to search items-base.json for basic weapons and armor
    url = DATA_BASE_URL + "items-base.json"
    base_data = get_json_data(url) or {"item": []}

    all_items = (
        item_data.get("item", [])
        + item_data.get("baseitem", [])
        + base_data.get("item", [])
        + base_data.get("baseitem", [])
    )

    query_lower = query.lower()
    matches = set()

    for item in all_items:
        name = item.get("name", "")
        if query_lower in name.lower():
            # Exclude magic variants if too noisy, but for now just add all matches
            matches.add(name)

    # Sort matches by length so exact/shorter matches appear first
    return sorted(list(matches), key=lambda x: (len(x), x))


def load_spell_data():
    """Carrega as magias do PHB, Xanathar e Tasha do 5e.tools e as combina."""
    combined = {"spell": []}
    files = ["spells/spells-xphb.json", "spells/spells-phb.json", "spells/spells-tce.json", "spells/spells-xge.json"]
    for file in files:
        url = DATA_BASE_URL + file
        data = get_json_data(url)
        if data and "spell" in data:
            combined["spell"].extend(data["spell"])
    return combined


def search_spell_by_name(query, spell_data=None):
    """Retorna uma lista de nomes distintos de magias que correspondam à query (case-insensitive)."""
    if not spell_data:
        spell_data = load_spell_data()
    if not spell_data or "spell" not in spell_data:
        return []

    query_lower = query.lower()
    matches = set()
    for spell in spell_data["spell"]:
        name = spell.get("name", "")
        if query_lower in name.lower():
            matches.add(name)

    return sorted(list(matches), key=lambda x: (len(x), x))


def calculate_spell_slots(class_name, level):
    """Retorna um dicionário {nivel: quantidade} de slots de magia para a classe e nível fornecidos."""
    c_name = class_name.lower()

    # Full Casters: bard, cleric, druid, sorcerer, wizard
    full_casters = {"bard", "cleric", "druid", "sorcerer", "wizard", "bardo", "clérigo", "druida", "feiticeiro", "mago"}
    # Half Casters: paladin, ranger
    half_casters = {"paladin", "ranger", "paladino", "patrulheiro"}
    # Artificer
    artificer = {"artificer", "artífice"}
    # Warlock
    warlock = {"warlock", "bruxo"}

    if c_name in full_casters:
        progression = {
            1: {1: 2},
            2: {1: 3},
            3: {1: 4, 2: 2},
            4: {1: 4, 2: 3},
            5: {1: 4, 2: 3, 3: 2},
            6: {1: 4, 2: 3, 3: 3},
            7: {1: 4, 2: 3, 3: 3, 4: 1},
            8: {1: 4, 2: 3, 3: 3, 4: 2},
            9: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            10: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
            11: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
            12: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
            13: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
            14: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
            15: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
            16: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
            17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
            18: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 1, 9: 1},
            19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1},
            20: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 2, 8: 1, 9: 1}
        }
        return progression.get(level, {})

    elif c_name in half_casters:
        progression = {
            1: {},
            2: {1: 2},
            3: {1: 3},
            4: {1: 3},
            5: {1: 4, 2: 2},
            6: {1: 4, 2: 2},
            7: {1: 4, 2: 3},
            8: {1: 4, 2: 3},
            9: {1: 4, 2: 3, 3: 2},
            10: {1: 4, 2: 3, 3: 2},
            11: {1: 4, 2: 3, 3: 3},
            12: {1: 4, 2: 3, 3: 3},
            13: {1: 4, 2: 3, 3: 3, 4: 1},
            14: {1: 4, 2: 3, 3: 3, 4: 1},
            15: {1: 4, 2: 3, 3: 3, 4: 2},
            16: {1: 4, 2: 3, 3: 3, 4: 2},
            17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            18: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
            20: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2}
        }
        return progression.get(level, {})

    elif c_name in artificer:
        progression = {
            1: {1: 2},
            2: {1: 2},
            3: {1: 3},
            4: {1: 3},
            5: {1: 4, 2: 2},
            6: {1: 4, 2: 2},
            7: {1: 4, 2: 3},
            8: {1: 4, 2: 3},
            9: {1: 4, 2: 3, 3: 2},
            10: {1: 4, 2: 3, 3: 2},
            11: {1: 4, 2: 3, 3: 3},
            12: {1: 4, 2: 3, 3: 3},
            13: {1: 4, 2: 3, 3: 3, 4: 1},
            14: {1: 4, 2: 3, 3: 3, 4: 1},
            15: {1: 4, 2: 3, 3: 3, 4: 2},
            16: {1: 4, 2: 3, 3: 3, 4: 2},
            17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            18: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
            20: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2}
        }
        return progression.get(level, {})

    elif c_name in warlock:
        progression = {
            1: {1: 1},
            2: {1: 2},
            3: {2: 2},
            4: {2: 2},
            5: {3: 2},
            6: {3: 2},
            7: {4: 2},
            8: {4: 2},
            9: {5: 2},
            10: {5: 2},
            11: {5: 3},
            12: {5: 3},
            13: {5: 3},
            14: {5: 3},
            15: {5: 3},
            16: {5: 3},
            17: {5: 4},
            18: {5: 4},
            19: {5: 4},
            20: {5: 4}
        }
        return progression.get(level, {})

    return {}


def build_level_up_plan(char_info, class_data):
    """Build a non-mutating XPHB-first plan for the next level of one class."""
    if not isinstance(char_info, dict):
        return {"valid": False, "error": "char_info inválido"}
    class_name = str(char_info.get("class") or "").strip()
    current_level = int(char_info.get("class_level") or char_info.get("level") or 0)
    if not class_name or current_level < 1 or current_level >= 20:
        return {"valid": False, "error": "classe ou nível inválido"}
    subclass = str(char_info.get("subclass") or "").strip()
    subclass_short = subclass
    if subclass:
        match = next((item for item in class_data.get("subclass", []) if item.get("name", "").casefold() == subclass.casefold()), None)
        if match:
            subclass_short = match.get("shortName") or subclass
    target_level = current_level + 1
    features = get_class_features_at_level(class_data, class_name, subclass_short, target_level)
    pending = [feature.get("name") for feature in features if any(token in feature.get("name", "").casefold() for token in ("improvement", "invocation", "option", "choice"))]
    return {"valid": True, "class": class_name, "subclass_short": subclass_short, "current_level": current_level, "target_level": target_level, "features": features, "pending_choices": pending}


def get_class_features_at_level(class_data, class_name, subclass_short, level):
    """Retorna lista de características novas da classe e subclasse para um nível específico."""
    features = []

    # XPHB is preferred when a class/subclass feature was reprinted.
    for key, owner_key, owner in (("classFeature", "className", class_name), ("subclassFeature", "subclassShortName", subclass_short)):
        if not owner:
            continue
        matches = [f for f in class_data.get(key, []) if f.get(owner_key, "").lower() == owner.lower() and f.get("level", 1) == level]
        grouped = {}
        for feature in matches:
            name = feature.get("name", "").casefold()
            if name not in grouped or source_priority(feature) < source_priority(grouped[name]):
                grouped[name] = feature
        features.extend(grouped.values())
    return features


def get_asi_levels(class_name):
    """Retorna os níveis em que a classe ganha ASI/Talento."""
    # Default ASI levels for most classes
    default_asi = {4, 8, 12, 16, 19}

    # Fighter gets extra ASIs at 6 and 14
    fighter_asi = {4, 6, 8, 12, 14, 16, 19}

    # Rogue gets extra ASI at 10
    rogue_asi = {4, 8, 10, 12, 16, 19}

    c_name = class_name.lower()
    if c_name in ("fighter", "guerreiro"):
        return fighter_asi
    elif c_name in ("rogue", "ladino"):
        return rogue_asi
    return default_asi


SPELLCASTING_PREPARED_CLASSES = {"cleric", "druid", "paladin", "wizard", "artificer", "clérigo", "druida", "paladino", "mago", "artífice"}
SPELLCASTING_KNOWN_CLASSES = {"bard", "sorcerer", "ranger", "bardo", "feiticeiro", "patrulheiro"}
SPELLCASTING_PACT_CLASSES = {"warlock", "bruxo"}
SPELL_AVAILABILITY_PRIORITY = {
    "": 0,
    "catalog": 0,
    "known": 1,
    "prepared": 2,
    "granted": 3,
    "always": 4,
}


def canonical_spell_ref(ref):
    """Normaliza somente URLs internas canônicas de magia."""
    if not isinstance(ref, str):
        return None
    value = ref.strip()
    if not value.startswith("/compendium/spells/"):
        return None
    return value.rstrip("/") + "/"


def materialize_spell(name, fetcher=None):
    """Materializa uma magia pelo resolvedor compartilhado, sem fabricar URL."""
    if not isinstance(name, str) or not name.strip():
        return None
    resolver = fetcher or fetch_from_5etools
    ref = resolver("spell", name.strip())
    normalized = canonical_spell_ref(ref)
    if not normalized:
        print(f"  [Compêndio] Magia não resolvida: {name}")
    return normalized


def build_spell_entry(
    ref,
    *,
    prepared=None,
    availability=None,
    source=None,
    usage=None,
    can_prepare=None,
):
    """Cria uma associação mínima; identidade e mecânica ficam no compêndio."""
    normalized = canonical_spell_ref(ref)
    if not normalized:
        return None
    entry = {"ref": normalized}
    if prepared is not None:
        entry["prepared"] = bool(prepared)
    if availability:
        entry["availability"] = str(availability).lower()
    if source:
        entry["source"] = str(source)
    if usage:
        entry["usage"] = str(usage)
    if can_prepare is not None:
        entry["can_prepare"] = bool(can_prepare)
    return entry


def merge_spell_entries(current, incoming):
    """Mescla estado operacional pela referência, favorecendo disponibilidade."""
    merged = dict(current)
    merged["ref"] = canonical_spell_ref(incoming.get("ref") or current.get("ref"))
    if current.get("prepared") or incoming.get("prepared"):
        merged["prepared"] = True
    elif "prepared" in current or "prepared" in incoming:
        merged["prepared"] = False

    old_availability = str(current.get("availability") or "").lower()
    new_availability = str(incoming.get("availability") or "").lower()
    if SPELL_AVAILABILITY_PRIORITY.get(new_availability, 0) > SPELL_AVAILABILITY_PRIORITY.get(old_availability, 0):
        merged["availability"] = new_availability
    elif old_availability:
        merged["availability"] = old_availability

    sources = []
    for entry in (current, incoming):
        values = entry.get("sources") or [entry.get("source")]
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if value and value not in sources:
                sources.append(value)
    if sources:
        merged["source"] = sources[0]
        if len(sources) > 1:
            merged["sources"] = sources

    usages = []
    for entry in (current, incoming):
        values = entry.get("usages") or [entry.get("usage")]
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if value and value not in usages:
                usages.append(value)
    if usages:
        merged["usage"] = usages[0]
        if len(usages) > 1:
            merged["usages"] = usages

    if current.get("can_prepare") is True or incoming.get("can_prepare") is True:
        merged["can_prepare"] = True
    elif "can_prepare" in current or "can_prepare" in incoming:
        merged["can_prepare"] = False
    return merged


def deduplicate_spell_entries(entries):
    """Deduplica associações canônicas sem copiar título, nível ou mecânica."""
    by_ref = {}
    order = []
    for raw in entries or []:
        if not isinstance(raw, dict):
            continue
        ref = canonical_spell_ref(raw.get("ref"))
        if not ref:
            continue
        minimal = build_spell_entry(
            ref,
            prepared=raw.get("prepared") if "prepared" in raw else None,
            availability=raw.get("availability"),
            source=raw.get("source"),
            usage=raw.get("usage"),
            can_prepare=raw.get("can_prepare") if "can_prepare" in raw else None,
        )
        if raw.get("sources"):
            minimal["sources"] = list(raw["sources"])
        if raw.get("usages"):
            minimal["usages"] = list(raw["usages"])
        if ref not in by_ref:
            by_ref[ref] = minimal
            order.append(ref)
        else:
            by_ref[ref] = merge_spell_entries(by_ref[ref], minimal)
    return [by_ref[ref] for ref in order]


def materialize_spell_entry(name, *, fetcher=None, **state):
    """Resolve o nome e produz uma entrada operacional, ou ``None``."""
    ref = materialize_spell(name, fetcher=fetcher)
    return build_spell_entry(ref, **state) if ref else None


def normalize_character_spell_entries(entries, fetcher=None, preserve_unresolved=True):
    """Normaliza legado resolvível e preserva fallback inline não resolvido."""
    normalized = []
    unresolved = []
    for raw in entries or []:
        if not isinstance(raw, dict):
            continue
        ref = canonical_spell_ref(raw.get("ref"))
        if not ref and raw.get("name"):
            ref = materialize_spell(str(raw["name"]), fetcher=fetcher)
        if not ref:
            if preserve_unresolved:
                unresolved.append(dict(raw))
            continue
        entry = build_spell_entry(
            ref,
            prepared=raw.get("prepared") if "prepared" in raw else None,
            availability=raw.get("availability"),
            source=raw.get("source"),
            usage=raw.get("usage"),
            can_prepare=raw.get("can_prepare") if "can_prepare" in raw else None,
        )
        normalized.append(entry)
    return deduplicate_spell_entries(normalized) + unresolved


def infer_spellcasting_profile(
    class_name,
    level=0,
    spell_slots=None,
    spells=None,
    class_spells=None,
    casting_ability=None,
    explicit_kind=None,
    class_data=None,
):
    """Infere um perfil mínimo de conjuração para a UI da ficha."""
    c_name = (class_name or "").strip().lower()
    casting_ability = (
        normalize_spellcasting_ability(casting_ability)
        or spellcasting_ability_from_class_data(class_data, class_name)
    )
    spell_slots = spell_slots or {}
    spells = spells or []
    class_spells = class_spells or []

    prepared_spells = []
    known_spells = []
    cantrips_known = 0
    for spell in spells:
        if not isinstance(spell, dict):
            continue
        if "level" in spell and spell.get("level") == 0:
            cantrips_known += 1
        if spell.get("prepared"):
            prepared_spells.append(spell)
        else:
            known_spells.append(spell)

    if explicit_kind:
        kind = explicit_kind
    elif c_name in SPELLCASTING_PACT_CLASSES:
        kind = "pact"
    elif c_name in SPELLCASTING_PREPARED_CLASSES:
        kind = "prepared"
    elif c_name in SPELLCASTING_KNOWN_CLASSES:
        kind = "known"
    elif prepared_spells and known_spells:
        kind = "hybrid"
    elif prepared_spells:
        kind = "prepared"
    elif class_spells and spells:
        kind = "known"
    else:
        kind = "none"

    slot_total = 0
    slot_levels = []
    normalized_slots = {}
    for raw_level, value in spell_slots.items():
        try:
            slot_level = int(raw_level)
            slot_count = int(value)
        except (TypeError, ValueError):
            continue
        if slot_level > 0 and slot_count > 0:
            normalized_slots[slot_level] = slot_count
            slot_levels.append(slot_level)
            slot_total += slot_count

    # Perfis híbridos exigem ``can_prepare`` por entrada; a regra global é
    # deliberadamente somente leitura para não oferecer uma ação inválida.
    can_prepare = kind == "prepared"
    can_mark_known = kind in {"known", "hybrid", "pact"}
    uses_pact_slots = kind == "pact"
    slot_label = "Espaços de Magia" if not uses_pact_slots else "Espaços de Pacto"
    slot_summary = f"{slot_total} espaço{'s' if slot_total != 1 else ''}" if slot_total else "Sem espaços"
    if cantrips_known:
        slot_summary = f"{slot_summary} · {cantrips_known} truque{'s' if cantrips_known != 1 else ''}"

    if kind == "pact":
        prepared_label = "Magias Conhecidas"
        known_label = "Magias de Pacto"
    elif kind == "known":
        prepared_label = "Magias Conhecidas"
        known_label = "Magias Conhecidas"
    else:
        prepared_label = "Magias Preparadas"
        known_label = "Magias Conhecidas"

    profile = {
        "kind": kind,
        "ability": casting_ability or "",
        "can_prepare": can_prepare,
        "can_mark_known": can_mark_known,
        "uses_pact_slots": uses_pact_slots,
        "slot_label": slot_label,
        "slot_total": slot_total,
        "slot_levels": sorted(set(slot_levels)),
        "slot_summary": slot_summary,
        "pact_slot_level": max(slot_levels) if uses_pact_slots and slot_levels else 0,
        "pact_slot_count": (
            normalized_slots.get(max(slot_levels), 0)
            if uses_pact_slots and slot_levels
            else 0
        ),
        "prepared_label": prepared_label,
        "known_label": known_label,
        "prepared_count": len(prepared_spells),
        "known_count": len(known_spells),
        "cantrips_known": cantrips_known,
        "total_spells": len(prepared_spells) + len(known_spells),
        "prepared_limit": len(prepared_spells),
        "class_count": len(class_spells),
    }
    return profile
CLASS_MAP_PT_EN = {
    "clérigo": "Cleric",
    "cleric": "Cleric",
    "paladino": "Paladin",
    "paladin": "Paladin",
    "druida": "Druid",
    "druid": "Druid",
    "artífice": "Artificer",
    "artificer": "Artificer",
    "mago": "Wizard",
    "wizard": "Wizard",
    "bardo": "Bard",
    "bard": "Bard",
    "feiticeiro": "Sorcerer",
    "sorcerer": "Sorcerer",
    "bruxo": "Warlock",
    "warlock": "Warlock",
    "patrulheiro": "Ranger",
    "ranger": "Ranger"
}


def load_sources_data():
    """Carrega o mapeamento de fontes e classes de spells/sources.json."""
    url = DATA_BASE_URL + "spells/sources.json"
    return get_json_data(url)


def import_all_class_spells(class_name):
    """Importa todas as magias de uma classe do 5e.tools para o compêndio local."""
    mapped_class = CLASS_MAP_PT_EN.get(class_name.lower())
    if not mapped_class:
        print(f"  [Aviso] Classe {class_name} não reconhecida para importação de magias.")
        return []

    sources = load_sources_data()
    if not sources:
        return []

    spells_to_import = []
    # Loop over all books (PHB, XGE, TCE)
    for book, spells_dict in sources.items():
        if book not in ["PHB", "XGE", "TCE"]:
            continue
        for spell_name, info in spells_dict.items():
            classes = info.get("class", [])
            for c in classes:
                if c.get("name") == mapped_class:
                    spells_to_import.append(spell_name)
                    break

    print(f"  [5e.tools] Encontradas {len(spells_to_import)} magias para a classe {mapped_class}.")
    imported_refs = []

    # Batch import
    total = len(spells_to_import)
    for idx, spell_name in enumerate(spells_to_import, 1):
        if idx % 15 == 0 or idx == total:
            print(f"  [5e.tools] Importando magias de {mapped_class}: {idx}/{total}...")
        ref = fetch_from_5etools("spell", spell_name)
        if ref:
            imported_refs.append(ref)

    return imported_refs


def update_frontmatter_field(path, field_name, field_value):
    """Atualiza um campo YAML preservando integralmente o corpo Markdown."""
    with open(path, "r", encoding="utf-8") as source:
        original = source.read()
    if not original.startswith("---"):
        return False
    parts = original.split("---", 2)
    if len(parts) != 3:
        return False
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        return False
    metadata[field_name] = field_value
    rendered = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    with open(path, "w", encoding="utf-8") as destination:
        destination.write(f"---\n{rendered}---{parts[2]}")
    return True


SPELL_ROLL_TAG_RE = re.compile(
    r"\{@(damage|dice|scaledamage|scaledice)\s+([^{}]+)\}",
    re.IGNORECASE,
)
DICE_TERM_RE = re.compile(r"([+-]?)(\d*)d(\d+)|([+-]?)(\d+)", re.IGNORECASE)


def iter_5etools_strings(value):
    """Percorre recursivamente estruturas do 5e.tools e produz strings."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_5etools_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_5etools_strings(item)


def normalize_dice_notation(notation):
    """Normaliza espaços sem interpretar prosa ou alterar a fórmula."""
    value = str(notation).strip().replace("−", "-")
    value = re.sub(r"\s+", "", value)
    return value.replace("D", "d")


def parse_scaling_levels(value):
    """Converte progressões ``1-9`` ou ``3,5,7,9`` em patamares."""
    text = str(value).strip()
    if re.fullmatch(r"\d+\s*-\s*\d+", text):
        start, end = (int(part.strip()) for part in text.split("-", 1))
        return list(range(start, end + 1)) if end >= start else []
    levels = []
    for part in text.split(","):
        part = part.strip()
        if part.isdigit():
            levels.append(int(part))
    return levels


def add_dice_notation(base, increment, times):
    """Soma expressões simples de dados para materializar um patamar."""
    base = normalize_dice_notation(base)
    increment = normalize_dice_notation(increment)
    if times <= 0:
        return base

    def parse_expression(expression):
        position = 0
        dice = {}
        constant = 0
        for match in DICE_TERM_RE.finditer(expression):
            if match.start() != position:
                return None
            position = match.end()
            if match.group(3):
                sign = -1 if match.group(1) == "-" else 1
                count = int(match.group(2) or 1) * sign
                sides = int(match.group(3))
                dice[sides] = dice.get(sides, 0) + count
            else:
                sign = -1 if match.group(4) == "-" else 1
                constant += int(match.group(5)) * sign
        if position != len(expression):
            return None
        return dice, constant

    parsed_base = parse_expression(base)
    parsed_increment = parse_expression(increment)
    if parsed_base is None or parsed_increment is None:
        return base
    dice, constant = parsed_base
    increment_dice, increment_constant = parsed_increment
    for sides, count in increment_dice.items():
        dice[sides] = dice.get(sides, 0) + count * times
    constant += increment_constant * times

    parts = []
    for sides in sorted(dice):
        count = dice[sides]
        if count:
            parts.append(f"{count}d{sides}")
    if constant:
        sign = "+" if constant > 0 and parts else ""
        parts.append(f"{sign}{constant}")
    return "".join(parts) or "0"


def build_scaling_thresholds(base, level_spec, increment):
    levels = parse_scaling_levels(level_spec)
    return {
        str(level): add_dice_notation(base, increment, index)
        for index, level in enumerate(levels)
    }


def extract_spell_rolls(spell):
    """Extrai rolagens estruturadas sem inferir regras escritas em prosa."""
    healing = "HL" in (spell.get("miscTags") or [])
    damage_types = list(dict.fromkeys(spell.get("damageInflict") or []))
    rolls = []

    def roll_kind(tag_type):
        if tag_type in {"damage", "scaledamage"}:
            return "damage"
        return "healing" if healing else "dice"

    def find_roll(kind, notation):
        for roll in rolls:
            if roll["kind"] == kind and roll["notation"] == notation:
                return roll
        return None

    values = [spell.get("entries", []), spell.get("entriesHigherLevel", [])]
    for text in iter_5etools_strings(values):
        for match in SPELL_ROLL_TAG_RE.finditer(text):
            tag_type = match.group(1).lower()
            payload = match.group(2)
            parts = [part.strip() for part in payload.split("|")]
            kind = roll_kind(tag_type)
            notation = normalize_dice_notation(parts[0])
            roll = find_roll(kind, notation)
            if roll is None:
                label = {"damage": "Dano", "healing": "Cura", "dice": "Dados"}[kind]
                roll = {"kind": kind, "notation": notation, "label": label}
                if kind == "damage" and len(damage_types) == 1:
                    roll["damage_type"] = damage_types[0]
                rolls.append(roll)
            if tag_type in {"scaledamage", "scaledice"} and len(parts) >= 3:
                roll["scaling"] = {
                    "mode": "spell_slot",
                    "thresholds": build_scaling_thresholds(
                        notation, parts[1], parts[2]
                    ),
                }

    scaling_level_dice = spell.get("scalingLevelDice")
    character_scaling_values = set()
    scaling_entries = (
        scaling_level_dice
        if isinstance(scaling_level_dice, list)
        else [scaling_level_dice]
        if isinstance(scaling_level_dice, dict)
        else []
    )
    for scaling_entry in scaling_entries:
        scaling = scaling_entry.get("scaling") or {}
        if not scaling:
            continue
        thresholds = {
            str(level): normalize_dice_notation(notation)
            for level, notation in scaling.items()
        }
        first_notation = next(iter(thresholds.values()))
        kind = "healing" if healing else "damage" if damage_types else "dice"
        roll = find_roll(kind, first_notation)
        if roll is None:
            label = scaling_entry.get("label") or {
                "damage": "Dano",
                "healing": "Cura",
                "dice": "Dados",
            }[kind]
            roll = {"kind": kind, "notation": first_notation, "label": label}
            if kind == "damage" and len(damage_types) == 1:
                roll["damage_type"] = damage_types[0]
            rolls.append(roll)
        roll["scaling"] = {
            "mode": "character_level",
            "thresholds": thresholds,
        }
        character_scaling_values.update(
            (kind, notation) for notation in thresholds.values()
        )

    return [
        roll
        for roll in rolls
        if roll.get("scaling")
        or (roll["kind"], roll["notation"]) not in character_scaling_values
    ]


def extract_spell_mechanics(spell):
    """Mapeia metadados mecânicos canônicos de uma magia do 5e.tools."""
    attack_map = {"M": "melee", "R": "ranged"}
    attacks = spell.get("spellAttack") or []
    attack_type = next(
        (attack_map[value] for value in attacks if value in attack_map), None
    )
    return {
        "level_number": int(spell.get("level", 0)),
        "attack_type": attack_type,
        "damage_types": list(dict.fromkeys(spell.get("damageInflict") or [])),
        "saving_throws": list(dict.fromkeys(spell.get("savingThrow") or [])),
        "rolls": extract_spell_rolls(spell),
    }


def fetch_from_5etools(kind, english_name):
    slug = slugify(english_name)
    print(f"  [5e.tools] Tentando baixar '{english_name}' ({kind})...")

    # Use the same deterministic resolver and current-schema serializers as the
    # controlled compendium rebuild. Unsupported legacy kinds continue through
    # the compatibility implementation below.
    shared_kind = "species" if kind == "race" else kind
    if shared_kind in {"spell", "item", "magic_item", "feat", "species", "class", "rule"}:
        try:
            from compendium_rebuild import sync_compendium_entity

            shared_ref = sync_compendium_entity(shared_kind, english_name, slug=slug)
            if shared_ref:
                print(f"  [5e.tools] Sincronizado pelo gerador compartilhado: {shared_ref}")
                return shared_ref
        except Exception as exc:
            print(f"  [5e.tools] Gerador compartilhado indisponível; usando compatibilidade: {exc}")

    file_map = {
        "spell": ["spells/spells-xphb.json", "spells/spells-phb.json", "spells/spells-tce.json", "spells/spells-xge.json"],
        "item": ["items.json", "items-base.json"],
        "magic_item": ["items.json", "items-base.json"],
        "feat": ["feats.json"],
        "race": ["races.json"],
        "species": ["races.json"],
        "class": ["classes.json"],
        "item_mastery": ["items-base.json"],
    }

    # Caching check (Task 2.2)
    content_dir_check = f"content/compendium/{kind}s"
    if kind == "magic_item":
        content_dir_check = "content/compendium/magic-items"
    elif kind == "species" or kind == "race":
        content_dir_check = "content/compendium/species"
    elif kind in ["class", "subclass"]:
        content_dir_check = "content/compendium/classes"
    elif kind == "item_mastery":
        content_dir_check = "content/compendium/rules"

    slug_check = slug
    if kind == "item_mastery":
        slug_check = f"weapon-mastery-{slug}"

    dest_path_check = f"{content_dir_check}/{slug_check}.md"
    if os.path.exists(dest_path_check) and kind not in {"item", "magic_item", "spell"}:
        print(f"  [5e.tools] Encontrado localmente: {dest_path_check}")
        if kind in ["class", "subclass"]:
            return f"/compendium/classes/{slug_check}/"
        elif kind == "item_mastery":
            return f"/compendium/rules/{slug_check}/"
        elif kind == "race" or kind == "species":
            return f"/compendium/species/{slug_check}/"
        else:
            return f"/compendium/{kind}s/{slug_check}/"
    elif os.path.exists(dest_path_check):
        print(f"  [5e.tools] Sincronizando metadados locais: {dest_path_check}")

    files = file_map.get(kind, [])
    # Lista de nomes de busca (suporta aliases para itens básicos)
    search_names = [english_name.lower()]
    item_aliases = {
        "leather": "leather armor",
        "studded leather": "studded leather armor",
        "scale mail": "scale mail armor",
        "ring mail": "ring mail armor",
        "plate": "plate armor",
        "hide": "hide armor",
        "padded": "padded armor",
        "chain mail": "chain mail armor",
        "splint": "splint armor"
    }
    # Aliases para feats com nomes diferentes no D&D Beyond vs 5e.tools
    feat_aliases = {
        "weapon mastery": "Weapon Master",
    }
    if kind in ["item", "magic_item"] and english_name.lower() in item_aliases:
        search_names.append(item_aliases[english_name.lower()])
    if kind == "feat" and english_name.lower() in feat_aliases:
        alt_name = feat_aliases[english_name.lower()]
        print(f"  [5e.tools] Alias detectado: '{english_name}' → '{alt_name}'")
        search_names.append(alt_name.lower())

    found_data = None
    headers = {'User-Agent': 'Mozilla/5.0'}

    if kind == "class":
        url_index = DATA_BASE_URL + "class/index.json"
        try:
            class_index = get_json_data(url_index)
            if class_index:
                class_key = english_name.lower()
                if class_key in class_index:
                    files = ["class/" + class_index[class_key]]
                else:
                    files = []
                    for k, filename in class_index.items():
                        if k in class_key or class_key in k:
                            files.append("class/" + filename)
        except Exception as e:
            print(f"  [5e.tools] Erro ao carregar index de classes: {e}")

    if kind == "subclass":
        url_index = DATA_BASE_URL + "class/index.json"
        try:
            class_index = get_json_data(url_index)
            if class_index:
                files = ["class/" + f for f in class_index.values()]
        except Exception as e:
            print(f"  [5e.tools] Erro ao carregar index de classes: {e}")
            files = []

    for file_path in files:
        url = DATA_BASE_URL + file_path
        try:
            data = get_json_data(url)
            if not data:
                continue

            # Buscar na lista correspondente
            if kind == "spell" and "spell" in data:
                for item in data["spell"]:
                    if item.get("name", "").lower() == english_name.lower():
                        found_data = item
                        break
            elif (kind == "item" or kind == "magic_item") and ("item" in data or "baseitem" in data):
                items_list = data.get("item", []) + data.get("baseitem", [])
                for item in items_list:
                    if item.get("name", "").lower() in search_names:
                        found_data = item
                        english_name = item.get("name")
                        slug = slugify(english_name)
                        break
            elif kind == "feat" and "feat" in data:
                for item in data["feat"]:
                    if item.get("name", "").lower() in search_names:
                        found_data = item
                        english_name = item.get("name")
                        slug = slugify(english_name)
                        break
            elif kind == "item_mastery" and "itemMastery" in data:
                for item in data["itemMastery"]:
                    if item.get("name", "").lower() == english_name.lower():
                        found_data = item
                        break
            elif (kind == "race" or kind == "species") and "race" in data:
                for item in data["race"]:
                    if item.get("name", "").lower() == english_name.lower():
                        found_data = item
                        break
            elif kind == "class" and "class" in data:
                for item in data["class"]:
                    if item.get("name", "").lower() == english_name.lower():
                        found_data = item
                        break
            elif kind == "subclass" and "subclass" in data:
                for item in data["subclass"]:
                    if item.get("name", "").lower() == english_name.lower():
                        found_data = item
                        break

            if found_data:
                break
        except Exception:
            continue

    # Fallback search: if name has parentheses (like 'Magic Initiate (Wizard)'), search for the base name
    if not found_data and "(" in english_name:
        base_name = english_name.split("(")[0].strip()
        print(f"  [5e.tools] Tentando busca secundária por '{base_name}'...")
        for file_path in files:
            url = DATA_BASE_URL + file_path
            try:
                data = get_json_data(url)
                if not data:
                    continue

                if kind == "spell" and "spell" in data:
                    for item in data["spell"]:
                        if item.get("name", "").lower() == base_name.lower():
                            found_data = item
                            english_name = base_name
                            slug = slugify(base_name)
                            break
                elif (kind == "item" or kind == "magic_item") and ("item" in data or "baseitem" in data):
                    items_list = data.get("item", []) + data.get("baseitem", [])
                    for item in items_list:
                        if item.get("name", "").lower() == base_name.lower():
                            found_data = item
                            english_name = base_name
                            slug = slugify(base_name)
                            break
                elif kind == "feat" and "feat" in data:
                    for item in data["feat"]:
                        if item.get("name", "").lower() == base_name.lower():
                            found_data = item
                            english_name = base_name
                            slug = slugify(base_name)
                            break
                if found_data:
                    break
            except Exception:
                continue

    if not found_data:
        print(f"  [5e.tools] AVISO: Não foi possível encontrar '{english_name}' nos arquivos oficiais do 5e.tools.")
        return None

    # Format and save according to kind
    content_dir = f"content/compendium/{kind}s"
    if kind == "magic_item":
        content_dir = "content/compendium/magic-items"
    elif kind == "race" or kind == "species":
        content_dir = "content/compendium/species"
    elif kind in ["class", "subclass"]:
        content_dir = "content/compendium/classes"
    elif kind == "item_mastery":
        content_dir = "content/compendium/rules"
        slug = f"weapon-mastery-{slug}"  # e.g. weapon-mastery-cleave

    os.makedirs(content_dir, exist_ok=True)
    dest_path = f"{content_dir}/{slug}.md"

    markdown = ""
    description = parse_entries(found_data.get("entries", []))

    if kind == "spell":
        level_map = {0: "Cantrip", 1: "1st level", 2: "2nd level", 3: "3rd level", 4: "4th level", 5: "5th level", 6: "6th level", 7: "7th level", 8: "8th level", 9: "9th level"}
        school_map = {"A": "Abjuration", "C": "Conjuration", "D": "Divination", "E": "Evocation", "I": "Illusion", "N": "Necromancy", "T": "Transmutation"}

        level_val = found_data.get("level", 1)
        level_str = level_map.get(level_val, f"{level_val}th level")
        school_str = school_map.get(found_data.get("school", "E"), "Evocation")

        times = found_data.get("time", [])
        cast_time = "1 action"
        if times:
            t = times[0]
            number = t.get('number', 1)
            unit = t.get('unit', 'action')
            if unit == 'bonus':
                unit = 'bonus action'
            cast_time = f"{number} {unit}"

        rng = found_data.get("range", {})
        range_str = "Self"
        if rng:
            dist = rng.get("distance", {})
            if dist:
                d_type = dist.get("type", "feet")
                if d_type == "self":
                    range_str = "Self"
                elif d_type == "touch":
                    range_str = "Touch"
                elif d_type == "sight":
                    range_str = "Sight"
                elif d_type == "unlimited":
                    range_str = "Unlimited"
                else:
                    amount = dist.get("amount")
                    if amount is not None:
                        range_str = f"{amount} {d_type}"
                    else:
                        range_str = d_type.title()
            else:
                range_str = rng.get("type", "point").title()

        comp = found_data.get("components", {})
        comps = []
        if comp.get("v"): comps.append("V")
        if comp.get("s"): comps.append("S")
        if comp.get("m"):
            mat = comp.get("m")
            m_text = mat.get("text", "") if isinstance(mat, dict) else str(mat)
            comps.append(f"M ({m_text})")
        components_str = ", ".join(comps) if comps else "None"

        durs = found_data.get("duration", [])
        duration_str = "Instantaneous"
        if durs:
            d = durs[0]
            if d.get("type") == "timed":
                t_dur = d.get("duration", {})
                duration_str = f"{t_dur.get('amount', 1)} {t_dur.get('type', 'minute')}"
                if d.get("concentration"):
                    duration_str = f"Concentration, up to {duration_str}"
            elif d.get("type") == "permanent":
                duration_str = "Permanent"

        spell_info_data = {
            "level": level_str,
            "school": school_str,
            "cast_time": cast_time,
            "range": range_str,
            "components": components_str,
            "ritual": bool((found_data.get("meta") or {}).get("ritual")),
            "duration": duration_str,
            **extract_spell_mechanics(found_data),
        }
        spell_info_yaml = dump_yaml_indented(spell_info_data, indent=2)
        higher_level_description = parse_entries(
            found_data.get("entriesHigherLevel", [])
        )
        full_description = description
        if higher_level_description:
            full_description = (
                f"{description}\n\n{higher_level_description}"
                if description
                else higher_level_description
            )

        markdown = f"""---
title: "{english_name}"
type: "spell"
draft: false
weight: 10
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

spell_info:{spell_info_yaml}
---

{full_description}
"""

    elif kind == "item" or kind == "magic_item":
        raw_item_type = found_data.get("type", "G")
        item_type = raw_item_type.split("|", 1)[0]
        type_map = {
            "G": "Adventuring Gear",
            "LA": "Light Armor",
            "MA": "Medium Armor",
            "HA": "Heavy Armor",
            "S": "Shield",
            "RG": "Ring",
            "M": "Weapon",
            "R": "Weapon",
            "AF": "Weapon",
            "P": "Potion",
            "SC": "Scroll",
            "WD": "Wand",
            "RD": "Rod",
            "ST": "Staff",
        }
        item_type_str = "Wondrous item" if found_data.get("wondrous") else type_map.get(item_type, "Adventuring Gear")

        cost_gp = f"{found_data.get('value', 0) / 100} gp" if found_data.get('value') else "—"
        weight_str = f"{found_data.get('weight', 0)} lb" if found_data.get('weight') else "—"
        rarity = found_data.get("rarity", "common").title()
        attunement = "Requires attunement" if found_data.get("reqAttune") else ""

        # Mapeamentos para armas
        prop_mapping = {
            "F": "finesse", "L": "light", "T": "thrown", "V": "versatile",
            "H": "heavy", "2H": "two-handed", "R": "reach", "A": "ammunition",
            "LD": "loading", "RL": "reload", "S": "special", "BF": "burst fire"
        }
        damage_type_mapping = {
            "P": "piercing", "S": "slashing", "B": "bludgeoning",
            "F": "fire", "C": "cold", "L": "lightning", "A": "acid",
            "O": "force", "R": "radiant", "N": "necrotic", "T": "thunder",
            "I": "poison", "Y": "psychic"
        }

        # Extrair propriedades de arma se houver
        item_props = []
        raw_props = found_data.get("property", [])
        if isinstance(raw_props, list):
            for p in raw_props:
                property_code = p.split("|", 1)[0]
                mapped = prop_mapping.get(property_code)
                if mapped:
                    item_props.append(mapped)
                else:
                    item_props.append(property_code.lower())

        dmg_str = found_data.get("dmg1")
        raw_dmg_type = found_data.get("dmgType")
        dmg_type_str = damage_type_mapping.get(raw_dmg_type) if raw_dmg_type else None

        range_val = found_data.get("range")
        ac_val = found_data.get("ac")

        # Extrair modificadores mágicos
        item_modifiers = {}
        ab_data = found_data.get("ability")
        if isinstance(ab_data, dict):
            if "static" in ab_data:
                item_modifiers["stat_override"] = {k: v for k, v in ab_data["static"].items() if k in ["str", "dex", "con", "int", "wis", "cha"]}
            else:
                bonuses = {k: v for k, v in ab_data.items() if k in ["str", "dex", "con", "int", "wis", "cha"] and isinstance(v, int)}
                if bonuses:
                    item_modifiers["stat_bonus"] = bonuses

        bonus_ac = found_data.get("bonusAc") or found_data.get("bonusArmorClass")
        if bonus_ac:
            try:
                if isinstance(bonus_ac, str):
                    bonus_ac = int(bonus_ac.replace("+", "").strip())
                item_modifiers["ac_bonus"] = int(bonus_ac)
            except ValueError:
                pass

        bonus_save = found_data.get("bonusSavingThrow")
        if bonus_save:
            try:
                if isinstance(bonus_save, str):
                    bonus_save = int(bonus_save.replace("+", "").strip())
                item_modifiers["save_bonus"] = int(bonus_save)
            except ValueError:
                pass

        # Construir dicionário item_info para YAML limpo
        item_info_data = {
            "type": item_type_str,
            "cost": cost_gp,
            "weight": weight_str
        }
        if kind == "magic_item":
            item_info_data["rarity"] = rarity
            if attunement:
                item_info_data["attunement"] = attunement

        if item_type_str == "Weapon":
            if item_type == "R":
                item_info_data["weapon_type"] = "ranged"
            else:
                item_info_data["weapon_type"] = "melee"
        if item_type in {"P", "SC"} or found_data.get("consumable"):
            item_info_data["consumable"] = True

        if item_props:
            item_info_data["properties"] = item_props
        if range_val:
            item_info_data["range"] = str(range_val)
        if dmg_str:
            item_info_data["damage"] = dmg_str
        if dmg_type_str:
            item_info_data["damage_type"] = dmg_type_str
        if ac_val:
            item_info_data["armor_class"] = int(ac_val)
            armor_type_map = {"LA": 1, "MA": 2, "HA": 3, "S": 4}
            if item_type in armor_type_map:
                item_info_data["armor_type"] = armor_type_map[item_type]

        if item_modifiers:
            item_info_data["modifiers"] = item_modifiers

        item_info_yaml = dump_yaml_indented(item_info_data, indent=2)

        markdown = f"""---
title: "{english_name}"
type: "{kind}"
draft: false
weight: 10
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

item_info:{item_info_yaml}
---

{description}
"""

    elif kind == "feat":
        prereq_list = []
        for p in found_data.get("prerequisite", []):
            if "ability" in p:
                for ab in p["ability"]:
                    for k, v in ab.items():
                        prereq_list.append(f"{k.upper()} {v}")
            if "race" in p:
                for rc in p["race"]:
                    prereq_list.append(f"{rc.get('name')} race")
            if "other" in p:
                prereq_list.append(p["other"])
        prereq_str = ", ".join(prereq_list) if prereq_list else "None"

        markdown = f"""---
title: "{english_name}"
type: "feat"
draft: false
weight: 10
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

feat_info:
  prerequisite: "{prereq_str}"
---

{description}
"""

    elif kind == "race" or kind == "species":
        scores = []
        abilities = found_data.get("ability", {})
        if isinstance(abilities, dict):
            for k, v in abilities.items():
                if isinstance(v, int):
                    scores.append(f"+{v} {k.upper()}")
        ability_str = ", ".join(scores) if scores else "+1 to all attributes"

        spd = found_data.get("speed", 30)
        speed_str = "9m"
        if isinstance(spd, dict):
            speed_str = f"{spd.get('walk', 30) * 0.3:.1f}m"
        elif isinstance(spd, (int, float)):
            speed_str = f"{spd * 0.3:.1f}m"

        markdown = f"""---
title: "{english_name}"
type: "species"
draft: false
weight: 10
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

species_info:
  ability_score: "{ability_str}"
  speed: "{speed_str}"
  languages: "Common, +1 extra"
---

{description}
"""

    elif kind == "class":
        hd = found_data.get("hd", {})
        hd_str = f"d{hd.get('faces', 8)}"

        markdown = f"""---
title: "{english_name}"
type: "class"
draft: false
weight: 10
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

class_info:
  hit_dice: "{hd_str}"
  primary_ability: "Constitution/Dexterity"
---

{description}
"""

    elif kind == "subclass":
        markdown = f"""---
title: "{english_name}"
type: "class"
draft: false
weight: 10
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

class_info:
  primary_ability: "Constitution/Dexterity"
---

{description}
"""

    elif kind == "item_mastery":
        markdown = f"""---
title: "Maestria de Arma: {english_name}"
type: "rule"
draft: false
weight: 10
tags:
  - draft
  - importado
  - weapon-mastery
visibility: "public"
status: "draft"
---

{description}
"""

    if markdown:
        if kind in {"item", "magic_item", "spell"} and os.path.exists(dest_path):
            field_name = "spell_info" if kind == "spell" else "item_info"
            field_value = spell_info_data if kind == "spell" else item_info_data
            if not update_frontmatter_field(dest_path, field_name, field_value):
                return None
            print(f"  [5e.tools] SUCESSO: Metadados estruturados atualizados em: {dest_path}")
        else:
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"  [5e.tools] SUCESSO: Arquivo de compêndio criado em: {dest_path}")
        if kind == "magic_item":
            return f"/compendium/magic-items/{slug}/"
        elif kind in ["class", "subclass"]:
            return f"/compendium/classes/{slug}/"
        elif kind == "item_mastery":
            return f"/compendium/rules/{slug}/"
        elif kind == "race" or kind == "species":
            return f"/compendium/species/{slug}/"
        else:
            return f"/compendium/{kind}s/{slug}/"

    return None


# Local character flows share this resolver instead of relying on an API importer.
def _local_compendium_page(ref):
    if not isinstance(ref, str) or not ref.startswith("/compendium/"):
        return False
    path = os.path.join("content", ref.strip("/"))
    return os.path.isfile(path + ".md") or os.path.isfile(os.path.join(path, "_index.md"))


def sync_character_compendium(char_info, references=None):
    """Resolve supported local character entities, preserving legacy data."""
    refs = [ref for ref in (references or []) if isinstance(ref, str)]
    unresolved = []
    if not isinstance(char_info, dict):
        return refs, ["char_info inválido"]

    def resolve(kind, name, entry=None):
        existing = entry.get("ref") if isinstance(entry, dict) else None
        if _local_compendium_page(existing):
            if existing not in refs:
                refs.append(existing)
            return existing
        if not isinstance(name, str) or not name.strip():
            return None
        ref = fetch_from_5etools(kind, name.strip())
        if not ref:
            unresolved.append(name.strip())
            return None
        if ref not in refs:
            refs.append(ref)
        if isinstance(entry, dict):
            entry["ref"] = ref
        return ref

    classes = char_info.get("classes_progression") or [{
        "name": char_info.get("class"), "subclass": char_info.get("subclass")
    }]
    for entry in classes:
        if isinstance(entry, dict) and resolve("class", entry.get("name")):
            ensure_compendium_class_overview(
                entry.get("name"), fetch_class_json(entry.get("name")), entry.get("subclass") or None
            )
    refresh_character_spellcasting_ability(char_info)
    resolve("species", char_info.get("species") or char_info.get("race"))
    for feat in char_info.get("feats") or []:
        resolve("feat", feat.get("name") if isinstance(feat, dict) else feat)
    for key in ("actions", "feature_actions"):
        for entry in char_info.get(key) or []:
            if isinstance(entry, dict):
                resolve("rule", entry.get("name"), entry)
    for entry in char_info.get("equipment") or []:
        if isinstance(entry, dict):
            kind = "magic_item" if "/magic-items/" in str(entry.get("ref", "")) else "item"
            resolve(kind, entry.get("name"), entry)
    for entry in char_info.get("spells") or []:
        if isinstance(entry, dict):
            resolve("spell", entry.get("name"), entry)
    return list(dict.fromkeys(refs)), list(dict.fromkeys(unresolved))
