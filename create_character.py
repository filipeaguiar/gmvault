#!/usr/bin/env python3
"""
create_character.py — Criação interativa de personagem para o GM Vault.

Guia o usuário por um fluxo de perguntas no terminal para preencher
todos os campos do frontmatter de personagem, baixa dados do compêndio
via 5e.tools e gera o arquivo Markdown final.

Uso:
    python3 create_character.py --campaign <slug>
    python3 create_character.py --interactive
"""
import os
import sys
import json
import argparse
import yaml

from dnd_utils import (
    slugify,
    get_modifier,
    dump_yaml_indented,
    fetch_from_5etools,
    fetch_class_json,
    publish_compendium_page,
    ensure_compendium_class_overview,
    clean_5etools_tags,
    parse_entries,
    STANDARD_ACTION_REFS,
)

# ──────────────────────────────────────────────
# Mapas de perícias (D&D 5e)
# ──────────────────────────────────────────────
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

SKILL_NAMES_PT = {
    "acrobatics": "Acrobacia",
    "animal-handling": "Adestrar Animais",
    "arcana": "Arcana",
    "athletics": "Atletismo",
    "deception": "Enganação",
    "history": "História",
    "insight": "Intuição",
    "intimidation": "Intimidação",
    "investigation": "Investigação",
    "medicine": "Medicina",
    "nature": "Natureza",
    "perception": "Percepção",
    "performance": "Atuação",
    "persuasion": "Persuasão",
    "religion": "Religião",
    "sleight-of-hand": "Prestidigitação",
    "stealth": "Furtividade",
    "survival": "Sobrevivência",
}

STAT_NAMES = ["str", "dex", "con", "int", "wis", "cha"]
STAT_LABELS = {
    "str": "Força (STR)",
    "dex": "Destreza (DEX)",
    "con": "Constituição (CON)",
    "int": "Inteligência (INT)",
    "wis": "Sabedoria (WIS)",
    "cha": "Carisma (CHA)",
}


# ──────────────────────────────────────────────
# Helpers de input
# ──────────────────────────────────────────────
def ask(prompt, default=None):
    """Solicita input do usuário com um valor padrão opcional."""
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value if value else (str(default) if default is not None else "")


def ask_int(prompt, default=0):
    """Solicita um inteiro do usuário."""
    while True:
        raw = ask(prompt, default)
        try:
            return int(raw)
        except ValueError:
            print("  ⚠ Valor inválido. Digite um número inteiro.")


def ask_list(prompt, separator=","):
    """Solicita uma lista separada por vírgula."""
    raw = ask(prompt, "")
    if not raw:
        return []
    return [item.strip() for item in raw.split(separator) if item.strip()]


def ask_yes_no(prompt, default=False):
    """Pergunta sim/não."""
    hint = "S/n" if default else "s/N"
    raw = ask(f"{prompt} ({hint})", "").lower()
    if not raw:
        return default
    return raw in ("s", "sim", "y", "yes")


def ask_choice(prompt, options):
    """Mostra opções numeradas e retorna a selecionada."""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = ask("Escolha", "1")
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        except ValueError:
            pass
        print(f"  ⚠ Escolha entre 1 e {len(options)}.")


def print_header(title):
    """Exibe um cabeçalho de seção."""
    width = 50
    print(f"\n{'═' * width}")
    print(f"  {title}")
    print(f"{'═' * width}")


def print_section(title):
    """Exibe um separador de subseção."""
    print(f"\n── {title} ──")


# ──────────────────────────────────────────────
# Fluxo de criação interativa
# ──────────────────────────────────────────────
def collect_basic_info(campaign_slug):
    """Coleta informações básicas do personagem."""
    print_header("INFORMAÇÕES BÁSICAS")

    name = ask("Nome do personagem")
    while not name:
        print("  ⚠ O nome é obrigatório.")
        name = ask("Nome do personagem")

    race = ask("Raça (em inglês, ex: Human, Elf, Dwarf)")
    while not race:
        print("  ⚠ A raça é obrigatória.")
        race = ask("Raça (em inglês)")

    class_name = ask("Classe principal (em inglês, ex: Fighter, Wizard)")
    while not class_name:
        print("  ⚠ A classe é obrigatória.")
        class_name = ask("Classe principal (em inglês)")

    subclass = ask("Subclasse (em inglês, deixe vazio se não houver)", "")
    level = ask_int("Nível", 1)
    if level < 1:
        level = 1

    alignment = ask("Alinhamento (ex: Neutral Good)", "True Neutral")
    size = ask("Tamanho (Tiny, Small, Medium, Large, Huge, Gargantuan)", "Medium")

    return {
        "name": name,
        "race": race,
        "class_name": class_name,
        "subclass": subclass,
        "level": level,
        "alignment": alignment,
        "size": size,
        "campaign": campaign_slug,
    }


def collect_ability_scores():
    """Coleta os 6 atributos e calcula modificadores."""
    print_header("ATRIBUTOS")
    print("Informe o valor final de cada atributo (já com bônus de raça, etc.).\n")

    stats = {}
    for stat in STAT_NAMES:
        stats[stat] = ask_int(f"  {STAT_LABELS[stat]}", 10)

    mods = {s: get_modifier(v) for s, v in stats.items()}

    print("\n  Modificadores calculados:")
    for s in STAT_NAMES:
        sign = "+" if mods[s] >= 0 else ""
        print(f"    {STAT_LABELS[s]}: {sign}{mods[s]}")

    return stats, mods


def collect_combat_info(mods, level, class_name):
    """Coleta AC, HP, velocidades e sentidos."""
    print_header("COMBATE")

    ac = ask_int("Classe de Armadura (AC)", 10 + mods["dex"])
    hp = ask_int("Pontos de Vida Máximos (HP)", 10 + mods["con"] * level)

    print_section("Velocidades (em pés)")
    speeds = {
        "walk": ask_int("  Andar", 30),
        "fly": ask_int("  Voar", 0),
        "swim": ask_int("  Nadar", 0),
        "climb": ask_int("  Escalar", 0),
        "burrow": ask_int("  Cavar", 0),
    }

    print_section("Sentidos")
    darkvision = ask_int("  Darkvision (pés, 0 se não tiver)", 0)

    return {
        "ac": ac,
        "hp": hp,
        "speeds": speeds,
        "darkvision": darkvision,
    }


def collect_proficiencies(mods, level):
    """Coleta proficiências em saves e skills."""
    prof_bonus = (level - 1) // 4 + 2
    print_header(f"PROFICIÊNCIAS (Bônus: +{prof_bonus})")

    # Saving Throws
    print_section("Saving Throws proficientes")
    print("  Informe os saves em que o personagem é proficiente.")
    print(f"  Opções: {', '.join(s.upper() for s in STAT_NAMES)}")
    prof_saves_raw = ask_list("  Saves proficientes (separados por vírgula)")
    proficient_saves = {s: False for s in STAT_NAMES}
    for raw in prof_saves_raw:
        key = raw.lower().strip()
        if key in proficient_saves:
            proficient_saves[key] = True

    # Calcular saves
    saves = {}
    for s in STAT_NAMES:
        saves[s] = mods[s] + (prof_bonus if proficient_saves[s] else 0)

    saves_summary_parts = []
    for s in STAT_NAMES:
        if proficient_saves[s]:
            sign = "+" if saves[s] >= 0 else ""
            saves_summary_parts.append(f"{s.capitalize()} {sign}{saves[s]}")
    saves_summary = ", ".join(saves_summary_parts)

    # Skills
    print_section("Perícias")
    print("  Informe perícias em que o personagem é proficiente.")
    print("  Nomes disponíveis:")
    for sk, pt in SKILL_NAMES_PT.items():
        print(f"    {sk:20s} ({pt})")

    prof_skills_raw = ask_list("\n  Perícias proficientes (nomes em inglês, separados por vírgula)")
    proficient_skills = set()
    for raw in prof_skills_raw:
        key = raw.lower().strip()
        if key in SKILL_MAP:
            proficient_skills.add(key)
        else:
            print(f"  ⚠ Perícia '{raw}' não reconhecida, ignorada.")

    expertise_skills = set()
    if proficient_skills:
        exp_raw = ask_list("  Perícias com expertise (separadas por vírgula, ou vazio)")
        for raw in exp_raw:
            key = raw.lower().strip()
            if key in proficient_skills:
                expertise_skills.add(key)
            elif key:
                print(f"  ⚠ '{raw}' não é uma perícia proficiente, expertise ignorada.")

    # Montar skills_data
    skills_data = {}
    for skill_name, stat_key in SKILL_MAP.items():
        is_prof = skill_name in proficient_skills
        is_exp = skill_name in expertise_skills
        total = mods[stat_key]
        if is_exp:
            total += 2 * prof_bonus
        elif is_prof:
            total += prof_bonus

        skills_data[skill_name] = {
            "bonus": total,
            "proficient": is_prof or is_exp,
            "expertise": is_exp,
            "stat": stat_key,
        }

    # Sentidos passivos
    passive_senses = {
        "perception": 10 + skills_data["perception"]["bonus"],
        "investigation": 10 + skills_data["investigation"]["bonus"],
        "insight": 10 + skills_data["insight"]["bonus"],
    }

    return {
        "prof_bonus": prof_bonus,
        "proficient_saves": proficient_saves,
        "saves": saves,
        "saves_summary": saves_summary,
        "skills_data": skills_data,
        "passive_senses": passive_senses,
    }


def collect_feats():
    """Coleta talentos do personagem."""
    print_header("TALENTOS")
    feats = ask_list("Talentos (em inglês, separados por vírgula)")
    return feats


def collect_equipment():
    """Coleta equipamentos do personagem."""
    print_header("EQUIPAMENTO")
    print("Adicione itens um por vez. Digite 'fim' para terminar.\n")

    equipment_list = []
    while True:
        item_name = ask("  Nome do item (ou 'fim')")
        if item_name.lower() == "fim" or not item_name:
            break

        qty = ask_int("  Quantidade", 1)
        equipped = ask_yes_no("  Equipado?", True)
        filter_type = ask_choice("  Tipo do item", [
            "Weapon", "Armor", "Wondrous item", "Ring",
            "Potion", "Scroll", "Other Gear"
        ])
        is_magic = ask_yes_no("  Item mágico?", False)

        atk_formula = ""
        dmg_formula = ""
        if filter_type == "Weapon":
            atk_formula = ask("  Fórmula de ataque (ex: 1d20 + 7)", "")
            dmg_formula = ask("  Fórmula de dano (ex: 1d8 + 4)", "")

        equipment_list.append({
            "name": item_name,
            "quantity": qty,
            "equipped": equipped,
            "filter_type": filter_type,
            "attack_formula": atk_formula,
            "damage_formula": dmg_formula,
            "_is_magic": is_magic,
        })

    return equipment_list


def collect_spells():
    """Coleta magias do personagem."""
    print_header("MAGIAS")
    print("Adicione magias uma por vez. Digite 'fim' para terminar.\n")

    spells = []
    while True:
        name = ask("  Nome da magia em inglês (ou 'fim')")
        if name.lower() == "fim" or not name:
            break

        level = ask_int("  Nível (0 para cantrip)", 0)
        prepared = ask_yes_no("  Preparada?", True)
        usage = ask("  Uso (Truque, Slot de Magia, 1x/Descanso Longo, etc.)",
                     "Truque" if level == 0 else "Slot de Magia")

        spells.append({
            "name": name,
            "level": level,
            "prepared": prepared,
            "usage": usage,
        })

    return sorted(spells, key=lambda s: (s["level"], s["name"]))


def collect_extra_info():
    """Coleta informações extras (idiomas, avatar, etc.)."""
    print_header("INFORMAÇÕES ADICIONAIS")

    languages = ask("Idiomas (separados por vírgula)", "Common")
    senses_extra = ask("Sentidos extras (ex: Blindsight 10 ft.)", "")
    avatar = ask("URL ou caminho do avatar (ou vazio)", "")

    # Spell DC e ataque (se aplicável)
    has_spellcasting = ask_yes_no("O personagem tem habilidade de conjuração?", False)
    spell_dc = 0
    spell_attack_bonus = 0
    casting_stat = ""
    if has_spellcasting:
        casting_stat = ask_choice("Atributo de conjuração", [
            "int", "wis", "cha"
        ])

    return {
        "languages": languages,
        "senses_extra": senses_extra,
        "avatar": avatar,
        "has_spellcasting": has_spellcasting,
        "spell_dc": spell_dc,
        "spell_attack_bonus": spell_attack_bonus,
        "casting_stat": casting_stat,
    }


# ──────────────────────────────────────────────
# Sincronização com o compêndio
# ──────────────────────────────────────────────
def sync_compendium(basic, feats, equipment, spells):
    """Baixa entidades do 5e.tools para o compêndio local e retorna compendium_refs."""
    print_header("SINCRONIZANDO COMPÊNDIO")

    compendium_refs = []

    # Classe
    class_slug = slugify(basic["class_name"])
    class_ref = f"/compendium/classes/{class_slug}/"
    class_path = f"content{class_ref.rstrip('/')}.md"
    if os.path.exists(class_path):
        compendium_refs.append(class_ref)
    else:
        ref = fetch_from_5etools("class", basic["class_name"])
        if ref:
            compendium_refs.append(ref)

    # Subclasse
    if basic["subclass"]:
        sub_slug = slugify(basic["subclass"])
        sub_ref = f"/compendium/classes/{sub_slug}/"
        sub_path = f"content{sub_ref.rstrip('/')}.md"
        if os.path.exists(sub_path):
            compendium_refs.append(sub_ref)
        else:
            ref = fetch_from_5etools("subclass", basic["subclass"])
            if ref:
                compendium_refs.append(ref)

    # Classe overview com progressão
    class_data = fetch_class_json(basic["class_name"])
    if class_data:
        ensure_compendium_class_overview(basic["class_name"], class_data)
        if basic["subclass"]:
            ensure_compendium_class_overview(
                basic["class_name"], class_data, basic["subclass"]
            )

    # Raça
    race_slug = slugify(basic["race"])
    race_ref = f"/compendium/races/{race_slug}/"
    race_path = f"content{race_ref.rstrip('/')}.md"
    if os.path.exists(race_path):
        compendium_refs.append(race_ref)
    else:
        ref = fetch_from_5etools("race", basic["race"])
        if ref:
            compendium_refs.append(ref)

    # Talentos
    for feat in feats:
        feat_slug = slugify(feat)
        feat_ref = f"/compendium/feats/{feat_slug}/"
        feat_path = f"content{feat_ref.rstrip('/')}.md"
        if os.path.exists(feat_path):
            compendium_refs.append(feat_ref)
        else:
            ref = fetch_from_5etools("feat", feat)
            if ref:
                compendium_refs.append(ref)

    # Equipamentos
    item_aliases = {
        "leather": "leather armor",
        "studded leather": "studded leather armor",
        "scale mail": "scale mail armor",
        "ring mail": "ring mail armor",
        "plate": "plate armor",
        "hide": "hide armor",
        "padded": "padded armor",
        "chain mail": "chain mail armor",
        "splint": "splint armor",
    }
    for item in equipment:
        item_name = item["name"]
        is_magic = item.get("_is_magic", False)
        kind = "magic_item" if is_magic else "item"
        slug_prefix = "magic-items" if is_magic else "items"
        check_name = item_aliases.get(item_name.lower(), item_name)
        item_ref = f"/compendium/{slug_prefix}/{slugify(check_name)}/"
        item_path = f"content{item_ref.rstrip('/')}.md"
        if os.path.exists(item_path):
            compendium_refs.append(item_ref)
            item["ref"] = item_ref
        else:
            ref = fetch_from_5etools(kind, item_name)
            if ref:
                compendium_refs.append(ref)
                item["ref"] = ref

    # Magias
    for spell in spells:
        spell_slug = slugify(spell["name"])
        spell_ref = f"/compendium/spells/{spell_slug}/"
        spell_path = f"content{spell_ref.rstrip('/')}.md"
        if os.path.exists(spell_path):
            compendium_refs.append(spell_ref)
            spell["ref"] = spell_ref
        else:
            ref = fetch_from_5etools("spell", spell["name"])
            if ref:
                compendium_refs.append(ref)
                spell["ref"] = ref

    # Ações padrão
    for action_name, action_ref in STANDARD_ACTION_REFS.items():
        compendium_refs.append(action_ref)
        publish_compendium_page(action_ref)

    return sorted(list(set(compendium_refs)))


# ──────────────────────────────────────────────
# Geração do Markdown
# ──────────────────────────────────────────────
def generate_character_file(
    basic, stats, mods, combat, prof_data, feats, equipment,
    spells, extra, compendium_refs
):
    """Gera o arquivo Markdown do personagem com frontmatter YAML formatado."""

    slug = slugify(basic["name"])
    file_path = f"content/campaigns/{basic['campaign']}/characters/{slug}.md"

    prof_bonus = prof_data["prof_bonus"]

    # Classe completa string
    class_str = f"{basic['class_name']} {basic['level']}"
    if basic["subclass"]:
        class_str += f" ({basic['subclass']})"

    feat_str = ", ".join(feats) if feats else "Nenhum"

    # Sentidos
    senses_parts = [f"Passive Perception {prof_data['passive_senses']['perception']}"]
    if combat["darkvision"] > 0:
        senses_parts.append(f"Darkvision {combat['darkvision']} ft.")
    if extra["senses_extra"]:
        senses_parts.append(extra["senses_extra"])
    senses_str = ", ".join(senses_parts)

    # Spell DC e bônus de ataque
    spell_dc = extra["spell_dc"]
    spell_attack_bonus = extra["spell_attack_bonus"]
    if extra["has_spellcasting"] and extra["casting_stat"]:
        casting_mod = mods[extra["casting_stat"]]
        spell_dc = 8 + prof_bonus + casting_mod
        spell_attack_bonus = prof_bonus + casting_mod

    # Ações
    actions_data = []
    for action_name, action_ref in STANDARD_ACTION_REFS.items():
        actions_data.append({
            "name": action_name,
            "ref": action_ref,
            "max_uses": 0,
            "reset": "",
        })

    # Equipamentos (limpar campo interno _is_magic)
    equipment_clean = []
    for item in equipment:
        entry = {
            "name": item["name"],
            "quantity": item["quantity"],
            "equipped": item["equipped"],
            "filter_type": item["filter_type"],
            "attack_formula": item.get("attack_formula", ""),
            "damage_formula": item.get("damage_formula", ""),
        }
        if "ref" in item:
            entry["ref"] = item["ref"]
        equipment_clean.append(entry)

    # Spells formatados
    structured_spells = []
    for spell in spells:
        entry = {
            "name": spell["name"],
            "level": spell["level"],
            "prepared": spell["prepared"],
            "usage": spell["usage"],
        }
        if "ref" in spell:
            entry["ref"] = spell["ref"]
        structured_spells.append(entry)

    # Classes progression
    classes_data = [{
        "name": basic["class_name"],
        "level": basic["level"],
        "subclass": basic["subclass"],
    }]

    # Spells usage
    spells_usage = []
    for spell in spells:
        if spell["level"] > 0:
            spells_usage.append({
                "name": spell["name"],
                "usage": spell["usage"],
            })

    primary_class_slug = slugify(basic["class_name"])

    markdown = f"""---
title: {json.dumps(basic['name'])}
date: 2026-07-09T19:00:00Z
params:
  kind: "character"
draft: false
weight: 10
summary: "{basic['race']} {class_str} criado manualmente."
tags:
  - jogador
  - {slugify(basic['race'])}
  - {primary_class_slug}
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "{class_str}"
  race: "{basic['race']}"
  ac: "{combat['ac']}"
  hp: "{combat['hp']}"
  hp_max: "{combat['hp']}"
  hp_current: "{combat['hp']}"
  feat: "{feat_str}"
  size: "{basic['size']}"
  alignment: "{basic['alignment']}"
  dndbeyond_id: ""
  proficiency_bonus: {prof_bonus}
  spell_dc: {spell_dc}
  spell_attack_bonus: {spell_attack_bonus}
  avatar: "{extra['avatar']}"
  speed:
    walk: {combat['speeds']['walk']}
    fly: {combat['speeds']['fly']}
    swim: {combat['speeds']['swim']}
    climb: {combat['speeds']['climb']}
    burrow: {combat['speeds']['burrow']}
  senses: "{senses_str}"
  passive_senses:
    perception: {prof_data['passive_senses']['perception']}
    investigation: {prof_data['passive_senses']['investigation']}
    insight: {prof_data['passive_senses']['insight']}
  languages: "{extra['languages']}"
  saves:
    str: {prof_data['saves']['str']}
    dex: {prof_data['saves']['dex']}
    con: {prof_data['saves']['con']}
    int: {prof_data['saves']['int']}
    wis: {prof_data['saves']['wis']}
    cha: {prof_data['saves']['cha']}
  saves_proficient:
    str: {str(prof_data['proficient_saves']['str']).lower()}
    dex: {str(prof_data['proficient_saves']['dex']).lower()}
    con: {str(prof_data['proficient_saves']['con']).lower()}
    int: {str(prof_data['proficient_saves']['int']).lower()}
    wis: {str(prof_data['proficient_saves']['wis']).lower()}
    cha: {str(prof_data['proficient_saves']['cha']).lower()}
  saves_summary: "{prof_data['saves_summary']}"
  mods:
    str: {mods['str']}
    dex: {mods['dex']}
    con: {mods['con']}
    int: {mods['int']}
    wis: {mods['wis']}
    cha: {mods['cha']}
  stats:
    str: {stats['str']}
    dex: {stats['dex']}
    con: {stats['con']}
    int: {stats['int']}
    wis: {stats['wis']}
    cha: {stats['cha']}
  currencies:
    cp: 0
    sp: 0
    gp: 0
    ep: 0
    pp: 0
  skills:{dump_yaml_indented(prof_data['skills_data'], 4)}
  actions:{dump_yaml_indented(actions_data, 4)}
  equipment:{dump_yaml_indented(equipment_clean, 4)}
  spells:{dump_yaml_indented(structured_spells, 4)}
  classes_progression:{dump_yaml_indented(classes_data, 4)}

# Relacionamentos
locations: []
factions: []
compendium_refs:{dump_yaml_indented(compendium_refs, 0)}
spells_usage:{dump_yaml_indented(spells_usage, 0)}
---

### Biografia
Este personagem foi criado manualmente via script interativo.

### Equipamentos e Recursos
Consulte os itens e magias listados no frontmatter acima.
"""

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    return file_path


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Cria um personagem interativamente para o GM Vault."
    )
    parser.add_argument(
        "--campaign", type=str, default=None,
        help="Slug da campanha de destino."
    )
    parser.add_argument(
        "--interactive", "--menu", action="store_true",
        help="Abre o menu interativo Rich (se disponível)."
    )
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

    # Selecionar campanha
    if not args.campaign:
        campaigns_dir = "content/campaigns"
        if os.path.isdir(campaigns_dir):
            campaigns = sorted([
                d for d in os.listdir(campaigns_dir)
                if os.path.isdir(os.path.join(campaigns_dir, d))
            ])
            if campaigns:
                args.campaign = ask_choice(
                    "Selecione a campanha:", campaigns
                )
            else:
                args.campaign = ask("Slug da campanha")
        else:
            args.campaign = ask("Slug da campanha")

    if not args.campaign:
        print("ERRO: Campanha é obrigatória.", file=sys.stderr)
        sys.exit(1)

    print(f"\n📋 Campanha selecionada: {args.campaign}")

    # Coletar dados
    basic = collect_basic_info(args.campaign)
    stats, mods = collect_ability_scores()
    combat = collect_combat_info(mods, basic["level"], basic["class_name"])
    prof_data = collect_proficiencies(mods, basic["level"])
    feats = collect_feats()
    equipment = collect_equipment()
    spells = collect_spells()
    extra = collect_extra_info()

    # Sincronizar compêndio
    compendium_refs = sync_compendium(basic, feats, equipment, spells)

    # Gerar arquivo
    print_header("GERANDO PERSONAGEM")
    file_path = generate_character_file(
        basic, stats, mods, combat, prof_data, feats, equipment,
        spells, extra, compendium_refs
    )

    print(f"\n✅ Personagem criado com sucesso em: {file_path}")
    print(f"   Referências de compêndio: {len(compendium_refs)} entradas")
    print(f"\n   Teste com: hugo server -D")


if __name__ == "__main__":
    main()
