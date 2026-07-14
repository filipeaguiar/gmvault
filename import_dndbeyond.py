#!/usr/bin/env python3
import urllib.request
import json
import os
import sys
import argparse

# Active community 5etools mirror URL for raw data
DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"

def get_modifier(score):
    return (score - 10) // 2

def slugify(text):
    import unicodedata
    import re
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '', text.replace(' ', '-'))
    return text

def clean_5etools_tags(text):
    import re
    # Clean tags like {@status surprised} -> surprised, or {@spell fireball|Bola de Fogo} -> Bola de Fogo
    def repl(match):
        val = match.group(2)
        label = match.group(3)
        # Handle cases where label is like 'some label' or just empty
        if label:
            # If label has pipes, get the last segment
            if '|' in label:
                return label.split('|')[-1]
            return label
        return val
    cleaned = re.sub(r'\{@(\w+) ([^\|\}]+)(?:\|([^\}]+))?\}', repl, text)
    return cleaned

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

def fetch_class_json(class_name):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url_index = DATA_BASE_URL + "class/index.json"
    try:
        req = urllib.request.Request(url_index, headers=headers)
        with urllib.request.urlopen(req) as response:
            class_index = json.loads(response.read().decode())
        class_key = class_name.lower()
        filename = class_index.get(class_key)
        if not filename:
            for k, f in class_index.items():
                if k in class_key or class_key in k:
                    filename = f
                    break
        if filename:
            url_class = DATA_BASE_URL + "class/" + filename
            req = urllib.request.Request(url_class, headers=headers)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
    except Exception as e:
        print(f"  [5e.tools] Erro ao carregar dados de classe para {class_name}: {e}")
    return None

def fetch_from_5etools(kind, english_name):
    slug = slugify(english_name)
    print(f"  [5e.tools] Tentando baixar '{english_name}' ({kind})...")
    
    file_map = {
        "spell": ["spells/spells-phb.json", "spells/spells-xge.json", "spells/spells-tce.json"],
        "item": ["items.json", "items-base.json"],
        "magic_item": ["items.json", "items-base.json"],
        "feat": ["feats.json"],
        "race": ["races.json"],
        "class": ["classes.json"]
    }
    
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
    if kind in ["item", "magic_item"] and english_name.lower() in item_aliases:
        search_names.append(item_aliases[english_name.lower()])
        
    found_data = None
    headers = {'User-Agent': 'Mozilla/5.0'}

    if kind == "class":
        url_index = DATA_BASE_URL + "class/index.json"
        try:
            req = urllib.request.Request(url_index, headers=headers)
            with urllib.request.urlopen(req) as response:
                class_index = json.loads(response.read().decode())
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
            req = urllib.request.Request(url_index, headers=headers)
            with urllib.request.urlopen(req) as response:
                class_index = json.loads(response.read().decode())
            files = ["class/" + f for f in class_index.values()]
        except Exception as e:
            print(f"  [5e.tools] Erro ao carregar index de classes: {e}")
            files = []
    
    for file_path in files:
        url = DATA_BASE_URL + file_path
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
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
                    if item.get("name", "").lower() == english_name.lower():
                        found_data = item
                        break
            elif kind == "race" and "race" in data:
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
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                    
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
    elif kind in ["class", "subclass"]:
        content_dir = "content/compendium/classes"
        
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
                
        markdown = f"""---
title: "{english_name}"
params:
  kind: "spell"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

spell_info:
  level: "{level_str}"
  school: "{school_str}"
  cast_time: "{cast_time}"
  range: "{range_str}"
  components: "{components_str}"
  duration: "{duration_str}"
---

{description}
"""

    elif kind == "item" or kind == "magic_item":
        item_type = found_data.get("type", "G")
        type_map = {"G": "Adventuring Gear", "LA": "Light Armor", "MA": "Medium Armor", "HA": "Heavy Armor", "S": "Shield", "R": "Ring", "W": "Weapon", "P": "Potion", "SC": "Scroll"}
        item_type_str = type_map.get(item_type, "Adventuring Gear")
        
        cost_gp = f"{found_data.get('value', 0) / 100} gp" if found_data.get('value') else "—"
        weight_str = f"{found_data.get('weight', 0)} lb" if found_data.get('weight') else "—"
        rarity = found_data.get("rarity", "common").title()
        attunement = "Requires attunement" if found_data.get("reqAttune") else ""
        
        if kind == "magic_item":
            markdown = f"""---
title: "{english_name}"
params:
  kind: "magic_item"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

item_info:
  type: "{item_type_str}"
  rarity: "{rarity}"
  attunement: "{attunement}"
  weight: "{weight_str}"
  cost: "{cost_gp}"
---

{description}
"""
        else:
            markdown = f"""---
title: "{english_name}"
params:
  kind: "item"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

item_info:
  type: "{item_type_str}"
  cost: "{cost_gp}"
  weight: "{weight_str}"
  properties: ""
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
params:
  kind: "feat"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
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

    elif kind == "race":
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
params:
  kind: "race"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
tags:
  - draft
  - importado
visibility: "public"
status: "draft"

race_info:
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
params:
  kind: "class"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
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
params:
  kind: "class"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
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

    if markdown:
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"  [5e.tools] SUCESSO: Arquivo de compêndio criado em: {dest_path}")
        if kind == "magic_item":
            return f"/compendium/magic-items/{slug}/"
        elif kind in ["class", "subclass"]:
            return f"/compendium/classes/{slug}/"
        else:
            return f"/compendium/{kind}s/{slug}/"
        
    return None


def main():
    parser = argparse.ArgumentParser(description="Importa um personagem do D&D Beyond para a wiki estática Hugo.")
    parser.add_argument("char_id", type=str, nargs="?", help="O ID do personagem do D&D Beyond (ex: 168106464)")
    parser.add_argument("--campaign", type=str, default="cidadela-radiante", help="O slug da campanha de destino (padrão: cidadela-radiante)")
    parser.add_argument("--interactive", "--menu", action="store_true", help="Abre o menu interativo Rich.")
    
    args = parser.parse_args()

    if args.interactive:
        from interactive_cli import dndbeyond_menu

        values = dndbeyond_menu()
        if values is None:
            print("Operação cancelada.")
            return
        args.char_id = values["char_id"]
        args.campaign = values["campaign"]
    elif not args.char_id:
        parser.error("o argumento char_id é obrigatório, exceto com --interactive/--menu")
    
    url = f"https://character-service.dndbeyond.com/character/v5/character/{args.char_id}"
    print(f"Buscando dados da API do D&D Beyond para o personagem ID: {args.char_id}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            payload = json.loads(response.read().decode())
            
        char = payload.get("data")
        if not char:
            print("ERRO: Resposta inválida da API ou personagem não encontrado/privado.", file=sys.stderr)
            sys.exit(1)
            
        char_name = char.get("name")
        print(f"Personagem encontrado: {char_name}!")
        
        # 1. Atributos Base e cálculo final com modificadores
        stats_base = {s['id']: s['value'] for s in char.get('stats', [])}
        stat_names = {1: 'str', 2: 'dex', 3: 'con', 4: 'int', 5: 'wis', 6: 'cha'}
        stats_final = {stat_names[i]: stats_base[i] for i in stat_names}
        
        modifiers = char.get('modifiers', {})
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus':
                    subtype = item.get('subType', '')
                    val = item.get('value')
                    if val is not None:
                        for stat_id, sname in stat_names.items():
                            if sname in subtype:
                                stats_final[sname] += int(val)
                                
        # Modificadores finais calculados
        dex_mod = get_modifier(stats_final['dex'])
        wis_mod = get_modifier(stats_final['wis'])
        con_mod = get_modifier(stats_final['con'])
        
        # 2. Classes e Nível Total
        classes_list = []
        total_level = 0
        is_monk = False
        is_barbarian = False
        primary_class_slug = ""
        primary_class_name = ""
        
        for cls in char.get('classes', []):
            cls_def = cls.get('definition', {})
            cls_name = cls_def.get('name')
            cls_level = cls.get('level', 1)
            total_level += cls_level
            subcls_def = cls.get('subclassDefinition')
            if subcls_def:
                subcls_name = subcls_def.get('name')
                classes_list.append(f"{cls_name} {cls_level} ({subcls_name})")
            else:
                classes_list.append(f"{cls_name} {cls_level}")
            
            if cls_name == "Monk":
                is_monk = True
            elif cls_name == "Barbarian":
                is_barbarian = True
                
            if cls.get('isStartingClass'):
                primary_class_slug = slugify(cls_name)
                primary_class_name = cls_name
                
        class_str = " / ".join(classes_list)
        if not primary_class_slug and classes_list:
            primary_class_name = char.get('classes')[0].get('definition', {}).get('name')
            primary_class_slug = slugify(primary_class_name)
            
        # 3. Raça e Sub-raça
        race_data = char.get('race', {})
        race_fullname = race_data.get('fullName', "Desconhecida")
        race_basename = race_data.get('baseName', race_fullname)
        race_slug = slugify(race_basename)
        
        # Tamanho e Alinhamento
        SIZE_MAP = {
            1: "Tiny",
            2: "Tiny",
            3: "Small",
            4: "Medium",
            5: "Large",
            6: "Huge",
            7: "Gargantuan"
        }
        ALIGNMENT_MAP = {
            1: "Lawful Good",
            2: "Neutral Good",
            3: "Chaotic Good",
            4: "Lawful Neutral",
            5: "True Neutral",
            6: "Chaotic Neutral",
            7: "Lawful Evil",
            8: "Neutral Evil",
            9: "Chaotic Evil"
        }

        alignment_val = char.get('alignmentId')
        char_alignment = ALIGNMENT_MAP.get(alignment_val, "Neutral")

        size_val = race_data.get('sizeId') or char.get('sizeId')
        char_size = SIZE_MAP.get(size_val, "Medium")

        # Velocidades de movimento
        race_speeds = race_data.get('weightSpeeds', {}).get('normal', {})
        char_speeds = {
            "walk": race_speeds.get('walk', 30),
            "fly": race_speeds.get('fly', 0),
            "swim": race_speeds.get('swim', 0),
            "climb": race_speeds.get('climb', 0),
            "burrow": race_speeds.get('burrow', 0)
        }

        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus':
                    subtype = item.get('subType', '')
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        val = int(val)
                        if subtype == 'unarmored-movement' or subtype == 'speed' or subtype == 'speed-walk' or 'walk-speed' in subtype:
                            char_speeds['walk'] += val
                        elif 'fly-speed' in subtype or subtype == 'speed-fly':
                            char_speeds['fly'] += val
                        elif 'swim-speed' in subtype or subtype == 'speed-swim':
                            char_speeds['swim'] += val
                        elif 'climb-speed' in subtype or subtype == 'speed-climb':
                            char_speeds['climb'] += val
                        elif 'burrow-speed' in subtype or subtype == 'speed-burrow':
                            char_speeds['burrow'] += val

        custom_speeds = char.get('customSpeeds', [])
        if custom_speeds:
            speed_map = {1: "walk", 2: "fly", 3: "swim", 4: "climb", 5: "burrow"}
            for cs in custom_speeds:
                sid = cs.get('speedId')
                dist = cs.get('distance')
                if sid in speed_map and dist is not None:
                    char_speeds[speed_map[sid]] = int(dist)

        # Salvamentos (Saving Throws)
        prof_bonus = (total_level - 1) // 4 + 2
        stat_names_save = {
            'str': 'strength',
            'dex': 'dexterity',
            'con': 'constitution',
            'int': 'intelligence',
            'wis': 'wisdom',
            'cha': 'charisma'
        }

        char_saves = {s: get_modifier(stats_final[s]) for s in stat_names_save}
        proficient_saves = {s: False for s in stat_names_save}

        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'proficiency':
                    subtype = item.get('subType', '')
                    for s, full_name in stat_names_save.items():
                        if subtype == f"{full_name}-saving-throws":
                            proficient_saves[s] = True

        for s in char_saves:
            if proficient_saves[s]:
                char_saves[s] += prof_bonus

        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus':
                    subtype = item.get('subType', '')
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        val = int(val)
                        if subtype == 'saving-throws':
                            for s in char_saves:
                                char_saves[s] += val
                        else:
                            for s, full_name in stat_names_save.items():
                                if subtype == f"{full_name}-saving-throws":
                                    char_saves[s] += val

        saves_summary_list = []
        for s in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            if proficient_saves[s]:
                val = char_saves[s]
                sign = "+" if val >= 0 else ""
                saves_summary_list.append(f"{s.capitalize()} {sign}{val}")
        char_saves_summary = ", ".join(saves_summary_list)

        # Sentidos (Senses)
        darkvision = 0
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'set-base' and item.get('subType') == 'darkvision':
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        darkvision = max(darkvision, int(val))

        is_proficient_perception = False
        has_expertise_perception = False
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('subType') == 'perception':
                    if item.get('type') == 'proficiency':
                        is_proficient_perception = True
                    elif item.get('type') == 'expertise':
                        has_expertise_perception = True

        passive_perception_bonus = 0
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus' and item.get('subType') == 'passive-perception':
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        passive_perception_bonus += int(val)

        passive_perception = 10 + wis_mod + passive_perception_bonus
        if has_expertise_perception:
            passive_perception += 2 * prof_bonus
        elif is_proficient_perception:
            passive_perception += prof_bonus

        senses_list = [f"Passive Perception {passive_perception}"]
        if darkvision > 0:
            senses_list.append(f"Darkvision {darkvision} ft.")
        char_senses = ", ".join(senses_list)

        # Idiomas (Languages)
        languages_list = []
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'language':
                    lang_name = item.get('friendlySubtypeName')
                    if lang_name and lang_name not in languages_list:
                        languages_list.append(lang_name)
        char_languages = ", ".join(sorted(languages_list))
        
        # 4. Cálculo do HP Máximo
        base_hp = char.get('baseHitPoints', 10)
        bonus_hp = char.get('bonusHitPoints') or 0
        final_hp = base_hp + (con_mod * total_level) + bonus_hp
        
        # 5. Cálculo da CA (Classe de Armadura)
        has_armor = False
        has_shield = False
        armor_ac = 10
        shield_ac = 0
        armor_type = None
        equipped_items_names = []
        
        for item in char.get('inventory', []):
            d = item.get('definition', {})
            if item.get('equipped'):
                equipped_items_names.append((d.get('name'), d.get('magic'), d.get('filterType')))
                
            if not item.get('equipped'):
                continue
            filter_type = d.get('filterType')
            if filter_type == 'Armor':
                ac_val = d.get('armorClass', 0)
                armor_type_id = d.get('armorTypeId', 0)
                if armor_type_id == 4: # Escudo
                    has_shield = True
                    shield_ac = ac_val
                else: # Armadura Leve, Média ou Pesada
                    has_armor = True
                    armor_ac = ac_val
                    armor_type = armor_type_id
                    
        # Algoritmo de CA
        if has_armor:
            if armor_type == 1: # Leve
                base_ac = armor_ac + dex_mod
            elif armor_type == 2: # Média
                base_ac = armor_ac + min(dex_mod, 2)
            else: # Pesada
                base_ac = armor_ac
        else:
            # Defesa Sem Armadura
            if is_monk and not has_shield:
                base_ac = 10 + dex_mod + wis_mod
            elif is_barbarian:
                base_ac = 10 + dex_mod + con_mod
            else:
                base_ac = 10 + dex_mod
                
        final_ac = base_ac + shield_ac
        
        # Bônus mágicos de CA do inventário
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus' and item.get('subType') == 'armor-class':
                    val = item.get('value')
                    if val is not None:
                        final_ac += int(val)
                        
        # 6. Talentos
        feats_list = []
        for feat_item in char.get('feats', []):
            f_name = feat_item.get('definition', {}).get('name', '')
            if f_name not in ["Dark Bargain", "Character Threads", "Runestones"]:
                feats_list.append(f_name)
        feat_str = ", ".join(feats_list) if feats_list else "Nenhum"
        
        # 7. Magias Conhecidas e seus detalhes de uso
        spells_list = []
        spells_usage_map = {}
        
        def get_spell_usage_str(s):
            s_def = s.get('definition', {})
            level = s_def.get('level', 0)
            if level == 0:
                return "Truque"
                
            is_ritual = s_def.get('ritual', False)
            uses_slot = s.get('usesSpellSlot', True)
            
            # Checar limites de uso (feats / items)
            lim = s.get('limitedUse')
            if lim and isinstance(lim, dict) and lim.get('maxUses'):
                max_u = lim.get('maxUses')
                reset = lim.get('resetType')
                reset_str = "Descanso Longo" if reset == 2 else "Descanso Curto" if reset == 1 else "Dia"
                return f"{max_u}x/{reset_str}"
                
            if is_ritual:
                if uses_slot:
                    return "Slot / Ritual"
                else:
                    return "Ritual"
                    
            if uses_slot:
                return "Slot de Magia"
                
            return "Especial"

        for class_spell_obj in char.get('classSpells', []):
            if isinstance(class_spell_obj, dict):
                slist = class_spell_obj.get('spells', [])
                if slist:
                    for s in slist:
                        s_def = s.get('definition', {})
                        if s_def and s_def.get('name'):
                            name = s_def.get('name')
                            spells_list.append(name)
                            spells_usage_map[name] = get_spell_usage_str(s)
                            
        # Adicionar outras fontes de magias (race, class, feat, item, background)
        other_spells = char.get('spells', {})
        if isinstance(other_spells, dict):
            for source, slist in other_spells.items():
                if slist:
                    for s in slist:
                        s_def = s.get('definition', {})
                        if s_def and s_def.get('name'):
                            name = s_def.get('name')
                            spells_list.append(name)
                            spells_usage_map[name] = get_spell_usage_str(s)
                            
        # Remove duplicatas
        spells_list = sorted(list(set(spells_list)))
                
        # 8. Resolver Compêndio Refs
        compendium_refs = []
        
        # Entidades que precisamos garantir no Compêndio
        entities_to_check = []
        
        # Classe principal
        entities_to_check.append(("class", primary_class_name, f"/compendium/classes/{primary_class_slug}/"))
        # Raça
        entities_to_check.append(("race", race_basename, f"/compendium/races/{race_slug}/"))
        # Subclasses
        for cls in char.get('classes', []):
            subcls_def = cls.get('subclassDefinition')
            if subcls_def:
                subcls_name = subcls_def.get('name')
                entities_to_check.append(("subclass", subcls_name, f"/compendium/classes/{slugify(subcls_name)}/"))
        # Talentos
        for feat in feats_list:
            entities_to_check.append(("feat", feat, f"/compendium/feats/{slugify(feat)}/"))
        # Itens Equipados
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
        for item_name, is_magic, filter_type in equipped_items_names:
            if filter_type in ['Weapon', 'Armor', 'Wondrous item', 'Ring', 'Potion', 'Scroll']:
                kind = "magic_item" if is_magic else "item"
                slug_prefix = "magic-items" if is_magic else "items"
                check_name = item_name
                if item_name.lower() in item_aliases:
                    check_name = item_aliases[item_name.lower()]
                entities_to_check.append((kind, item_name, f"/compendium/{slug_prefix}/{slugify(check_name)}/"))
        # Magias
        for spell_name in spells_list:
            entities_to_check.append(("spell", spell_name, f"/compendium/spells/{slugify(spell_name)}/"))
            
        # Checar se existem localmente, senão baixar do 5e.tools
        for kind, eng_name, ref in entities_to_check:
            content_path = "content" + ref.rstrip('/') + ".md"
            folder_path = "content" + ref + "_index.md"
            
            if os.path.exists(content_path) or os.path.exists(folder_path):
                compendium_refs.append(ref)
            else:
                # O item não existe localmente! Tenta buscar e criar do 5e.tools
                new_ref = fetch_from_5etools(kind, eng_name)
                if new_ref:
                    compendium_refs.append(new_ref)
                    
        # Remove duplicatas nas referências
        compendium_refs = sorted(list(set(compendium_refs)))
        
        # Preparar spells_usage para o front matter
        yaml_spells_usage = []
        for name in sorted(spells_usage_map.keys()):
            yaml_spells_usage.append({
                "name": name,
                "usage": spells_usage_map[name]
            })
            
        # Função para garantir a criação da regra no compêndio
        def ensure_compendium_rule(name, description):
            # Limpar indentações no início de cada linha que geram blocos de código em markdown
            cleaned_lines = []
            for line in description.split('\n'):
                stripped = line.strip()
                if stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('+') or stripped.startswith('o'):
                    cleaned_lines.append(stripped)
                else:
                    cleaned_lines.append(line.lstrip(' \t'))
            description = '\n'.join(cleaned_lines)
            
            slug = slugify(name)
            ref_path = f"/compendium/rules/{slug}/"
            dest_path = f"content/compendium/rules/{slug}.md"
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            markdown = f"""---
title: "{name}"
params:
  kind: "rule"
draft: true
status: "draft"
summary: "Habilidade de classe."
---

{description}
"""
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"  [Compêndio] Habilidade de classe atualizada/criada: {dest_path}")
            return ref_path

        # 10. Coletar e criar opções customizadas de classe (Pactos e Invocações) no Compêndio
        class_opts = char.get('options', {}).get('class', [])
        if isinstance(class_opts, list):
            for opt in class_opts:
                if isinstance(opt, dict):
                    opt_def = opt.get('definition', {})
                    if opt_def:
                        opt_name = opt_def.get('name')
                        opt_snippet = opt_def.get('snippet', '') or opt_def.get('description', '')
                        if opt_name and opt_snippet:
                            clean_snippet = clean_5etools_tags(opt_snippet.replace('<em>', '').replace('</em>', '').replace('<p>', '').replace('</p>', '\n').replace('<br>', '\n'))
                            ref = ensure_compendium_rule(opt_name, clean_snippet.strip())
                            compendium_refs.append(ref)
            
        # 11. Coletar e criar habilidades de classe e subclasse a partir do 5e.tools no Compêndio
        feature_blacklist = [
            "core bard traits", "core warlock traits", "core fighter traits", 
            "core rogue traits", "core barbarian traits", "core monk traits",
            "core sorcerer traits", "core wizard traits", "core cleric traits",
            "core druid traits", "core paladin traits", "core ranger traits",
            "ability score improvement", "ability score increase", "bard subclass",
            "warlock subclass", "subclass options", "bonus proficiency",
            "roguish archetype", "subclass feature", "roguish archetype feature",
            "sorcerous origin", "monastic tradition", "primal path", "bard college",
            "cleric domain", "druid circle", "martial archetype", "sacred oath",
            "ranger archetype", "arcane tradition", "subclass", "rogue subclass",
            "sorcerer subclass", "barbarian subclass", "fighter subclass",
            "monk subclass", "warlock subclass", "wizard subclass", "cleric subclass",
            "druid subclass", "paladin subclass", "ranger subclass"
        ]

        for cl in char.get('classes', []):
            cls_def = cl.get('definition', {})
            class_name = cls_def.get('name')
            class_level = cl.get('level', 1)
            subcls_def = cl.get('subclassDefinition')
            subclass_name = subcls_def.get('name') if subcls_def else None
            
            class_data = fetch_class_json(class_name)
            if not class_data:
                continue
                
            raw_features = []
            # Coletar classFeature
            for f in class_data.get('classFeature', []):
                if f.get('className', '').lower() == class_name.lower() and f.get('level', 1) <= class_level:
                    raw_features.append(f)
                    
            # Coletar subclassFeature se houver subclasse
            if subclass_name:
                for sf in class_data.get('subclassFeature', []):
                    if sf.get('className', '').lower() == class_name.lower() and sf.get('level', 1) <= class_level:
                        sf_sc_name = sf.get('subclassShortName', '')
                        if sf_sc_name.lower() == subclass_name.lower() or subclass_name.lower() in sf.get('subclassShortName', '').lower() or sf_sc_name.lower() in subclass_name.lower():
                            raw_features.append(sf)
            
            # Ordenar por prioridade de fonte (XPHB > PHB > outras) para sobrescrever com versões mais novas
            def get_source_priority(item):
                source = item.get("source", "")
                if source == "XPHB":
                    return 2
                if source == "PHB":
                    return 1
                return 0
                
            raw_features.sort(key=get_source_priority)
            
            # Filtrar duplicados pelo nome (mantendo o de maior prioridade de fonte)
            features_dict = {}
            for f in raw_features:
                name = f.get('name')
                if name:
                    features_dict[name.lower()] = f
                    
            # Criar as regras
            for name_lower, f in features_dict.items():
                name = f.get('name')
                if name.lower() in feature_blacklist:
                    continue
                    
                entries = f.get('entries', [])
                if not entries:
                    continue
                    
                description = parse_entries(entries)
                if not description or not description.strip():
                    continue
                    
                ref = ensure_compendium_rule(name, description.strip())
                compendium_refs.append(ref)

        # Remove duplicatas nas referências
        compendium_refs = sorted(list(set(compendium_refs)))
            
        # 9. Montar conteúdo Markdown
        slug = slugify(char_name)
        slug_map = {
            "perwinkle-pinky-pirata": "pinky",
            "nyx-": "nyxclair"
        }
        title_map = {
            "pinky": "Pinky",
            "nyxclair": "Nyx'Clair"
        }
        if slug in slug_map:
            slug = slug_map[slug]
        
        display_title = char_name
        if slug in title_map:
            display_title = title_map[slug]
            
        file_path = f"content/campaigns/{args.campaign}/characters/{slug}.md"
        
        markdown = f"""---
title: {json.dumps(display_title)}
date: 2026-07-09T19:00:00Z
params:
  kind: "character"
draft: false
weight: 10
summary: "{race_fullname} {class_str} importado do D&D Beyond."
tags:
  - jogador
  - {race_basename.lower()}
  - {primary_class_slug}
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "{class_str}"
  race: "{race_fullname}"
  ac: "{final_ac}"
  hp: "{final_hp}"
  feat: "{feat_str}"
  size: "{char_size}"
  alignment: "{char_alignment}"
  dndbeyond_id: "{args.char_id}"
  speed:
    walk: {char_speeds['walk']}
    fly: {char_speeds['fly']}
    swim: {char_speeds['swim']}
    climb: {char_speeds['climb']}
    burrow: {char_speeds['burrow']}
  senses: "{char_senses}"
  languages: "{char_languages}"
  saves:
    str: {char_saves['str']}
    dex: {char_saves['dex']}
    con: {char_saves['con']}
    int: {char_saves['int']}
    wis: {char_saves['wis']}
    cha: {char_saves['cha']}
  saves_summary: "{char_saves_summary}"
  stats:
    str: {stats_final['str']}
    dex: {stats_final['dex']}
    con: {stats_final['con']}
    int: {stats_final['int']}
    wis: {stats_final['wis']}
    cha: {stats_final['cha']}

# Relacionamentos
locations: []
factions: []
compendium_refs: {json.dumps(compendium_refs)}
spells_usage: {json.dumps(yaml_spells_usage)}
---

### Biografia
Este personagem foi importado automaticamente do D&D Beyond. 

### Equipamentos e Recursos
Acesse a ficha completa original no D&D Beyond para acompanhar o inventário de itens e slots de magia em tempo real.
"""
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)
            
        print(f"SUCESSO: Ficha do personagem criada com sucesso em: {file_path}")
        
    except Exception as e:
        print(f"ERRO: Falha ao processar ou importar o personagem. Detalhes: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
