#!/usr/bin/env python3
"""
create_character_v1.py — Criação de personagem guiada por dados para o GM Vault.

Usa dados estruturados do 5e.tools para guiar na escolha da espécie,
variante/subespécie, classe, atributos e calcula valores derivados como HP e AC.
"""
import os
import re
import sys
import json
import argparse
import urllib.request
import yaml
import dnd_utils
from datetime import datetime, timezone
from dnd_utils import (
    slugify,
    get_modifier,
    dump_yaml_indented,
    fetch_from_5etools,
    fetch_class_json,
    publish_compendium_page,
    ensure_compendium_class_overview,
    STANDARD_ACTION_REFS,
    parse_entries,
    GoBackException,
)

# ──────────────────────────────────────────────
# Configuração de URLs e Cache
# ──────────────────────────────────────────────
FEV_RACES_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/races.json"
FEV_FEATS_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/feats.json"
FEV_CLASS_INDEX_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/class/index.json"
FEV_CLASS_DATA_URL_BASE = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/class/"

# ──────────────────────────────────────────────
# Mapas e Constantes de RPG
# ──────────────────────────────────────────────
STAT_NAMES = ["str", "dex", "con", "int", "wis", "cha"]
STAT_LABELS = {
    "str": "Força (STR)",
    "dex": "Destreza (DEX)",
    "con": "Constituição (CON)",
    "int": "Inteligência (INT)",
    "wis": "Sabedoria (WIS)",
    "cha": "Carisma (CHA)",
}

SKILL_MAP = {
    "acrobatics": "dex",
    "animal-handling": "wis",
    "arcana": "int",
    "athletics": "str",
    "deception": "cha",
    "history": "int",
    "insight": "wis",
    "intimidation": "cha",
    "investigation": "int",
    "medicine": "wis",
    "nature": "int",
    "perception": "wis",
    "performance": "cha",
    "persuasion": "cha",
    "religion": "int",
    "sleight-of-hand": "dex",
    "stealth": "dex",
    "survival": "wis",
}

# ──────────────────────────────────────────────
# Funções de Cache do 5e.tools
# ──────────────────────────────────────────────
def fetch_json_with_cache(url, cache_path):
    """Carrega dados JSON com cache local para evitar requisições constantes."""
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    print(f"  [5e.tools] Baixando dados de {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            return data
    except Exception as e:
        print(f"  [5e.tools] Erro ao carregar dados: {e}")
        return None

def load_species_data():
    cache = "content/compendium/species/.races_cache.json"
    return fetch_json_with_cache(FEV_RACES_URL, cache)

def load_feats_data():
    """Carrega e armazena em cache o índice de talentos do 5e.tools."""
    cache = "content/compendium/feats/.feats_cache.json"
    return fetch_json_with_cache(FEV_FEATS_URL, cache)

def load_class_index():
    cache = "content/compendium/classes/.classes_index_cache.json"
    return fetch_json_with_cache(FEV_CLASS_INDEX_URL, cache)

def load_class_data(filename):
    url = f"{FEV_CLASS_DATA_URL_BASE}{filename}"
    cache = f"content/compendium/classes/.{filename}_cache.json"
    return fetch_json_with_cache(url, cache)

# ──────────────────────────────────────────────
# Prompts Interativos
# ──────────────────────────────────────────────
class NavigationCancelled(Exception):
    """Indica que 00 foi informado sem existir uma pergunta anterior."""


class QuestionNavigator:
    """Mantém respostas e permite editar exatamente a pergunta anterior."""

    def __init__(self):
        self.answers = []
        self.cursor = 0
        self._occurrences = {}
        self._edit_index = None

    def begin_pass(self):
        self.cursor = 0
        self._occurrences = {}

    def _key(self, kind, prompt):
        base = f"{kind}:{prompt}"
        occurrence = self._occurrences.get(base, 0)
        self._occurrences[base] = occurrence + 1
        return f"{base}#{occurrence}"

    def request_back(self):
        if self.cursor == 0:
            raise NavigationCancelled()
        self._edit_index = self.cursor - 1
        raise GoBackException()

    def answer(self, kind, prompt, reader, validator=None):
        key = self._key(kind, prompt)
        validator = validator or (lambda _value: True)

        if self.cursor < len(self.answers) and self._edit_index != self.cursor:
            saved = self.answers[self.cursor]
            if saved["key"] == key and validator(saved["value"]):
                self.cursor += 1
                return saved["value"]
            del self.answers[self.cursor:]

        value = reader()
        record = {"key": key, "value": value}
        if self.cursor < len(self.answers):
            self.answers[self.cursor] = record
        else:
            self.answers.append(record)
        self.cursor += 1
        if self._edit_index is not None and self.cursor > self._edit_index:
            self._edit_index = None
        return value


_active_navigator = None


def _go_back():
    if _active_navigator is not None:
        _active_navigator.request_back()
    raise GoBackException()


def _answer(kind, prompt, reader, validator=None):
    if _active_navigator is None:
        return reader()
    return _active_navigator.answer(kind, prompt, reader, validator)


def ask(prompt, default=None):
    def read_value():
        suffix = f" [{default}]" if default is not None else ""
        value = input(f"{prompt}{suffix} (00: voltar): ").strip()
        if value == "00":
            _go_back()
        return value if value else (str(default) if default is not None else "")

    return _answer("text", prompt, read_value)


def ask_int(prompt, default=0):
    def read_value():
        while True:
            suffix = f" [{default}]" if default is not None else ""
            raw = input(f"{prompt}{suffix} (00: voltar): ").strip()
            if raw == "00":
                _go_back()
            if not raw and default is not None:
                raw = str(default)
            try:
                return int(raw)
            except ValueError:
                print("  ⚠ Digite um número inteiro válido.")

    return _answer("int", prompt, read_value, lambda value: isinstance(value, int))


def ask_choice(prompt, options):
    def read_value():
        try:
            from rich.console import Console
            from rich.table import Table
            import math

            console = Console()
            console.print(f"\n[bold]{prompt}[/]")
            num_cols = 4 if len(options) >= 8 else 1
            if num_cols > 1:
                table = Table(show_header=False, box=None, padding=(0, 2))
                for _ in range(num_cols):
                    table.add_column()
                num_rows = math.ceil(len(options) / num_cols)
                for row in range(num_rows):
                    cells = []
                    for col in range(num_cols):
                        index = row + col * num_rows
                        if index < len(options):
                            option = options[index]
                            label = option[0] if isinstance(option, tuple) else option
                            cells.append(f"[bold cyan]{index + 1:2d}.[/] {label}")
                        else:
                            cells.append("")
                    table.add_row(*cells)
                console.print(table)
            else:
                for index, option in enumerate(options, 1):
                    label = option[0] if isinstance(option, tuple) else option
                    console.print(f"  [bold cyan]{index}[/]  {label}")
            console.print("  [bold cyan]00[/]  Voltar")
        except ImportError:
            print(f"\n{prompt}")
            for index, option in enumerate(options, 1):
                label = option[0] if isinstance(option, tuple) else option
                print(f"  {index}. {label}")
            print("  00. Voltar")

        while True:
            try:
                raw = input("Escolha (00: voltar): ").strip()
                if raw == "00":
                    _go_back()
                index = int(raw or "1")
                if 1 <= index <= len(options):
                    return options[index - 1]
            except ValueError:
                pass
            print(f"  ⚠ Escolha inválida. Escolha entre 1 e {len(options)} (ou 00 para voltar).")

    return _answer("choice", prompt, read_value, lambda value: value in options)

def filter_feats(feats_data, categories, source="XPHB"):
    """Retorna talentos das categorias indicadas, filtrando opcionalmente pela fonte."""
    if not isinstance(feats_data, dict):
        return []

    categories = set(categories)
    feats = feats_data.get("feat", [])
    if not isinstance(feats, list):
        return []

    return sorted(
        [
            feat for feat in feats
            if isinstance(feat, dict)
            and (source is None or feat.get("source") == source)
            and feat.get("category") in categories
            and feat.get("name")
        ],
        key=lambda feat: feat["name"].lower(),
    )


def get_origin_feats(feats_data, source="XPHB"):
    return filter_feats(feats_data, {"O"}, source)


def get_general_feats(feats_data, source="XPHB"):
    return filter_feats(feats_data, {"G", "FS", "FS:P", "FS:R"}, source)


def ask_multiple_feat_choices(prompt, options):
    """Exibe talentos numerados e aceita índices separados por vírgula."""
    available_names = {feat["name"] for feat in options}

    def read_value():
        try:
            from rich.console import Console
            from rich.table import Table
            import math

            console = Console()
            console.print(f"\n[bold]{prompt}[/]")
            num_cols = 4 if len(options) >= 8 else 1
            if num_cols > 1:
                table = Table(show_header=False, box=None, padding=(0, 2))
                for _ in range(num_cols):
                    table.add_column()
                num_rows = math.ceil(len(options) / num_cols)
                for row in range(num_rows):
                    cells = []
                    for col in range(num_cols):
                        index = row + col * num_rows
                        if index < len(options):
                            feat = options[index]
                            cells.append(
                                f"[bold cyan]{index + 1:2d}.[/] "
                                f"{feat['name']} ({feat.get('source', 'sem fonte')})"
                            )
                        else:
                            cells.append("")
                    table.add_row(*cells)
                console.print(table)
            else:
                for index, feat in enumerate(options, 1):
                    console.print(
                        f"  [bold cyan]{index}[/]  "
                        f"{feat['name']} ({feat.get('source', 'sem fonte')})"
                    )
            console.print("  [bold cyan]00[/]  Voltar")
        except ImportError:
            print(f"\n{prompt}")
            for index, feat in enumerate(options, 1):
                print(f"  {index}. {feat['name']} ({feat.get('source', 'sem fonte')})")
            print("  00. Voltar")

        while True:
            raw = input("Escolhas (separe números por vírgula) (00: voltar): ").strip()
            if raw == "00":
                _go_back()
            if not raw:
                return []
            try:
                indices = [int(value.strip()) for value in raw.split(",") if value.strip()]
            except ValueError:
                print("  ⚠ Entrada inválida. Digite números separados por vírgula ou deixe vazio.")
                continue
            if any(index < 1 or index > len(options) for index in indices):
                print(f"  ⚠ Escolha inválida. Use números entre 1 e {len(options)}.")
                continue

            selected = []
            for index in indices:
                feat_name = options[index - 1]["name"]
                if feat_name not in selected:
                    selected.append(feat_name)
            return selected

    return _answer(
        "multiple-choice",
        prompt,
        read_value,
        lambda values: isinstance(values, list) and set(values) <= available_names,
    )


def normalize_spell_entry(name, ref, level=0, source="class", prepared=False, always_prepared=False, known=True, can_prepare=False, usage="", origin=None):
    return {
        "name": name,
        "ref": ref,
        "level": int(level or 0),
        "source": source,
        "prepared": bool(prepared),
        "always_prepared": bool(always_prepared),
        "known": bool(known),
        "can_prepare": bool(can_prepare),
        "usage": usage or "",
        "origin": origin or source,
    }


def merge_spell_entries(entries):
    merged = []
    seen = set()
    for entry in entries:
        ref = entry.get("ref")
        key = ref or entry.get("name")
        if not key or key in seen:
            continue
        seen.add(key)
        merged.append(entry)
    return merged


def ask_manual_feats(prompt):
    """Fallback quando o índice remoto não pôde ser carregado/processado."""
    print("  ⚠ O índice de talentos não está disponível; a referência será criada pelo nome informado.")
    raw = ask(prompt)
    return [name.strip() for name in raw.split(",") if name.strip()]


def select_feats_for_level(level):
    if level == 1:
        title = "TALENTOS DE ORIGEM (XPHB)"
        categories = get_origin_feats
        manual_prompt = "Digite os nomes dos talentos de Origem (separados por vírgula)"
    elif level >= 4:
        title = "TALENTOS GERAIS/ESTILOS DE COMBATE (XPHB)"
        categories = get_general_feats
        manual_prompt = "Digite os nomes dos talentos Gerais (separados por vírgula)"
    else:
        return []

    print_header(title)
    try:
        feats_data = load_feats_data()
    except Exception as error:
        print(f"  ⚠ Erro ao carregar talentos: {error}")
        return ask_manual_feats(manual_prompt)

    if feats_data is None:
        return ask_manual_feats(manual_prompt)

    try:
        xphb_options = categories(feats_data, "XPHB")
        other_options = [
            feat for feat in categories(feats_data, None)
            if feat.get("source") != "XPHB"
        ]
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        print(f"  ⚠ Erro ao processar talentos: {error}")
        return ask_manual_feats(manual_prompt)

    catalogs = []
    if xphb_options:
        catalogs.append(("XPHB (D&D 2024) — recomendado", xphb_options))
    if other_options:
        catalogs.append(("Outros — fontes anteriores ou alternativas", other_options))

    if not catalogs:
        print("  ⚠ Nenhum talento compatível foi encontrado no índice.")
        return ask_manual_feats(manual_prompt)

    if len(catalogs) == 1:
        options = catalogs[0][1]
    else:
        catalog_labels = [f"{label} ({len(options)} talentos)" for label, options in catalogs]
        selected_label = ask_choice("Selecione a fonte dos talentos:", catalog_labels)
        selected_index = catalog_labels.index(selected_label)
        options = catalogs[selected_index][1]

    return ask_multiple_feat_choices("Selecione um ou mais talentos:", options)


def deduplicate_features(features_list, get_source_priority_fn):
    grouped = {}
    for f in features_list:
        name = f.get("name")
        if not name:
            continue
        key = name.lower()
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(f)

    deduped = []
    for key, group in grouped.items():
        group.sort(key=get_source_priority_fn)
        deduped.append(group[0])
    return deduped


def extract_roll_formula(feature_name, description, level, mods):
    name_lower = feature_name.lower()

    # Special overrides for well-known features
    if name_lower == "sneak attack" or name_lower == "ataque furtivo":
        sneak_dice = (level + 1) // 2
        return f"{sneak_dice}d6"

    if name_lower == "second wind" or name_lower == "retomar o fôlego":
        return f"1d10+{level}"

    if name_lower == "bardic inspiration" or name_lower == "inspiração bárdica":
        if level >= 15:
            return "1d12"
        elif level >= 10:
            return "1d10"
        elif level >= 5:
            return "1d8"
        else:
            return "1d6"

    # Regex search for standard dice notation (e.g. 1d6, 1d10+3, 1d8 + STR)
    matches = re.findall(r'\b(\d+d\d+(?:\s*[+-]\s*(?:\d+|str|dex|con|int|wis|cha))?)\b', description, re.IGNORECASE)
    if matches:
        formula = matches[0].lower().replace(" ", "")
        # Resolve attributes to values
        for stat, val in mods.items():
            if stat in formula:
                sign = "+" if val >= 0 else ""
                formula = formula.replace(stat, f"{sign}{val}")
                formula = formula.replace("++", "+").replace("+-", "-").replace("-+", "-").replace("--", "+")
        return formula

    return None


def prompt_choices_for_feature(feature_name, level):
    name_lower = feature_name.lower()
    choices = []

    if "fighting style" in name_lower or "estilo de luta" in name_lower:
        options = ["Defense", "Archery", "Dueling", "Great Weapon Fighting", "Two-Weapon Fighting", "Protection", "Interception", "Thrown Weapon Fighting", "Blind Fighting"]
        choice = ask_choice("Escolha seu Estilo de Luta (Fighting Style):", options)
        choices.append({
            "name": f"Fighting Style: {choice}",
            "description": f"Estilo de Luta escolhido: {choice}."
        })

    elif "metamagic" in name_lower or "metamagia" in name_lower:
        options = ["Careful Spell", "Distant Spell", "Empowered Spell", "Extended Spell", "Heightened Spell", "Quickened Spell", "Subtle Spell", "Twinned Spell"]
        count = 2 if level < 10 else 3 if level < 17 else 4
        print(f"\nSua classe permite escolher {count} opções de Metamagia:")
        selected = set()
        while len(selected) < count:
            c = ask_choice(f"Escolha a {len(selected)+1}ª Metamagia:", [opt for opt in options if opt not in selected])
            selected.add(c)
        for sel in selected:
            choices.append({
                "name": f"Metamagic: {sel}",
                "description": f"Opção de Metamagia escolhida: {sel}."
            })

    return choices


def create_rule_stub(name, entries, *, source=None):
    """Compatibility wrapper for the shared provenance-aware rule serializer."""
    return dnd_utils.create_rule_stub(name, entries, source=source)


def print_header(title):
    print(f"\n{'═' * 50}\n  {title}\n{'═' * 50}")


def calculate_skills_data(proficient_skills, mods, prof_bonus):
    """Calcula perícias no formato canônico de ``char_info.skills``."""
    skills_data = {}
    for skill, ability in SKILL_MAP.items():
        is_proficient = skill in proficient_skills
        skills_data[skill] = {
            "bonus": mods[ability] + (prof_bonus if is_proficient else 0),
            "proficient": is_proficient,
            "expertise": False,
            "stat": ability,
        }
    return skills_data


def calculate_saves_data(class_entry, mods, prof_bonus):
    """Normaliza proficiências de resistência vindas do 5e.tools."""
    raw_proficiencies = class_entry.get("proficiency", [])
    if isinstance(raw_proficiencies, dict):
        proficient = {
            stat
            for stat, enabled in raw_proficiencies.items()
            if stat in STAT_NAMES and enabled
        }
    elif isinstance(raw_proficiencies, list):
        proficient = {
            str(stat).lower() for stat in raw_proficiencies if stat in STAT_NAMES
        }
    else:
        proficient = set()

    class_saves = {stat: stat in proficient for stat in STAT_NAMES}
    saves = {
        stat: mods[stat] + (prof_bonus if class_saves[stat] else 0)
        for stat in STAT_NAMES
    }
    summary = []
    for stat in STAT_NAMES:
        if class_saves[stat]:
            value = saves[stat]
            summary.append(f"{stat.capitalize()} {'+' if value >= 0 else ''}{value}")
    return saves, class_saves, ", ".join(summary)


def build_selected_spell_entries(selected_spells, class_name, fetcher=None):
    """Materializa escolhas interativas e devolve associações mínimas."""
    class_key = (class_name or "").strip().lower()
    is_prepared = class_key in dnd_utils.SPELLCASTING_PREPARED_CLASSES
    is_pact = class_key in dnd_utils.SPELLCASTING_PACT_CLASSES
    availability = "prepared" if is_prepared else "known"
    entries = []
    unresolved = []
    for selected in selected_spells or []:
        name = selected.get("name") if isinstance(selected, dict) else None
        if not name:
            continue
        entry = dnd_utils.materialize_spell_entry(
            str(name),
            fetcher=fetcher,
            prepared=True if is_prepared else None,
            availability=availability,
            source="class",
            usage=selected.get("usage") or "1 action",
            can_prepare=is_prepared,
        )
        if entry:
            entries.append(entry)
        else:
            unresolved.append(str(name))
            print(f"  [Compêndio] Magia não adicionada: {name}")
    return dnd_utils.deduplicate_spell_entries(entries), unresolved


# ──────────────────────────────────────────────
# Fluxo Principal de Criação
# ──────────────────────────────────────────────
def main():
    global _active_navigator

    parser = argparse.ArgumentParser(description="Criação de personagem guiada por dados para o GM Vault.")
    parser.add_argument("--campaign", type=str, default=None, help="Slug da campanha de destino.")
    parser.add_argument("--interactive", "--menu", action="store_true", help="Abre o menu interativo Rich.")
    args = parser.parse_args()

    if args.interactive:
        try:
            from interactive_cli import create_character_menu
            values = create_character_menu()
            if values is None:
                print("Operação cancelada.")
                return
            args.campaign = values.get("campaign", args.campaign)
        except ImportError:
            print("  [AVISO] interactive_cli não disponível, usando modo texto.")

    campaign_argument = args.campaign

    # Inicializar variáveis para evitar UnboundLocalError ao navegar
    char_name = ""
    alignment = "True Neutral"
    selected_species_name = ""
    species_variant = ""
    is_variant = False
    full_species_name = ""
    ability_bonuses = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
    selected_class_name = ""
    level = 1
    prof_bonus = 2
    subclass = ""
    subclass_short = ""
    selected_feats = []
    hd_str = "d8"
    bg_name = ""
    bg_items = []
    bg_gold = 0
    selected_pack = "Nenhum"
    pack_items = []
    base_stats = {s: 10 for s in STAT_NAMES}
    final_stats = {s: 10 for s in STAT_NAMES}
    mods = {s: 0 for s in STAT_NAMES}
    proficient_skills = set()
    extra_items = []
    extra_spells = []
    class_spells_field_data = []
    class_entry = {}
    base_race_entry = {}
    selected_sub_entry = {}
    class_data = {}
    compendium_refs = []
    equipment_data = []
    spells_field_data = []
    spell_slots_val = {}
    hd_faces = 8
    feature_actions = []
    feature_choices = {}
    is_prepared_caster = False

    navigator = QuestionNavigator()
    _active_navigator = navigator
    navigator.begin_pass()

    step = 1
    while step <= 10:
        try:
            if step == 1:
                # 1. Selecionar campanha
                if not campaign_argument:
                    campaigns_dir = "content/campaigns"
                    if os.path.isdir(campaigns_dir):
                        campaigns = sorted([d for d in os.listdir(campaigns_dir) if os.path.isdir(os.path.join(campaigns_dir, d))])
                        if campaigns:
                            args.campaign = ask_choice("Selecione a campanha:", campaigns)
                        else:
                            args.campaign = ask("Slug da campanha", "cidadela-radiante")
                    else:
                        args.campaign = ask("Slug da campanha", "cidadela-radiante")

                print(f"\n📋 Campanha de destino: {args.campaign}")

                # 2. Coletar Nome
                print_header("NOME DO PERSONAGEM")
                char_name = ask("Nome do personagem")
                while not char_name:
                    print("  ⚠ Nome é obrigatório.")
                    char_name = ask("Nome do personagem")

                alignment = ask("Alinhamento (ex: Neutral Good)", "True Neutral")
                step = 2

            elif step == 2:
                # 3. Escolher Espécie
                print_header("SELEÇÃO DE ESPÉCIE")
                sp_data = load_species_data()
                if not sp_data:
                    print("ERRO: Não foi possível carregar as espécies do 5e.tools.", file=sys.stderr)
                    sys.exit(1)

                base_species = sorted(list(set(
                    r.get("name") for r in sp_data.get("race", [])
                    if "name" in r and not r.get("_copy")
                )))
                selected_species_name = ask_choice("Selecione a Espécie Base:", base_species)

                SOURCE_PRIORITY = ["PHB", "XPHB", "MPMM", "VGM", "ERLW", "GGR", "DMG"]
                matching_races = [r for r in sp_data.get("race", []) if r.get("name") == selected_species_name]
                def get_source_priority(entry):
                    src = entry.get("source", "")
                    if src in SOURCE_PRIORITY:
                        return SOURCE_PRIORITY.index(src)
                    return 999
                matching_races.sort(key=get_source_priority)
                base_race_entry = matching_races[0] if matching_races else None

                subspecies_options = []
                subspecies_options.append(("Espécie Base", base_race_entry))

                for s in sp_data.get("subrace", []):
                    if s.get("raceName") == selected_species_name:
                        subspecies_options.append((f"Variante: {s.get('name')}", s))

                selected_subspecies_label, selected_sub_entry = ask_choice(
                    f"Selecione uma Variante/Subespécie para {selected_species_name}:",
                    subspecies_options
                )

                is_variant = selected_subspecies_label != "Espécie Base"
                species_variant = selected_sub_entry.get('name', '') if is_variant else ""
                full_species_name = selected_species_name
                if is_variant:
                    full_species_name = f"{selected_species_name} ({species_variant})"

                ability_bonuses = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
                def apply_ab(entry):
                    if not entry or not entry.get("ability"):
                        return
                    for ab in entry.get("ability", []):
                        if isinstance(ab, dict):
                            for k, v in ab.items():
                                if k in ability_bonuses and isinstance(v, int):
                                    ability_bonuses[k] += v

                apply_ab(base_race_entry)
                if is_variant:
                    apply_ab(selected_sub_entry)
                step = 3

            elif step == 3:
                # 4. Escolher Classe e Nível
                print_header("SELEÇÃO DE CLASSE")
                class_index = load_class_index()
                if not class_index:
                    print("ERRO: Não foi possível carregar o index de classes.", file=sys.stderr)
                    sys.exit(1)

                classes_available = sorted(list(class_index.keys()))
                selected_class_name = ask_choice("Selecione a Classe principal:", [c.title() for c in classes_available])
                class_filename = class_index[selected_class_name.lower()]
                class_data = load_class_data(class_filename)

                level = ask_int("Nível do personagem", 1)
                if level < 1:
                    level = 1
                prof_bonus = (level - 1) // 4 + 2
                subclass = ""
                subclass_short = ""

                # Source priority function for subclass sorting
                SOURCE_PRIORITY = ["PHB", "XPHB", "MPMM", "VGM", "ERLW", "GGR", "DMG"]
                def get_source_priority(entry):
                    src = entry.get("source", "")
                    if src in SOURCE_PRIORITY:
                        return SOURCE_PRIORITY.index(src)
                    return 999

                if "subclass" in class_data:
                    subclass_options = ["Nenhuma"] + sorted(list(set(sc.get("name") for sc in class_data["subclass"] if sc.get("name"))))
                    selected_subclass = ask_choice("Selecione a Subclasse (se houver):", subclass_options)
                    if selected_subclass != "Nenhuma":
                        subclass = selected_subclass
                        matching_scs = [sc for sc in class_data["subclass"] if sc.get("name") == selected_subclass]
                        matching_scs.sort(key=get_source_priority)
                        subclass_short = matching_scs[0].get("shortName", selected_subclass)
                step = 4

            elif step == 4:
                # 4.1 Selecionar talentos conforme o nível
                selected_feats = select_feats_for_level(level)
                if selected_feats:
                    print(f"  Talentos escolhidos: {', '.join(selected_feats)}")
                    print("  ⚠ Verifique no passo de atributos os possíveis aumentos concedidos pelos talentos escolhidos.")

                classes_list = class_data.get("class", [])
                classes_list.sort(key=get_source_priority)
                class_entry = classes_list[0] if classes_list else {}
                hd_info = class_entry.get("hd", {"number": 1, "faces": 8})
                hd_faces = hd_info.get("faces", 8)
                hd_str = f"d{hd_faces}"
                step = 5

            elif step == 5:
                # 5. Coletar Background e Pacote Inicial
                print_header("BACKGROUND E EQUIPAMENTO INICIAL")
                bg_data = dnd_utils.load_background_data()
                item_data = dnd_utils.load_item_data()

                backgrounds = []
                if bg_data:
                    backgrounds = sorted([b.get("name") for b in bg_data.get("background", []) if b.get("source") == "XPHB"])

                selected_bg = ""
                bg_items = []
                bg_gold = 0
                if backgrounds:
                    selected_bg = ask_choice("Selecione o seu Antecedente (Background):", backgrounds)
                    bg_items, bg_gold = dnd_utils.extract_background_equipment(selected_bg, bg_data)
                    print(f"  [Equipamento] Itens recebidos do background: {', '.join([i['name'] for i in bg_items])} (+{bg_gold} GP)")
                else:
                    print("  [Aviso] Dados de backgrounds não encontrados.")

                pack_options = [
                    "Nenhum",
                    "Burglar's Pack",
                    "Diplomat's Pack",
                    "Dungeoneer's Pack",
                    "Entertainer's Pack",
                    "Explorer's Pack",
                    "Priest's Pack",
                    "Scholar's Pack"
                ]
                selected_pack = ask_choice("Selecione o seu Pacote Inicial (geralmente concedido pela sua Classe):", pack_options)
                pack_items = []
                if selected_pack != "Nenhum" and item_data:
                    pack_items = dnd_utils.extract_pack_items(selected_pack, item_data)
                    print(f"  [Equipamento] Itens do {selected_pack} descompactados e adicionados ao inventário.")
                step = 6

            elif step == 6:
                # 6. Coletar Atributos
                print_header("ATRIBUTOS BASE (Standard Array / Point Buy / Rolado)")
                print("Digite seus atributos base (antes dos aumentos).")

                base_stats = {}
                for s in STAT_NAMES:
                    base_stats[s] = ask_int(f"  {STAT_LABELS[s]}", 10)

                final_stats = {s: base_stats[s] for s in STAT_NAMES}

                print(f"\nAumentos padrão calculados da espécie {full_species_name}:")
                has_defaults = False
                for s in STAT_NAMES:
                    if ability_bonuses[s] > 0:
                        print(f"  {STAT_LABELS[s]}: +{ability_bonuses[s]}")
                        has_defaults = True
                    elif ability_bonuses[s] < 0:
                        print(f"  {STAT_LABELS[s]}: {ability_bonuses[s]}")
                        has_defaults = True

                if not has_defaults:
                    print("  Nenhum (aumentos customizáveis ou de background)")

                bonus_rule = ask_choice(
                    "Como deseja aplicar os aumentos de atributos?",
                    [
                        "Usar padrão da espécie (se houver)",
                        "Definir aumentos customizados de Background (+2 / +1)",
                        "Definir aumentos customizados de Background (+1 / +1 / +1)",
                        "Não aplicar aumentos (manter atributos base secos)"
                    ]
                )

                if bonus_rule == "Usar padrão da espécie (se houver)":
                    for s in STAT_NAMES:
                        final_stats[s] += ability_bonuses[s]

                elif bonus_rule == "Definir aumentos customizados de Background (+2 / +1)":
                    custom_stat_plus2 = ask_choice("Selecione o atributo para receber +2:", [STAT_LABELS[s] for s in STAT_NAMES])
                    custom_stat_plus1 = ask_choice("Selecione o atributo para receber +1 (deve ser diferente):", [STAT_LABELS[s] for s in STAT_NAMES if STAT_LABELS[s] != custom_stat_plus2])

                    for k, label in STAT_LABELS.items():
                        if label == custom_stat_plus2:
                            final_stats[k] += 2
                        elif label == custom_stat_plus1:
                            final_stats[k] += 1

                elif bonus_rule == "Definir aumentos customizados de Background (+1 / +1 / +1)":
                    custom_stat_1 = ask_choice("Selecione o 1º atributo para receber +1:", [STAT_LABELS[s] for s in STAT_NAMES])
                    custom_stat_2 = ask_choice("Selecione o 2º atributo para receber +1 (diferente):", [STAT_LABELS[s] for s in STAT_NAMES if STAT_LABELS[s] != custom_stat_1])
                    custom_stat_3 = ask_choice("Selecione o 3º atributo para receber +1 (diferente):", [STAT_LABELS[s] for s in STAT_NAMES if STAT_LABELS[s] not in (custom_stat_1, custom_stat_2)])

                    for k, label in STAT_LABELS.items():
                        if label in (custom_stat_1, custom_stat_2, custom_stat_3):
                            final_stats[k] += 1

                mods = {s: get_modifier(final_stats[s]) for s in STAT_NAMES}
                step = 7

            elif step == 7:
                # 6. Coletar Perícias (Skills) e Especializações (Expertise)
                print_header("PROFICIÊNCIAS EM PERÍCIAS (SKILLS)")

                auto_skills = set()
                def extract_skills(entry):
                    if not entry:
                        return
                    for p in entry.get("skillProficiencies", []):
                        for k, v in p.items():
                            if isinstance(v, bool) and v:
                                auto_skills.add(k.lower().replace(" ", "-"))
                            elif k.lower() == "choose":
                                pass
                extract_skills(base_race_entry)
                if is_variant:
                    extract_skills(selected_sub_entry)

                if auto_skills:
                    print(f"  Perícias automáticas da espécie: {', '.join(s.title() for s in auto_skills)}")

                class_skills_list = []
                choose_count = 2

                starting_prof = class_entry.get("startingProficiencies", {})
                skills_prof = starting_prof.get("skills", [])
                if skills_prof:
                    choose_info = skills_prof[0].get("choose", {})
                    choose_count = choose_info.get("count", 2)
                    class_skills_raw = choose_info.get("from", [])
                    for s_raw in class_skills_raw:
                        clean_s = s_raw.split("|")[0].strip().lower().replace(" ", "-")
                        if clean_s in SKILL_MAP:
                            class_skills_list.append(clean_s)

                if not class_skills_list:
                    class_skills_list = sorted(list(SKILL_MAP.keys()))

                class_skills_filtered = [s for s in class_skills_list if s not in auto_skills]
                if not class_skills_filtered:
                    class_skills_filtered = sorted([s for s in SKILL_MAP.keys() if s not in auto_skills])

                print(f"  Sua classe {selected_class_name} permite escolher {choose_count} perícias:")
                selected_skills = set()

                actual_choose_count = min(choose_count, len(class_skills_filtered))

                if actual_choose_count > 0:
                    for i, sk in enumerate(class_skills_filtered, 1):
                        print(f"    {i}. {sk.replace('-', ' ').title()}")

                    while len(selected_skills) < actual_choose_count:
                        prompt_msg = f"Escolha até {actual_choose_count} perícias (ex: 1,3)"
                        raw_sel = ask(prompt_msg, "1")
                        try:
                            indices = [int(x.strip()) for x in raw_sel.split(",") if x.strip()]
                            valid_indices = [idx for idx in indices if 1 <= idx <= len(class_skills_filtered)]
                            for idx in valid_indices:
                                selected_skills.add(class_skills_filtered[idx - 1])
                                if len(selected_skills) >= actual_choose_count:
                                    break
                        except ValueError:
                            print("    ⚠ Entrada inválida. Digite apenas números separados por vírgula.")

                if selected_skills:
                    print(f"  Perícias escolhidas: {', '.join(s.title() for s in selected_skills)}")

                extra_skills = set()
                extra_count = ask_int("Quantas perícias adicionais você ganha por outras fontes (Background, Talentos, etc.)?", 2)
                if extra_count > 0:
                    current_proficient = auto_skills.union(selected_skills)
                    remaining_skills = sorted([s for s in SKILL_MAP.keys() if s not in current_proficient])
                    actual_extra_count = min(extra_count, len(remaining_skills))

                    if actual_extra_count > 0:
                        print(f"\n  Escolha mais {actual_extra_count} perícias adicionais da lista geral:")
                        for i, sk in enumerate(remaining_skills, 1):
                            print(f"    {i}. {sk.replace('-', ' ').title()}")

                        while len(extra_skills) < actual_extra_count:
                            prompt_msg = f"Escolha até {actual_extra_count} perícias (ex: 1,2)"
                            raw_sel = ask(prompt_msg, "1")
                            try:
                                indices = [int(x.strip()) for x in raw_sel.split(",") if x.strip()]
                                valid_indices = [idx for idx in indices if 1 <= idx <= len(remaining_skills)]
                                for idx in valid_indices:
                                    extra_skills.add(remaining_skills[idx - 1])
                                    if len(extra_skills) >= actual_extra_count:
                                        break
                            except ValueError:
                                print("    ⚠ Entrada inválida. Digite apenas números separados por vírgula.")

                proficient_skills = auto_skills.union(selected_skills).union(extra_skills)
                step = 8

            elif step == 8:
                # 8. Extra Equipment Choice
                print_header("EQUIPAMENTOS ADICIONAIS / EXTRAS")
                extra_items = []
                while True:
                    query = ask("Digite o nome de um equipamento extra (ou deixe em branco para finalizar)")
                    if not query.strip():
                        break

                    matches = dnd_utils.search_item_by_name(query.strip())
                    if not matches:
                        print("  [Aviso] Nenhum item encontrado.")
                        continue

                    if len(matches) == 1:
                        selected_item = matches[0]
                        print(f"  Item encontrado: {selected_item}")
                    else:
                        selected_item = ask_choice("Múltiplos itens encontrados. Qual deseja?", matches)

                    qty = ask_int(f"Quantidade de {selected_item}", 1)
                    extra_items.append({"name": selected_item, "quantity": qty})
                    print(f"  {qty}x {selected_item} adicionado(s) à lista.")
                step = 9

            elif step == 9:
                # 9. Spells Choice
                print_header("MAGIAS EXTRAS / CONHECIDAS")
                extra_spells = []
                spell_data = None

                prepared_caster_classes = {"cleric", "paladin", "druid", "artificer", "clérigo", "paladino", "druida", "artífice"}
                is_prepared_caster = selected_class_name.lower() in prepared_caster_classes

                class_spells_field_data = []

                while True:
                    query = ask("Deseja adicionar uma magia conhecida/preparada? (Deixe em branco para pular/finalizar)")
                    if not query.strip():
                        break

                    if not spell_data:
                        spell_data = dnd_utils.load_spell_data()

                    matches = dnd_utils.search_spell_by_name(query.strip(), spell_data)
                    if not matches:
                        print("  [Aviso] Nenhuma magia encontrada com esse nome.")
                        continue

                    if len(matches) == 1:
                        selected_spell = matches[0]
                        print(f"  Magia encontrada: {selected_spell}")
                    else:
                        selected_spell = ask_choice("Múltiplas magias encontradas. Qual deseja?", matches)

                    spell_lvl = 0
                    for s in spell_data.get("spell", []):
                        if s.get("name") == selected_spell:
                            spell_lvl = s.get("level", 0)
                            break

                    extra_spells.append(normalize_spell_entry(
                        selected_spell,
                        f"/compendium/spells/{slugify(selected_spell)}/",
                        spell_lvl,
                        source="manual",
                        prepared=False,
                        always_prepared=False,
                        known=True,
                        can_prepare=is_prepared_caster,
                        usage="",
                        origin="manual",
                    ))
                    print(f"  {selected_spell} adicionada.")
                step = 10

            elif step == 10:
                # Coletar escolhas de características antes de qualquer gravação.
                class_features = [
                    feature for feature in class_data.get("classFeature", [])
                    if feature.get("className", "").lower() == selected_class_name.lower()
                    and feature.get("level", 1) <= level
                ]
                subclass_features = [
                    feature for feature in class_data.get("subclassFeature", [])
                    if subclass_short
                    and feature.get("subclassShortName", "").lower() == subclass_short.lower()
                    and feature.get("level", 1) <= level
                ]
                all_features = deduplicate_features(
                    class_features + subclass_features, get_source_priority
                )
                feature_choices = {}
                for feature in all_features:
                    name = feature.get("name")
                    if name:
                        choices = prompt_choices_for_feature(name, level)
                        if choices:
                            feature_choices[name] = choices
                break

        except NavigationCancelled:
            _active_navigator = None
            print("\n⚠ Operação cancelada.")
            return
        except GoBackException:
            step = 1
            navigator.begin_pass()
            print("\n↩ Voltando para a pergunta anterior...")

    # Efeitos externos começam somente após todas as perguntas serem concluídas.
    _active_navigator = None
    if is_prepared_caster:
        print(f"  [Classe Conjuradora Preparada] Baixando automaticamente todas as magias de {selected_class_name}...")
        class_spells_field_data = dnd_utils.import_all_class_spells(selected_class_name)

    # Non-interactive Calculations & File Saving
    skills_data = calculate_skills_data(proficient_skills, mods, prof_bonus)
    saves, class_saves, saves_summary = calculate_saves_data(
        class_entry, mods, prof_bonus
    )

    # HP calculation
    max_hp = hd_faces + mods["con"]
    if level > 1:
        avg_hd = int(hd_faces / 2) + 1
        max_hp += (level - 1) * (avg_hd + mods["con"])

    # Features
    feature_actions = []
    class_features = []
    if "classFeature" in class_data:
        for f in class_data["classFeature"]:
            if f.get("className", "").lower() == selected_class_name.lower():
                if f.get("level", 1) <= level:
                    class_features.append(f)

    subclass_features = []
    if subclass_short and "subclassFeature" in class_data:
        for f in class_data["subclassFeature"]:
            if f.get("subclassShortName", "").lower() == subclass_short.lower():
                if f.get("level", 1) <= level:
                    subclass_features.append(f)

    all_features = deduplicate_features(class_features + subclass_features, get_source_priority)

    for f in all_features:
        name = f.get("name")
        if not name:
            continue

        entries = f.get("entries", [])
        desc = parse_entries(entries)

        choices = feature_choices.get(name, [])
        if choices:
            for choice in choices:
                ref = create_rule_stub(choice["name"], [choice["description"]], source=f.get("source"))
                feature_actions.append({
                    "name": choice["name"],
                    "ref": ref,
                    "max_uses": 0,
                    "reset": "",
                    "source": "class"
                })
        else:
            try:
                ref = create_rule_stub(name, entries, source=f.get("source"))
                roll_formula = extract_roll_formula(name, desc, level, mods)

                action_item = {
                    "name": name,
                    "ref": ref,
                    "max_uses": 0,
                    "reset": "",
                    "source": "class"
                }
                if roll_formula:
                    action_item["roll"] = roll_formula

                feature_actions.append(action_item)
            except Exception as e:
                print(f"  [Aviso] Falha ao criar stub para característica '{name}': {e}")

    # Standard calculations: walk speed, size, darkvision
    walk_speed = 30
    size_val = "Medium"
    darkvision_dist = 0

    if base_race_entry:
        size_val = base_race_entry.get("size", ["M"])[0]
        if size_val == "M":
            size_val = "Medium"
        elif size_val == "S":
            size_val = "Small"

        spd_info = base_race_entry.get("speed", 30)
        if isinstance(spd_info, dict):
            walk_speed = spd_info.get("walk", 30)
        elif isinstance(spd_info, int):
            walk_speed = spd_info

        if "darkvision" in base_race_entry:
            darkvision_dist = base_race_entry.get("darkvision", 0)

    if is_variant and selected_sub_entry:
        size_val = selected_sub_entry.get("size", [size_val])[0]
        if size_val == "M":
            size_val = "Medium"
        elif size_val == "S":
            size_val = "Small"

        spd_info = selected_sub_entry.get("speed", walk_speed)
        if isinstance(spd_info, dict):
            walk_speed = spd_info.get("walk", walk_speed)
        elif isinstance(spd_info, int):
            walk_speed = spd_info
        if "darkvision" in selected_sub_entry:
            darkvision_dist = selected_sub_entry.get("darkvision", darkvision_dist)

    walk_speed_m = f"{walk_speed * 0.3:.1f}m".replace(".0", "")

    # Sync compendium refs
    compendium_refs = []
    ref_species = fetch_from_5etools("species", selected_species_name)
    if ref_species:
        compendium_refs.append(ref_species)

    if is_variant:
        ref_sub = fetch_from_5etools("subclass" if "subclass" in selected_subspecies_label else "species", selected_sub_entry.get("name"))
        if ref_sub:
            compendium_refs.append(ref_sub)

    ref_class = fetch_from_5etools("class", selected_class_name)
    if ref_class:
        compendium_refs.append(ref_class)
        ensure_compendium_class_overview(selected_class_name, class_data)

    for feat_name in selected_feats:
        ref_feat = fetch_from_5etools("feat", feat_name)
        if ref_feat:
            compendium_refs.append(ref_feat)

    for action_name, action_ref in STANDARD_ACTION_REFS.items():
        compendium_refs.append(action_ref)
        publish_compendium_page(action_ref)

    for act in feature_actions:
        if act.get("ref"):
            compendium_refs.append(act["ref"])

    # Equipment consolidation
    equipment_data = []
    combined_items = bg_items + pack_items + extra_items
    for item in combined_items:
        item_ref = dnd_utils.fetch_from_5etools("item", item["name"])
        if item_ref:
            compendium_refs.append(item_ref)
        else:
            item_ref = f"/compendium/items/{slugify(item['name'])}/"

        equipment_data.append({
            "name": item["name"],
            "ref": item_ref,
            "quantity": item["quantity"],
            "equipped": False
        })

    # Spells consolidation
    spells_field_data, unresolved_spells = build_selected_spell_entries(
        extra_spells, selected_class_name
    )
    compendium_refs.extend(
        entry["ref"] for entry in spells_field_data if entry.get("ref")
    )

    class_spells_field_data = list(dict.fromkeys(
        ref for ref in class_spells_field_data
        if dnd_utils.canonical_spell_ref(ref)
    ))
    if class_spells_field_data:
        compendium_refs.extend(class_spells_field_data)

    persisted_spells = merge_spell_entries(spells_field_data)
    for ref in class_spells_field_data:
        persisted_spells.append(normalize_spell_entry(
            name=ref.rstrip("/").split("/")[-1].replace("-", " ").title(),
            ref=ref,
            level=0,
            source="class",
            prepared=False,
            always_prepared=True if is_prepared_caster else False,
            known=True,
            can_prepare=is_prepared_caster,
            usage="",
            origin="class",
        ))
    persisted_spells = merge_spell_entries(persisted_spells)

    spell_slots_val = dnd_utils.calculate_spell_slots(selected_class_name, level)
    spellcasting_profile = dnd_utils.infer_spellcasting_profile(
        selected_class_name,
        level,
        spell_slots=spell_slots_val,
        spells=spells_field_data,
        class_spells=class_spells_field_data,
    )

    passive_senses = {
        "perception": 10 + skills_data["perception"]["bonus"],
        "investigation": 10 + skills_data["investigation"]["bonus"],
        "insight": 10 + skills_data["insight"]["bonus"]
    }
    senses_str = f"Passive Perception {passive_senses['perception']}"
    if darkvision_dist > 0:
        senses_str += f", Darkvision {darkvision_dist} ft."

    actions_data = []
    for action_name, action_ref in STANDARD_ACTION_REFS.items():
        actions_data.append({
            "name": action_name,
            "ref": action_ref,
            "max_uses": 0,
            "reset": ""
        })
    actions_data.extend(feature_actions)

    classes_data = [{
        "name": selected_class_name,
        "level": level,
        "subclass": subclass
    }]

    spellcasting_profile = dnd_utils.infer_spellcasting_profile(
        selected_class_name,
        level,
        spell_slots=spell_slots_val,
        spells=spells_field_data,
        class_spells=class_spells_field_data,
    )
    # Última passagem comum: cobre referências que os passos interativos não
    # conhecem isoladamente e nunca inventa URLs para conteúdo não resolvido.
    sync_char_info = {
        "class": selected_class_name,
        "level": level,
        "subclass": subclass,
        "species": selected_species_name,
        "feats": selected_feats,
        "actions": actions_data,
        "equipment": equipment_data,
        "spells": persisted_spells,
        "classes_progression": classes_data,
    }
    compendium_refs, unresolved_compendium = dnd_utils.sync_character_compendium(
        sync_char_info, compendium_refs
    )
    if unresolved_compendium:
        print("[Compêndio] Entradas não resolvidas: " + ", ".join(unresolved_compendium))
    spell_state = {
        "mode": spellcasting_profile.get("kind", "known"),
        "ability": spellcasting_profile.get("ability", ""),
        "prepared_spell_refs": [entry["ref"] for entry in spells_field_data if entry.get("prepared")],
        "known_spell_refs": [entry["ref"] for entry in spells_field_data if entry.get("known")],
        "always_prepared_spell_refs": [entry["ref"] for entry in spells_field_data if entry.get("always_prepared")],
        "class_spell_refs": class_spells_field_data,
        "bonus_spell_refs": [entry["ref"] for entry in spells_field_data if entry.get("origin") != "class"],
        "slot_progression": spell_slots_val,
        "pact_slots": spellcasting_profile.get("pact_slots", {}),
        "ritual_casting": bool(spellcasting_profile.get("ritual_casting")),
        "sources": spellcasting_profile.get("sources", []),
    }

    summary_str = f"{full_species_name} {selected_class_name} {level} criado manualmente guiado por dados."
    feats_field = f"feats:{dump_yaml_indented(selected_feats, 2)}" if selected_feats else "feats: []"

    markdown = f"""---
title: "{char_name}"
date: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
params:
  kind: "character"
draft: false
weight: 10
summary: "{summary_str}"
tags:
  - jogador
  - {slugify(selected_species_name)}
  - {slugify(selected_class_name)}
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "{selected_class_name}"
  class_level: {level}
  subclass: "{subclass}"
  level: {level}
  species: "{selected_species_name}"
  species_variant: "{species_variant}"
  ac: "{10 + mods['dex']}"
  hp: "{max_hp}"
  hp_max: "{max_hp}"
  hp_current: "{max_hp}"
  feat: ""
  {feats_field}
  size: "{size_val}"
  alignment: "{alignment}"
  dndbeyond_id: ""
  proficiency_bonus: {prof_bonus}
  spell_dc: 0
  spell_attack_bonus: 0
  avatar: ""
  spellcasting:{dump_yaml_indented(spell_state, 4)}
  speed:
    walk: {walk_speed}
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "{senses_str}"
  passive_senses:
    perception: {passive_senses['perception']}
    investigation: {passive_senses['investigation']}
    insight: {passive_senses['insight']}
  languages: "Common"
  saves:
    str: {saves['str']}
    dex: {saves['dex']}
    con: {saves['con']}
    int: {saves['int']}
    wis: {saves['wis']}
    cha: {saves['cha']}
  saves_proficient:
    str: {str(class_saves['str']).lower()}
    dex: {str(class_saves['dex']).lower()}
    con: {str(class_saves['con']).lower()}
    int: {str(class_saves['int']).lower()}
    wis: {str(class_saves['wis']).lower()}
    cha: {str(class_saves['cha']).lower()}
  saves_summary: "{saves_summary}"
  mods:
    str: {mods['str']}
    dex: {mods['dex']}
    con: {mods['con']}
    int: {mods['int']}
    wis: {mods['wis']}
    cha: {mods['cha']}
  stats:
    str: {final_stats['str']}
    dex: {final_stats['dex']}
    con: {final_stats['con']}
    int: {final_stats['int']}
    wis: {final_stats['wis']}
    cha: {final_stats['cha']}
  currencies:
    cp: 0
    sp: 0
    gp: {int(bg_gold)}
    ep: 0
    pp: 0
  skills:{dump_yaml_indented(skills_data, 4)}
  actions:{dump_yaml_indented(actions_data, 4)}
  equipment:{dump_yaml_indented(equipment_data, 4)}
  spells:{dump_yaml_indented(persisted_spells, 4)}
  spell_slots:{dump_yaml_indented(spell_slots_val, 4)}
  class_spells:{dump_yaml_indented(class_spells_field_data, 4)}
  classes_progression:{dump_yaml_indented(classes_data, 4)}

# Relacionamentos
locations: []
factions: []
compendium_refs:{dump_yaml_indented(sorted(list(set(compendium_refs))), 0)}
spells_usage: []
---

### Biografia
Este personagem foi criado manualmente via script interativo guiado por dados do 5e.tools.

### Equipamentos e Recursos
Ficha básica de V1. Use os comandos estendidos nas próximas fases para adicionar recursos adicionais.
"""

    file_path = f"content/campaigns/{args.campaign}/characters/{slugify(char_name)}.md"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ Ficha de personagem V1 criada com sucesso em: {file_path}")
    _active_navigator = None


if __name__ == "__main__":
    main()
