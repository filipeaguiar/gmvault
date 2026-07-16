import urllib.request
import json
import os
import unicodedata
import re
import yaml


def dump_yaml_indented(data, indent=2):
    if not data:
        return " []" if isinstance(data, list) else " {}"
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
params:
  kind: "rule"
draft: false
weight: 10
summary: "Característica de classe: {name}."
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

def load_background_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = DATA_BASE_URL + "backgrounds.json"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  [5e.tools] Erro ao carregar backgrounds.json: {e}")
        return None

def load_item_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = DATA_BASE_URL + "items.json"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  [5e.tools] Erro ao carregar items.json: {e}")
        return None

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
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = DATA_BASE_URL + "items-base.json"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            base_data = json.loads(response.read().decode())
    except Exception:
        base_data = {"item": []}

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
    if os.path.exists(dest_path_check) and kind not in {"item", "magic_item"}:
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
draft: false
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
params:
  kind: "{kind}"
draft: false
weight: 10
summary: "Draft imported from 5e.tools. Requires translation."
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
params:
  kind: "feat"
draft: false
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
draft: false
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
draft: false
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
draft: false
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
draft: false
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
        if kind in {"item", "magic_item"} and os.path.exists(dest_path):
            if not update_frontmatter_field(dest_path, "item_info", item_info_data):
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
