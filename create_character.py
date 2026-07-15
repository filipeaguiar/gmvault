#!/usr/bin/env python3
"""
create_character_v1.py — Criação de personagem guiada por dados para o GM Vault.

Usa dados estruturados do 5e.tools para guiar na escolha da espécie,
variante/subespécie, classe, atributos e calcula valores derivados como HP e AC.
"""
import os
import sys
import json
import argparse
import urllib.request
import yaml

from dnd_utils import (
    slugify,
    get_modifier,
    dump_yaml_indented,
    fetch_from_5etools,
    fetch_class_json,
    publish_compendium_page,
    ensure_compendium_class_overview,
    STANDARD_ACTION_REFS,
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
def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value if value else (str(default) if default is not None else "")

def ask_int(prompt, default=0):
    while True:
        raw = ask(prompt, default)
        try:
            return int(raw)
        except ValueError:
            print("  ⚠ Digite um número inteiro válido.")

def ask_choice(prompt, options):
    try:
        from rich.console import Console
        from rich.table import Table
        import math

        console = Console()
        console.print(f"\n[bold]{prompt}[/]")

        # Se houver muitas opções, organiza em até 4 colunas
        num_cols = 4 if len(options) >= 8 else 1

        if num_cols > 1:
            table = Table(show_header=False, box=None, padding=(0, 2))
            for _ in range(num_cols):
                table.add_column()

            num_rows = math.ceil(len(options) / num_cols)
            for r in range(num_rows):
                row_cells = []
                for c in range(num_cols):
                    idx = r + c * num_rows
                    if idx < len(options):
                        # Formata o item: converte tuplas em string caso ocorra na lista de subespécies
                        opt_val = options[idx]
                        if isinstance(opt_val, tuple):
                            opt_label = str(opt_val[0])
                        else:
                            opt_label = str(opt_val)
                        row_cells.append(f"[bold cyan]{idx+1:2d}.[/] {opt_label}")
                    else:
                        row_cells.append("")
                table.add_row(*row_cells)
            console.print(table)
        else:
            for i, opt in enumerate(options, 1):
                opt_label = opt[0] if isinstance(opt, tuple) else opt
                console.print(f"  [bold cyan]{i}[/]  {opt_label}")
    except ImportError:
        print(f"\n{prompt}")
        for i, opt in enumerate(options, 1):
            opt_label = opt[0] if isinstance(opt, tuple) else opt
            print(f"  {i}. {opt_label}")

    while True:
        raw = ask("Escolha", "1")
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        except ValueError:
            pass
        print(f"  ⚠ Escolha inválida. Escolha entre 1 e {len(options)}.")

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
                print(f"  {index}. {feat['name']} ({feat.get('source', 'sem fonte')})")
    except ImportError:
        print(f"\n{prompt}")
        for index, feat in enumerate(options, 1):
            print(f"  {index}. {feat['name']} ({feat.get('source', 'sem fonte')})")

    while True:
        raw = ask("Escolhas (separe números por vírgula)")
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


def print_header(title):
    print(f"\n{'═' * 50}\n  {title}\n{'═' * 50}")

# ──────────────────────────────────────────────
# Fluxo Principal de Criação
# ──────────────────────────────────────────────
def main():
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

    # 1. Selecionar campanha
    if not args.campaign:
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

    # 3. Escolher Espécie
    print_header("SELEÇÃO DE ESPÉCIE")
    sp_data = load_species_data()
    if not sp_data:
        print("ERRO: Não foi possível carregar as espécies do 5e.tools.", file=sys.stderr)
        sys.exit(1)

    # Filtrar espécies principais
    base_species = sorted(list(set(
        r.get("name") for r in sp_data.get("race", [])
        if "name" in r and not r.get("_copy")
    )))
    selected_species_name = ask_choice("Selecione a Espécie Base:", base_species)

    # Procurar a melhor entrada de espécie base considerando prioridade de fontes (evita DMG/NPC templates)
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
    # Inclui a opção "Sem variante / Base"
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

    # Resolver bônus de atributos da espécie
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
    subclass = ask("Subclasse (deixe vazio se não houver)", "")

    # 4.1 Selecionar talentos conforme o nível
    selected_feats = select_feats_for_level(level)
    if selected_feats:
        print(f"  Talentos escolhidos: {', '.join(selected_feats)}")
        print("  ⚠ Verifique no passo de atributos os possíveis aumentos concedidos pelos talentos escolhidos.")

    # Obter dados de vida (Hit Dice)
    class_entry = class_data.get("class", [{}])[0]
    hd_info = class_entry.get("hd", {"number": 1, "faces": 8})
    hd_faces = hd_info.get("faces", 8)
    hd_str = f"d{hd_faces}"

    # 5. Coletar Atributos
    print_header("ATRIBUTOS BASE (Standard Array / Point Buy / Rolado)")
    print("Digite seus atributos base (antes dos aumentos).")
    
    base_stats = {}
    for s in STAT_NAMES:
        base_stats[s] = ask_int(f"  {STAT_LABELS[s]}", 10)

    # Inicializa final_stats com base_stats
    final_stats = {s: base_stats[s] for s in STAT_NAMES}

    # Mostrar aumentos padrão calculados da espécie
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

    # Sempre oferecer as opções de aplicação de bônus
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

    # Calcular modificadores finais
    mods = {s: get_modifier(final_stats[s]) for s in STAT_NAMES}

    # 6. Coletar Perícias (Skills) e Especializações (Expertise)
    print_header("PROFICIÊNCIAS EM PERÍCIAS (SKILLS)")
    
    # 6.1 Identificar perícias automáticas da espécie
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

    # 6.2 Perícias de Classe
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

    # 6.2.5 Perícias extras (Background, etc.)
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
            print(f"  Perícias extras escolhidas: {', '.join(s.title() for s in extra_skills)}")

    # 6.3 Especialização (Expertise)
    expertise_count = 0
    if selected_class_name.lower() == "rogue":
        expertise_count = 2 if level < 6 else 4
    elif selected_class_name.lower() == "bard":
        if level >= 10:
            expertise_count = 4
        elif level >= 3:
            expertise_count = 2

    expertises_selected = set()
    all_proficient = auto_skills.union(selected_skills).union(extra_skills)
    
    actual_exp_count = min(expertise_count, len(all_proficient))
    
    if actual_exp_count > 0 and all_proficient:
        print_header("ESPECIALIZAÇÃO (EXPERTISE)")
        proficient_list = sorted(list(all_proficient))
        print(f"  Escolha até {actual_exp_count} perícias para especialização (bônus duplicado):")
        for i, sk in enumerate(proficient_list, 1):
            print(f"    {i}. {sk.replace('-', ' ').title()}")
            
        while len(expertises_selected) < actual_exp_count:
            raw_exp = ask(f"Escolha até {actual_exp_count} perícias (ex: 1,2)", "1")
            try:
                indices = [int(x.strip()) for x in raw_exp.split(",") if x.strip()]
                valid_indices = [idx for idx in indices if 1 <= idx <= len(proficient_list)]
                for idx in valid_indices:
                    expertises_selected.add(proficient_list[idx - 1])
                    if len(expertises_selected) >= actual_exp_count:
                        break
            except ValueError:
                print("    ⚠ Entrada inválida. Digite apenas números separados por vírgula.")
                
        print(f"  Especializações escolhidas: {', '.join(s.title() for s in expertises_selected)}")

    # 6. Calcular HP e Valores Derivados
    # HP Máximo: Dado máximo no nível 1 + Mod de CON, e a média nos níveis subsequentes
    con_mod = mods["con"]
    hd_average = (hd_faces // 2) + 1
    max_hp = hd_faces + con_mod + (level - 1) * (hd_average + con_mod)
    # Garante que HP seja pelo menos 1 por nível
    if max_hp < level:
        max_hp = level

    # Velocidade e Sentidos derivados da espécie
    walk_speed = 30
    darkvision_dist = 0
    size_val = "Medium"

    if base_race_entry:
        spd_info = base_race_entry.get("speed", 30)
        if isinstance(spd_info, dict):
            walk_speed = spd_info.get("walk", 30)
        elif isinstance(spd_info, (int, float)):
            walk_speed = spd_info
        
        darkvision_dist = base_race_entry.get("darkvision", 0)
        size_list = base_race_entry.get("size", ["M"])
        size_val = "Medium" if "M" in size_list else "Small" if "S" in size_list else "Medium"

    if is_variant and selected_sub_entry:
        if "speed" in selected_sub_entry:
            spd_info = selected_sub_entry.get("speed", 30)
            if isinstance(spd_info, dict):
                walk_speed = spd_info.get("walk", 30)
            elif isinstance(spd_info, (int, float)):
                walk_speed = spd_info
        if "darkvision" in selected_sub_entry:
            darkvision_dist = selected_sub_entry.get("darkvision", darkvision_dist)

    walk_speed_m = f"{walk_speed * 0.3:.1f}m".replace(".0", "")

    # 7. Sincronizar com o Compêndio
    print_header("SINCRONIZANDO COMPÊNDIO")
    compendium_refs = []

    # Sincroniza Espécie (kind: species)
    ref_species = fetch_from_5etools("species", selected_species_name)
    if ref_species:
        compendium_refs.append(ref_species)

    # Sincroniza Variante/Subespécie se houver
    if is_variant:
        ref_sub = fetch_from_5etools("subclass" if "subclass" in selected_subspecies_label else "species", selected_sub_entry.get("name"))
        if ref_sub:
            compendium_refs.append(ref_sub)

    # Sincroniza Classe
    ref_class = fetch_from_5etools("class", selected_class_name)
    if ref_class:
        compendium_refs.append(ref_class)
        ensure_compendium_class_overview(selected_class_name, class_data)

    # Sincroniza talentos escolhidos
    for feat_name in selected_feats:
        ref_feat = fetch_from_5etools("feat", feat_name)
        if ref_feat:
            compendium_refs.append(ref_feat)

    # Adicionar ações básicas
    for action_name, action_ref in STANDARD_ACTION_REFS.items():
        compendium_refs.append(action_ref)
        publish_compendium_page(action_ref)

    # 8. Gerar Arquivo Final
    print_header("GRAVANDO FICHA")
    
    slug = slugify(char_name)
    file_path = f"content/campaigns/{args.campaign}/characters/{slug}.md"
    prof_bonus = (level - 1) // 4 + 2

    # Criar saves padrão da classe
    class_saves = {s: False for s in STAT_NAMES}
    prof_saves_from_class = class_entry.get("proficiency", [])
    # Geralmente os saves da classe estão definidos como proficiencies de saving throws no 5e.tools
    # Se não encontrado diretamente, vamos perguntar ao usuário
    print("\nQuais saving throws são proficientes para sua classe?")
    for s in STAT_NAMES:
        class_saves[s] = ask(f"  Proficiente em Save de {STAT_LABELS[s]}? (s/N)").lower() in ("s", "sim", "y", "yes")

    saves = {s: mods[s] + (prof_bonus if class_saves[s] else 0) for s in STAT_NAMES}
    saves_summary_parts = []
    for s in STAT_NAMES:
        if class_saves[s]:
            sign = "+" if saves[s] >= 0 else ""
            saves_summary_parts.append(f"{s.capitalize()} {sign}{saves[s]}")
    saves_summary = ", ".join(saves_summary_parts)

    # Calcula bônus das skills com base em proficiências e expertise
    skills_data = {}
    for sk, stat_key in SKILL_MAP.items():
        is_prof = sk in all_proficient
        is_exp = sk in expertises_selected
        
        bonus = mods[stat_key]
        if is_exp:
            bonus += 2 * prof_bonus
        elif is_prof:
            bonus += prof_bonus
            
        skills_data[sk] = {
            "bonus": bonus,
            "proficient": is_prof,
            "expertise": is_exp,
            "stat": stat_key
        }

    passive_senses = {
        "perception": 10 + skills_data["perception"]["bonus"],
        "investigation": 10 + skills_data["investigation"]["bonus"],
        "insight": 10 + skills_data["insight"]["bonus"]
    }
    senses_str = f"Passive Perception {passive_senses['perception']}"
    if darkvision_dist > 0:
        senses_str += f", Darkvision {darkvision_dist} ft."

    # Ações
    actions_data = []
    for action_name, action_ref in STANDARD_ACTION_REFS.items():
        actions_data.append({
            "name": action_name,
            "ref": action_ref,
            "max_uses": 0,
            "reset": ""
        })

    classes_data = [{
        "name": selected_class_name,
        "level": level,
        "subclass": subclass
    }]

    summary_str = f"{full_species_name} {selected_class_name} {level}"
    if subclass:
        summary_str += f" ({subclass})"
    summary_str += " criado manualmente guiado por dados."

    feats_field = f"feats:{dump_yaml_indented(selected_feats, 2)}" if selected_feats else "feats: []"

    markdown = f"""---
title: {json.dumps(char_name)}
date: 2026-07-09T19:00:00Z
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
    gp: 0
    ep: 0
    pp: 0
  skills:{dump_yaml_indented(skills_data, 4)}
  actions:{dump_yaml_indented(actions_data, 4)}
  equipment: []
  spells: []
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

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ Ficha de personagem V1 criada com sucesso em: {file_path}")

if __name__ == "__main__":
    main()
