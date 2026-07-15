import urllib.request
import json
import os
import unicodedata
import re
import yaml


def dump_yaml_indented(data, indent=2):
    if not data:
        return "[]" if isinstance(data, list) else "{}"
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    prefix = " " * indent
    return "\n" + "\n".join(prefix + line for line in yaml_str.splitlines())

# Active community 5etools mirror URL for raw data
DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"

def get_modifier(score):
    return (score - 10) // 2

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

    if os.path.exists(dest_path):
        try:
            with open(dest_path, "r", encoding="utf-8") as handle:
                existing = handle.read()
            body = existing.split("---", 2)[-1].strip() if existing.startswith("---") else existing.strip()
            if body:
                return ref_path
        except OSError:
            return ref_path

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
        return None

    lines = [f"## Progressão de {title}", ""]
    seen = set()
    for feature in sorted(features, key=lambda item: (item.get("level", 0), item.get("name", ""))):
        name = feature.get("name")
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        feature_ref = f"/compendium/rules/{slugify(name)}/"
        feature_path = f"content{feature_ref.rstrip('/')}.md"
        if os.path.exists(feature_path):
            lines.append(f"- Nível {feature.get('level', 1)}: [{name}]({feature_ref})")
        else:
            lines.append(f"- Nível {feature.get('level', 1)}: {name}")

    markdown = f"""---
title: "{title}"
params:
  kind: "class"
draft: false
weight: 10
summary: "{summary}"
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
    if os.path.exists(dest_path_check):
        print(f"  [5e.tools] Encontrado localmente: {dest_path_check}")
        if kind == "magic_item":
            return f"/compendium/magic-items/{slug_check}/"
        elif kind in ["class", "subclass"]:
            return f"/compendium/classes/{slug_check}/"
        elif kind == "item_mastery":
            return f"/compendium/rules/{slug_check}/"
        elif kind == "race" or kind == "species":
            return f"/compendium/species/{slug_check}/"
        else:
            return f"/compendium/{kind}s/{slug_check}/"
    
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
params:
  kind: "species"
draft: true
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
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

    elif kind == "item_mastery":
        markdown = f"""---
title: "Maestria de Arma: {english_name}"
params:
  kind: "rule"
draft: true
weight: 10
summary: "Propriedade de Maestria de Arma do D&D 2024 (XPHB). Requires translation."
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
