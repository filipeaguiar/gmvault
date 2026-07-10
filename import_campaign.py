#!/usr/bin/env python3
import urllib.request
import json
import os
import sys
import re
import unicodedata
import argparse
import urllib.parse

DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"
IMG_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/master/"

# Lista de fontes conhecidas do D&D para ignorar se aparecerem como argumento de exibição nas tags
KNOWN_SOURCES = {
    "phb", "mm", "dmg", "scag", "vgm", "xge", "toa", "mtof", "tcoe", "vrgr", 
    "jttrc", "cos", "erlw", "wbw", "bgdia", "idrotf", "lmop", "oota", "typt", 
    "ggr", "ftd", "scc", "aag", "bam", "dltso", "pactc", "sat", "bmt", "kftgv"
}

# Cache global para bestiários de outros livros
OTHER_BESTIARY_CACHE = {}

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '', text.replace(' ', '-'))
    return text

def format_dice_rolls(text):
    def dice_repl(match):
        formula = match.group(1).replace(" ", "")
        return f"[[{formula}]]"
    pattern = r'(?<!\[\[)\b(\d+d\d+(?:\s*[\+\-]\s*\d+)?)\b(?!\]\])'
    return re.sub(pattern, dice_repl, text)

def get_monster_from_source(monster_name, source_book):
    source_book = source_book.lower()
    
    if source_book in OTHER_BESTIARY_CACHE:
        return OTHER_BESTIARY_CACHE[source_book].get(monster_name.lower())
        
    print(f"  [5e.tools] Baixando bestiário complementar: {source_book.upper()}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    url_bestiary = DATA_BASE_URL + f"bestiary/bestiary-{source_book}.json"
    url_fluff = DATA_BASE_URL + f"bestiary/fluff-bestiary-{source_book}.json"
    
    monsters_list = []
    fluff_list = []
    
    try:
        req = urllib.request.Request(url_bestiary, headers=headers)
        with urllib.request.urlopen(req) as r:
            bestiary_json = json.loads(r.read().decode())
            monsters_list = bestiary_json.get("monster", [])
    except Exception as e:
        OTHER_BESTIARY_CACHE[source_book] = {}
        return None
        
    try:
        req = urllib.request.Request(url_fluff, headers=headers)
        with urllib.request.urlopen(req) as r:
            fluff_json = json.loads(r.read().decode())
            fluff_list = fluff_json.get("monsterFluff", [])
    except Exception as e:
        pass
        
    fluff_by_name = {f.get("name").lower(): f for f in fluff_list}
    
    book_data = {}
    for m in monsters_list:
        name = m.get("name")
        fluff = fluff_by_name.get(name.lower())
        book_data[name.lower()] = {
            "stats": m,
            "fluff": fluff
        }
        
    OTHER_BESTIARY_CACHE[source_book] = book_data
    return book_data.get(monster_name.lower())

def extract_fluff_images(fluff):
    if not fluff:
        return []
    images = []
    if "images" in fluff:
        for img in fluff["images"]:
            if isinstance(img, dict) and "href" in img:
                path = img["href"].get("path")
                if path:
                    images.append(path)
    return images

def parse_5etools_tag(tag_name, inner_text, target_slug, ctx):
    args = inner_text.split('|')
    default_val = args[0]
    
    # 1. Tags de Criaturas e Monstros
    if tag_name in ["monster", "creature"]:
        source = "mm"
        display_name = default_val
        
        if len(args) > 1:
            last_arg = args[-1]
            if last_arg.lower() in KNOWN_SOURCES:
                source = last_arg.lower()
                display_name = default_val
            elif len(args) > 2 and args[1].lower() in KNOWN_SOURCES:
                source = args[1].lower()
                display_name = args[2]
            else:
                display_name = last_arg
                source = args[1].lower() if len(args) > 1 else "mm"
        
        # Se for da própria campanha
        if source.lower() == target_slug.lower():
            c_slug = slugify(default_val)
            ctx["campaign_creatures"].add((c_slug, default_val))
            return display_name
            
        # Monstro geral do compêndio
        monster_slug = slugify(default_val)
        ctx["monsters"].add((monster_slug, default_val, source))
        return display_name
        
    # 2. Tags de Itens
    elif tag_name == "item":
        source = "phb"
        display_name = default_val
        
        if len(args) > 1:
            last_arg = args[-1]
            if last_arg.lower() in KNOWN_SOURCES:
                source = last_arg.lower()
                display_name = default_val
            elif len(args) > 2 and args[1].lower() in KNOWN_SOURCES:
                source = args[1].lower()
                display_name = args[2]
            else:
                display_name = last_arg
                source = args[1].lower() if len(args) > 1 else "phb"
                
        # Se for da própria campanha
        if source.lower() == target_slug.lower():
            i_slug = slugify(default_val)
            ctx["campaign_items"].add((i_slug, default_val))
            return display_name
            
        # Item de compêndio padrão
        item_slug = slugify(default_val)
        ctx["items"].add(item_slug)
        return display_name
        
    # 3. Tags de Magias
    elif tag_name == "spell":
        source = "phb"
        display_name = default_val
        
        if len(args) > 1:
            last_arg = args[-1]
            if last_arg.lower() in KNOWN_SOURCES:
                source = last_arg.lower()
                display_name = default_val
            elif len(args) > 2 and args[1].lower() in KNOWN_SOURCES:
                source = args[1].lower()
                display_name = args[2]
            else:
                display_name = last_arg
                source = args[1].lower() if len(args) > 1 else "phb"
                
        spell_slug = slugify(default_val)
        ctx["spells"].add(spell_slug)
        return display_name
        
    elif tag_name == "area":
        return default_val
        
    elif tag_name == "dc":
        return f"CD {default_val}"
        
    # Fallback genérico para as outras tags
    if len(args) > 1:
        last_arg = args[-1]
        if last_arg.lower() not in KNOWN_SOURCES:
            return last_arg
            
    return default_val

def clean_5etools_tags(text, campaign_slug, target_slug, ctx):
    def dice_tag_repl(match):
        formula = match.group(2).split('|')[0].replace(" ", "")
        return f"[[{formula}]]"
    
    text = re.sub(r'\{@(dice|damage) ([^\}]+)\}', dice_tag_repl, text)
    
    # Substituir tags simples de estilo
    text = re.sub(r'\{@i ([^\}]+)\}', r'*\1*', text)
    text = re.sub(r'\{@b ([^\}]+)\}', r'**\1**', text)
    text = re.sub(r'\{@note ([^\}]+)\}', r'> **Nota:** \1', text)
    text = re.sub(r'\{@hit ([^\}]+)\}', r'\1', text)
    text = re.sub(r'\{@chance ([^\}]+)\}', r'\1%', text)
    
    # Substituir links
    def link_repl(match):
        url = match.group(1)
        label = match.group(2)
        if label:
            return f"[{label}]({url})"
        return url
    text = re.sub(r'\{@link ([^\|\}]+)(?:\|([^\}]+))?\}', link_repl, text)

    # Limpar outras tags genéricas usando o resolvedor refinado com contexto
    def tag_repl(match):
        tag_name = match.group(1)
        inner_text = match.group(2)
        return parse_5etools_tag(tag_name, inner_text, target_slug, ctx)
        
    cleaned = re.sub(r'\{@(\w+) ([^\}]+)\}', tag_repl, text)
    cleaned = format_dice_rolls(cleaned)
    return cleaned

def download_image(img_path, campaign_slug):
    filename = img_path.split("/")[-1]
    local_dir = f"static/images/campaigns/{campaign_slug}"
    local_file = os.path.join(local_dir, filename)
    
    if os.path.exists(local_file):
        return
        
    os.makedirs(local_dir, exist_ok=True)
    encoded_path = urllib.parse.quote(img_path)
    url = IMG_BASE_URL + encoded_path
    
    print(f"    [Download] Baixando imagem: {filename}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(local_file, "wb") as f:
                f.write(response.read())
    except Exception as e:
        print(f"    [Aviso] Falha ao baixar imagem de {url}: {e}")

def parse_entry(entry, campaign_slug, target_slug, ctx):
    if isinstance(entry, str):
        return clean_5etools_tags(entry, campaign_slug, target_slug, ctx)
        
    elif isinstance(entry, dict):
        entry_type = entry.get("type")
        
        if entry_type == "section":
            name = entry.get("name", "")
            content_lines = []
            if name:
                name_clean = clean_5etools_tags(name, campaign_slug, target_slug, ctx)
                content_lines.append(f"\n## {name_clean}\n")
            for sub in entry.get("entries", []):
                res = parse_entry(sub, campaign_slug, target_slug, ctx)
                if res:
                    content_lines.append(res)
            return "\n".join(content_lines)
            
        elif entry_type == "entries":
            name = entry.get("name", "")
            content_lines = []
            if name:
                name_clean = clean_5etools_tags(name, campaign_slug, target_slug, ctx)
                content_lines.append(f"\n### {name_clean}\n")
            for sub in entry.get("entries", []):
                res = parse_entry(sub, campaign_slug, target_slug, ctx)
                if res:
                    content_lines.append(res)
            return "\n".join(content_lines)
            
        elif entry_type in ["inset", "insetReadaloud"]:
            name = entry.get("name", "")
            content_lines = []
            if name:
                name_clean = clean_5etools_tags(name, campaign_slug, target_slug, ctx)
                content_lines.append(f"> ### {name_clean}")
            for sub in entry.get("entries", []):
                res = parse_entry(sub, campaign_slug, target_slug, ctx)
                if res:
                    for line in res.split("\n"):
                        content_lines.append(f"> {line}")
            return "\n".join(content_lines)
            
        elif entry_type == "list":
            content_lines = []
            for item in entry.get("items", []):
                res = parse_entry(item, campaign_slug, target_slug, ctx)
                if res:
                    content_lines.append(f"* {res}")
            return "\n".join(content_lines)
            
        elif entry_type == "table":
            caption = entry.get("caption")
            headers = entry.get("colHeaders", [])
            rows = entry.get("rows", [])
            
            content_lines = []
            if caption:
                caption_clean = clean_5etools_tags(caption, campaign_slug, target_slug, ctx)
                content_lines.append(f"\n**Tabela: {caption_clean}**\n")
                
            if headers:
                clean_headers = [clean_5etools_tags(h, campaign_slug, target_slug, ctx) for h in headers]
                content_lines.append("| " + " | ".join(clean_headers) + " |")
                content_lines.append("| " + " | ".join(["---"] * len(clean_headers)) + " |")
                
            for row in rows:
                clean_row = []
                for cell in row:
                    clean_row.append(parse_entry(cell, campaign_slug, target_slug, ctx))
                content_lines.append("| " + " | ".join(clean_row) + " |")
                
            return "\n".join(content_lines)
            
        elif entry_type == "image":
            title = entry.get("title") or entry.get("name") or "Imagem"
            title_clean = clean_5etools_tags(title, campaign_slug, target_slug, ctx)
            href = entry.get("href", {})
            img_path = href.get("path")
            
            if img_path:
                filename = img_path.split("/")[-1]
                local_path = f"/images/campaigns/{campaign_slug}/{filename}"
                download_image(img_path, campaign_slug)
                return f"\n![{title_clean}]({local_path})\n"
                
        elif entry_type == "gallery":
            content_lines = []
            for item in entry.get("images", []):
                res = parse_entry(item, campaign_slug, target_slug, ctx)
                if res:
                    content_lines.append(res)
            return "\n".join(content_lines)
            
    return ""

def parse_ac(ac_field):
    if not ac_field:
        return "10"
    if isinstance(ac_field, int):
        return str(ac_field)
    if isinstance(ac_field, list):
        parts = []
        for item in ac_field:
            if isinstance(item, int):
                parts.append(str(item))
            elif isinstance(item, dict):
                ac_val = item.get("ac")
                condition = item.get("condition")
                braces = item.get("braces")
                part = str(ac_val)
                if condition:
                    part += f" ({condition})"
                elif braces:
                    part += f" ({', '.join(braces)})"
                parts.append(part)
        return ", ".join(parts)
    return str(ac_field)

def parse_hp(hp_field):
    if not hp_field:
        return "10"
    if isinstance(hp_field, int):
        return str(hp_field)
    if isinstance(hp_field, dict):
        avg = hp_field.get("average")
        formula = hp_field.get("formula")
        if avg and formula:
            return f"{avg} ({formula})"
        if avg:
            return str(avg)
        return str(hp_field)
    return str(hp_field)

def parse_speed(speed_field):
    if not speed_field:
        return "30 ft."
    if isinstance(speed_field, int):
        return f"{speed_field} ft."
    if isinstance(speed_field, dict):
        parts = []
        for mode, val in speed_field.items():
            if mode == "walk":
                parts.append(f"{val} ft.")
            else:
                parts.append(f"{mode} {val} ft.")
        return ", ".join(parts)
    return str(speed_field)

def parse_saves(save_field):
    if not save_field:
        return ""
    if isinstance(save_field, dict):
        parts = []
        for attr, modifier in save_field.items():
            parts.append(f"{attr.title()} {modifier}")
        return ", ".join(parts)
    return str(save_field)

def parse_skills(skill_field):
    if not skill_field:
        return ""
    if isinstance(skill_field, dict):
        parts = []
        for skill, modifier in skill_field.items():
            parts.append(f"{skill.title()} {modifier}")
        return ", ".join(parts)
    return str(skill_field)

def parse_entries_list(entries, campaign_slug, target_slug):
    lines = []
    ctx = {"campaign_creatures": set(), "campaign_items": set(), "monsters": set(), "spells": set(), "items": set(), "locations": set()}
    for entry in entries:
        if isinstance(entry, str):
            lines.append(clean_5etools_tags(entry, campaign_slug, target_slug, ctx))
        elif isinstance(entry, dict):
            res = parse_entry(entry, campaign_slug, target_slug, ctx)
            if res:
                lines.append(res)
    return "\n\n".join(lines)

def format_statblock_markdown(m, campaign_slug, target_slug):
    stats = {
        "ac": parse_ac(m.get("ac")),
        "hp": parse_hp(m.get("hp")),
        "speed": parse_speed(m.get("speed")),
        "attributes": {
            "str": m.get("str", 10),
            "dex": m.get("dex", 10),
            "con": m.get("con", 10),
            "int": m.get("int", 10),
            "wis": m.get("wis", 10),
            "cha": m.get("cha", 10),
        }
    }
    
    saves = parse_saves(m.get("save"))
    if saves:
        stats["saves"] = saves
        
    skills = parse_skills(m.get("skill"))
    if skills:
        stats["skills"] = skills
        
    senses = []
    if m.get("senses"):
        senses.extend(m.get("senses"))
    if m.get("passive"):
        senses.append(f"passive Perception {m.get('passive')}")
    if senses:
        stats["senses"] = ", ".join(senses)
        
    if m.get("languages"):
        stats["languages"] = ", ".join(m.get("languages"))
        
    if m.get("cr"):
        stats["cr"] = str(m.get("cr"))
        
    sizes = m.get("size", ["M"])
    size_char = sizes[0] if isinstance(sizes, list) else sizes
    size_map = {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}
    size_str = size_map.get(size_char, "Medium")
    
    type_str = m.get("type", "monstrosity")
    if isinstance(type_str, dict):
        type_str = type_str.get("type")
        
    align_list = m.get("alignment", [])
    align_map = {"L": "leal", "N": "neutro", "C": "caótico", "G": "bom", "E": "mau", "U": "sem tendência"}
    align_parts = [align_map[c] for c in align_list if isinstance(c, str) and c in align_map]
    align_str = " e ".join(align_parts) if align_parts else "sem tendência"
    
    stats_meta = f"{size_str} {type_str}, {align_str}"
    
    body_parts = []
    if m.get("trait"):
        body_parts.append("### Características\n")
        for trait in m.get("trait"):
            name = trait.get("name")
            desc = parse_entries_list(trait.get("entries", []), campaign_slug, target_slug)
            body_parts.append(f"**{name}.** {desc}\n")
            
    if m.get("action"):
        body_parts.append("### Ações\n")
        for act in m.get("action"):
            name = act.get("name")
            desc = parse_entries_list(act.get("entries", []), campaign_slug, target_slug)
            body_parts.append(f"**{name}.** {desc}\n")
            
    return stats, stats_meta, "\n".join(body_parts)

def write_handout_art_stub(campaign_slug, entity_slug, entity_name, img_filename):
    os.makedirs(f"content/campaigns/{campaign_slug}/handouts", exist_ok=True)
    handout_slug = f"{entity_slug}-art"
    handout_file = f"content/campaigns/{campaign_slug}/handouts/{handout_slug}.md"
    if os.path.exists(handout_file):
        return f"/campaigns/{campaign_slug}/handouts/{handout_slug}/"
        
    local_path = f"/images/campaigns/{campaign_slug}/{img_filename}"
    
    with open(handout_file, "w") as f:
        f.write(f"""---
title: "Arte: {entity_name}"
params:
  kind: "handout"
draft: true
titulo_pt_br: ""
visibility: "players"
status: "ready"
tags:
  - handout
  - arte
  - importado
---

![Arte: {entity_name}]({local_path})
""")
    print(f"    [Handout de Arte] Criado handout para os jogadores: Arte: {entity_name}")
    return f"/campaigns/{campaign_slug}/handouts/{handout_slug}/"

def write_npc_stub(campaign_slug, npc_slug, npc_name, bestiary_entry=None, target_slug=None):
    npc_file = f"content/campaigns/{campaign_slug}/npcs/{npc_slug}.md"
    if os.path.exists(npc_file):
        handout_refs = []
        if bestiary_entry and bestiary_entry.get("fluff"):
            fluff = bestiary_entry["fluff"]
            img_paths = extract_fluff_images(fluff)
            for path in img_paths:
                handout_refs.append(f"/campaigns/{campaign_slug}/handouts/{npc_slug}-art/")
        return handout_refs
        
    front_matter_lines = [
        "---",
        f'title: "{npc_name}"',
        'draft: true',
        'titulo_pt_br: ""',
        'visibility: "gm"',
        'status: "ready"',
        'tags:',
        '  - npc',
        '  - importado',
        'params:',
        '  kind: "npc"'
    ]
    
    body = f"\nNPC **{npc_name}** importado automaticamente da campanha.\n"
    handout_refs = []
    
    if bestiary_entry:
        m = bestiary_entry["stats"]
        stats, stats_meta, stats_body = format_statblock_markdown(m, campaign_slug, target_slug)
        fluff = bestiary_entry.get("fluff")
        
        front_matter_lines.append(f'stats_meta: "{stats_meta}"')
        front_matter_lines.append("stats:")
        front_matter_lines.append(f'  ac: "{stats["ac"]}"')
        front_matter_lines.append(f'  hp: "{stats["hp"]}"')
        front_matter_lines.append(f'  speed: "{stats["speed"]}"')
        front_matter_lines.append("  attributes:")
        for attr, val in stats["attributes"].items():
            front_matter_lines.append(f"    {attr}: {val}")
        if "saves" in stats:
            front_matter_lines.append(f'  saves: "{stats["saves"]}"')
        if "skills" in stats:
            front_matter_lines.append(f'  skills: "{stats["skills"]}"')
        if "senses" in stats:
            front_matter_lines.append(f'  senses: "{stats["senses"]}"')
        if "languages" in stats:
            front_matter_lines.append(f'  languages: "{stats["languages"]}"')
        if "cr" in stats:
            front_matter_lines.append(f'  cr: "{stats["cr"]}"')
            
        lore_markdown = ""
        if fluff:
            fluff_entries = fluff.get("entries", [])
            lore_markdown = parse_entries_list(fluff_entries, campaign_slug, target_slug)
            
            img_paths = extract_fluff_images(fluff)
            for path in img_paths:
                filename = path.split("/")[-1]
                download_image(path, campaign_slug)
                local_path = f"/images/campaigns/{campaign_slug}/{filename}"
                lore_markdown = f"![Arte: {npc_name}]({local_path})\n\n" + lore_markdown
                h_ref = write_handout_art_stub(campaign_slug, npc_slug, npc_name, filename)
                handout_refs.append(h_ref)
            
        body = f"""
{lore_markdown}

{stats_body}
"""
        
    front_matter_lines.append("---")
    
    with open(npc_file, "w") as f:
        f.write("\n".join(front_matter_lines) + "\n" + body)
    print(f"    [NPC] Importado NPC detalhado: {npc_name}")
    return handout_refs

def write_monster_stub(campaign_slug, monster_slug, monster_name, bestiary_entry=None, target_slug=None):
    os.makedirs("content/compendium/monsters", exist_ok=True)
    monster_file = f"content/compendium/monsters/{monster_slug}.md"
    if os.path.exists(monster_file):
        handout_refs = []
        if bestiary_entry and bestiary_entry.get("fluff"):
            fluff = bestiary_entry["fluff"]
            img_paths = extract_fluff_images(fluff)
            for path in img_paths:
                handout_refs.append(f"/campaigns/{campaign_slug}/handouts/{monster_slug}-art/")
        return handout_refs
        
    front_matter_lines = [
        "---",
        f'title: "{monster_name}"',
        'draft: true',
        'titulo_pt_br: ""',
        'visibility: "gm"',
        'status: "ready"',
        'tags:',
        '  - monstro',
        '  - importado',
        'params:',
        '  kind: "monster"'
    ]
    
    body = f"\nMonstro **{monster_name}** importado automaticamente da campanha.\n"
    handout_refs = []
    
    if bestiary_entry:
        m = bestiary_entry["stats"]
        stats, stats_meta, stats_body = format_statblock_markdown(m, campaign_slug, target_slug)
        fluff = bestiary_entry.get("fluff")
        
        front_matter_lines.append(f'stats_meta: "{stats_meta}"')
        front_matter_lines.append("stats:")
        front_matter_lines.append(f'  ac: "{stats["ac"]}"')
        front_matter_lines.append(f'  hp: "{stats["hp"]}"')
        front_matter_lines.append(f'  speed: "{stats["speed"]}"')
        front_matter_lines.append("  attributes:")
        for attr, val in stats["attributes"].items():
            front_matter_lines.append(f"    {attr}: {val}")
        if "saves" in stats:
            front_matter_lines.append(f'  saves: "{stats["saves"]}"')
        if "skills" in stats:
            front_matter_lines.append(f'  skills: "{stats["skills"]}"')
        if "senses" in stats:
            front_matter_lines.append(f'  senses: "{stats["senses"]}"')
        if "languages" in stats:
            front_matter_lines.append(f'  languages: "{stats["languages"]}"')
        if "cr" in stats:
            front_matter_lines.append(f'  cr: "{stats["cr"]}"')
            
        lore_markdown = ""
        if fluff:
            fluff_entries = fluff.get("entries", [])
            lore_markdown = parse_entries_list(fluff_entries, campaign_slug, target_slug)
            
            img_paths = extract_fluff_images(fluff)
            for path in img_paths:
                filename = path.split("/")[-1]
                download_image(path, campaign_slug)
                local_path = f"/images/campaigns/{campaign_slug}/{filename}"
                lore_markdown = f"![Arte: {monster_name}]({local_path})\n\n" + lore_markdown
                h_ref = write_handout_art_stub(campaign_slug, monster_slug, monster_name, filename)
                handout_refs.append(h_ref)
            
        body = f"""
{lore_markdown}

{stats_body}
"""
        
    front_matter_lines.append("---")
    
    with open(monster_file, "w") as f:
        f.write("\n".join(front_matter_lines) + "\n" + body)
    print(f"    [Monstro] Importado monstro detalhado para o Compêndio: {monster_name}")
    return handout_refs

def write_magic_item_stub(campaign_slug, item_slug, item_name):
    os.makedirs("content/compendium/magic-items", exist_ok=True)
    item_file = f"content/compendium/magic-items/{item_slug}.md"
    if os.path.exists(item_file):
        return
        
    with open(item_file, "w") as f:
        f.write(f"""---
title: "{item_name}"
params:
  kind: "magic_item"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
tags:
  - item_magico
  - importado
---

Item mágico **{item_name}** importado automaticamente da campanha.
""")
    print(f"    [Item Mágico] Importado item mágico detalhado para o Compêndio: {item_name}")

def write_location_stub(campaign_slug, loc_slug, loc_name):
    loc_file = f"content/campaigns/{campaign_slug}/locations/{loc_slug}.md"
    if os.path.exists(loc_file):
        return
    with open(loc_file, "w") as f:
        f.write(f"""---
title: "{loc_name}"
params:
  kind: "location"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
tags:
  - localidade
  - importado
---

Localidade **{loc_name}** importada automaticamente da campanha.
""")
    print(f"    [Localidade] Criado stub de Localidade: {loc_name}")

def create_directory_structure(campaign_slug):
    paths = [
        f"content/campaigns/{campaign_slug}/adventures",
        f"content/campaigns/{campaign_slug}/journal",
        f"content/campaigns/{campaign_slug}/characters",
        f"content/campaigns/{campaign_slug}/npcs",
        f"content/campaigns/{campaign_slug}/locations",
        f"content/campaigns/{campaign_slug}/factions",
        f"content/campaigns/{campaign_slug}/handouts"
    ]
    for p in paths:
        os.makedirs(p, exist_ok=True)
        idx = os.path.join(p, "_index.md")
        if not os.path.exists(idx):
            dir_name = p.split("/")[-1]
            title = dir_name.title()
            if dir_name == "npcs":
                title = "Personagens Não-Jogáveis (NPCs)"
            elif dir_name == "factions":
                title = "Organizações e Facções"
            elif dir_name == "characters":
                title = "Personagens dos Jogadores"
            elif dir_name == "handouts":
                title = "Handouts e Materiais"
            
            with open(idx, "w") as f:
                f.write(f"""---
title: "{title}"
params:
  kind: "{dir_name}_index"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "draft"
---
""")

def write_campaign_index(campaign_slug, campaign_title):
    idx = f"content/campaigns/{campaign_slug}/_index.md"
    if os.path.exists(idx):
        return
        
    with open(idx, "w") as f:
        f.write(f"""---
title: "{campaign_title}"
params:
  kind: "campaign"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "active"
system: "D&D 5e"
---

### Descrição Geral
Campanha importada do 5e.tools: {campaign_title}.

### Pitch
[Insira o pitch da campanha]

### Links Rápidos
* [A História Até Aqui (Diário)](/campaigns/{campaign_slug}/journal/)
* [Aventuras Ativas](/campaigns/{campaign_slug}/adventures/)
""")

def create_adventure_structure(campaign_slug, adv_slug, adv_title):
    adv_dir = f"content/campaigns/{campaign_slug}/adventures/{adv_slug}"
    sessions_dir = os.path.join(adv_dir, "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    
    adv_idx = os.path.join(adv_dir, "_index.md")
    if not os.path.exists(adv_idx):
        with open(adv_idx, "w") as f:
            f.write(f"""---
title: "{adv_title}"
params:
  kind: "adventure"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Aventura independente importada do capítulo {adv_title}."
---
""")
            
    sessions_idx = os.path.join(sessions_dir, "_index.md")
    if not os.path.exists(sessions_idx):
        with open(sessions_idx, "w") as f:
            f.write(f"""---
title: "Sessões de {adv_title}"
params:
  kind: "sessions_index"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Lista de sessões planejadas e jogadas para a aventura {adv_title}."
---
""")
    return adv_dir, sessions_dir

def create_session_structure(adv_dir, session_slug, session_title):
    sess_dir = os.path.join(adv_dir, "sessions", session_slug)
    scenes_dir = os.path.join(sess_dir, "scenes")
    os.makedirs(scenes_dir, exist_ok=True)
    
    sess_idx = os.path.join(sess_dir, "_index.md")
    if not os.path.exists(sess_idx):
        with open(sess_idx, "w") as f:
            f.write(f"""---
title: "{session_title}"
params:
  kind: "session"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Planejamento para a sessão."
---
""")
            
    scenes_idx = os.path.join(scenes_dir, "_index.md")
    if not os.path.exists(scenes_idx):
        with open(scenes_idx, "w") as f:
            f.write(f"""---
title: "Cenas de {session_title}"
params:
  kind: "scenes_index"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Lista de cenas operacionais para a sessão."
---
""")
    return sess_dir, scenes_dir

def fetch_adventure_data(slug):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"  [5e.tools] Baixando índice de aventuras...")
    req = urllib.request.Request(DATA_BASE_URL + "adventures.json", headers=headers)
    with urllib.request.urlopen(req) as r:
        adv_index = json.loads(r.read().decode())
        
    adventure_meta = None
    for adv in adv_index.get("adventure", []):
        if adv.get("id", "").lower() == slug.lower() or adv.get("source", "").lower() == slug.lower():
            adventure_meta = adv
            break
            
    if not adventure_meta:
        print(f"Erro: Aventura '{slug}' não encontrada no índice do 5e.tools.")
        sys.exit(1)
        
    print(f"  [5e.tools] Baixando conteúdo da aventura {adventure_meta['name']}...")
    req = urllib.request.Request(DATA_BASE_URL + f"adventure/adventure-{slug.lower()}.json", headers=headers)
    with urllib.request.urlopen(req) as r:
        adventure_data = json.loads(r.read().decode())
        
    return adventure_meta, adventure_data

def fetch_bestiary_data(slug):
    headers = {'User-Agent': 'Mozilla/5.0'}
    bestiary_data = {}
    
    url_bestiary = DATA_BASE_URL + f"bestiary/bestiary-{slug.lower()}.json"
    url_fluff = DATA_BASE_URL + f"bestiary/fluff-bestiary-{slug.lower()}.json"
    
    monsters_list = []
    fluff_list = []
    
    try:
        req = urllib.request.Request(url_bestiary, headers=headers)
        with urllib.request.urlopen(req) as r:
            bestiary_json = json.loads(r.read().decode())
            monsters_list = bestiary_json.get("monster", [])
            print(f"  [5e.tools] Encontrado bestiário com {len(monsters_list)} criaturas específicas.")
    except Exception as e:
        print(f"  [5e.tools] Aventura não possui bestiário específico (ou falha: {e}).")
        
    try:
        req = urllib.request.Request(url_fluff, headers=headers)
        with urllib.request.urlopen(req) as r:
            fluff_json = json.loads(r.read().decode())
            fluff_list = fluff_json.get("monsterFluff", [])
    except Exception as e:
        pass
        
    fluff_by_name = {f.get("name").lower(): f for f in fluff_list}
    
    for m in monsters_list:
        name = m.get("name")
        fluff = fluff_by_name.get(name.lower())
        bestiary_data[name.lower()] = {
            "stats": m,
            "fluff": fluff
        }
        
    return bestiary_data

def handle_campaign_entities(campaign_slug, target_slug, creatures_set, items_set, monsters_set, bestiary_data, all_npcs, all_monsters, all_handouts):
    # Separa criaturas, monstros e itens da campanha e cria stubs corretos
    scene_npcs_refs = []
    scene_monsters_refs = []
    scene_items_refs = []
    scene_handouts_refs = []
    
    # 1. Processar criaturas da campanha (NPCs vs Monstros Específicos de Campanha)
    for c_slug, c_name in creatures_set:
        entry = bestiary_data.get(c_name.lower())
        
        is_real_npc = False
        if entry:
            stats = entry["stats"]
            if stats.get("isNpc") or stats.get("isNamedCreature"):
                is_real_npc = True
        else:
            is_real_npc = True
            
        if is_real_npc:
            h_refs = write_npc_stub(campaign_slug, c_slug, c_name, entry, target_slug)
            npc_ref = f"/campaigns/{campaign_slug}/npcs/{c_slug}/"
            scene_npcs_refs.append(npc_ref)
            all_npcs.add(npc_ref)
            for hr in h_refs:
                scene_handouts_refs.append(hr)
                all_handouts.add(hr)
        else:
            h_refs = write_monster_stub(campaign_slug, c_slug, c_name, entry, target_slug)
            monster_ref = f"/compendium/monsters/{c_slug}/"
            scene_monsters_refs.append(monster_ref)
            all_monsters.add(monster_ref)
            for hr in h_refs:
                scene_handouts_refs.append(hr)
                all_handouts.add(hr)
            
    # 2. Processar monstros gerais da cena (ex: goblin do MM) no Compêndio Global
    for m_slug, m_name, m_source in monsters_set:
        monster_file = f"content/compendium/monsters/{m_slug}.md"
        monster_ref = f"/compendium/monsters/{m_slug}/"
        scene_monsters_refs.append(monster_ref)
        all_monsters.add(monster_ref)
        
        entry = get_monster_from_source(m_name, m_source)
        h_refs = write_monster_stub(campaign_slug, m_slug, m_name, entry, target_slug)
        for hr in h_refs:
            scene_handouts_refs.append(hr)
            all_handouts.add(hr)
            
    # 3. Processar itens mágicos específicos da aventura
    for i_slug, i_name in items_set:
        write_magic_item_stub(campaign_slug, i_slug, i_name)
        item_ref = f"/compendium/magic-items/{i_slug}/"
        scene_items_refs.append(item_ref)
        
    return scene_npcs_refs, scene_monsters_refs, scene_items_refs, scene_handouts_refs

def main():
    parser = argparse.ArgumentParser(description="Importador de Campanhas do 5e.tools")
    parser.add_argument("slug", help="Slug da aventura no 5e.tools (ex: jttrc, lmop)")
    args = parser.parse_args()
    
    slug = args.slug
    adv_meta, adv_data = fetch_adventure_data(slug)
    bestiary_data = fetch_bestiary_data(slug)
    
    campaign_title = adv_meta["name"]
    campaign_slug = slugify(campaign_title)
    
    print(f"\nAventura carregada: {campaign_title}")
    print(f"Total de capítulos: {len(adv_data.get('data', []))}")
    print("\nCapítulos:")
    for idx, chap in enumerate(adv_data.get("data", [])):
        print(f"  [{idx}] {chap.get('name')}")
        
    print("\nOpções de Mapeamento:")
    print("  (1) Livro Inteiro como Única Aventura: O livro vira a campanha. Cada capítulo vira uma Sessão. As subseções do capítulo viram Cenas.")
    print("  (2) Antologia de Aventuras: O livro vira a campanha. Cada capítulo vira uma Aventura independente sob a pasta `adventures/`.")
    print("  (3) Apenas Um Capítulo Específico: Escolha um único capítulo para importar como Aventura isolada na campanha.")
    
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    create_directory_structure(campaign_slug)
    write_campaign_index(campaign_slug, campaign_title)
    
    chapters = adv_data.get("data", [])
    
    if choice == "1":
        adv_slug = campaign_slug
        adv_dir, sessions_dir = create_adventure_structure(campaign_slug, adv_slug, campaign_title)
        
        all_npcs = set()
        all_monsters = set()
        all_locations = set()
        all_handouts = set()
            
        for c_idx, chap in enumerate(chapters):
            chap_title = chap.get("name")
            session_slug = f"{c_idx+1:03d}-{slugify(chap_title)}"
            session_title = f"Sessão {c_idx+1} - {chap_title}"
            
            loc_slug = slugify(chap_title)
            write_location_stub(campaign_slug, loc_slug, chap_title)
            all_locations.add(f"/campaigns/{campaign_slug}/locations/{loc_slug}/")
            
            sess_dir, scenes_dir = create_session_structure(adv_dir, session_slug, session_title)
                
            scenes = []
            current_scene_title = "Introdução"
            current_scene_entries = []
            
            for entry in chap.get("entries", []):
                if isinstance(entry, dict) and entry.get("type") in ["section", "entries"]:
                    if current_scene_entries:
                        scenes.append((current_scene_title, current_scene_entries))
                        current_scene_entries = []
                    current_scene_title = entry.get("name") or "Cena"
                    current_scene_entries.extend(entry.get("entries", []))
                else:
                    current_scene_entries.append(entry)
                    
            if current_scene_entries:
                scenes.append((current_scene_title, current_scene_entries))
                
            for s_idx, (s_title, s_entries) in enumerate(scenes):
                scene_slug = f"{s_idx+1:02d}-{slugify(s_title)}"
                scene_file = os.path.join(scenes_dir, f"{scene_slug}.md")
                
                ctx = {
                    "campaign_creatures": set(),
                    "campaign_items": set(),
                    "monsters": set(),
                    "spells": set(),
                    "items": set(),
                    "locations": set()
                }
                
                content_markdown = ""
                for entry in s_entries:
                    res = parse_entry(entry, campaign_slug, slug, ctx)
                    if res:
                        content_markdown += res + "\n\n"
                
                scene_npcs, scene_spec_monsters, scene_spec_items, scene_handouts = handle_campaign_entities(
                    campaign_slug, slug, ctx["campaign_creatures"], ctx["campaign_items"], ctx["monsters"], bestiary_data, all_npcs, all_monsters, all_handouts
                )
                
                scene_monsters = [f"/compendium/monsters/{m}/" for m, _, _ in ctx["monsters"]]
                for m_ref in scene_spec_monsters:
                    if m_ref not in scene_monsters:
                        scene_monsters.append(m_ref)
                for i_ref in scene_spec_items:
                    scene_monsters.append(i_ref)
                    
                scene_locations = [f"/campaigns/{campaign_slug}/locations/{loc_slug}/"]
                
                with open(scene_file, "w") as f:
                    npcs_yaml = "\n".join([f"  - \"{n}\"" for n in scene_npcs])
                    monsters_yaml = "\n".join([f"  - \"{m}\"" for m in scene_monsters])
                    locations_yaml = "\n".join([f"  - \"{l}\"" for l in scene_locations])
                    handouts_yaml = "\n".join([f"  - \"{h}\"" for h in scene_handouts])
                    
                    f.write(f"""---
title: "Cena {s_idx+1} - {s_title}"
params:
  kind: "scene"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Cena operacional para conduzir na sessão."
npcs:
{npcs_yaml}
locations:
{locations_yaml}
compendium_refs:
{monsters_yaml}
handouts:
{handouts_yaml}
---

### Descrição e Elementos Importantes

{content_markdown}
""")
                    
        # Gravar as associações acumuladas no _index.md da Aventura
        adv_idx = os.path.join(adv_dir, "_index.md")
        npcs_yaml = "\n".join([f"  - \"{n}\"" for n in sorted(list(all_npcs))])
        locations_yaml = "\n".join([f"  - \"{l}\"" for l in sorted(list(all_locations))])
        handouts_yaml = "\n".join([f"  - \"{h}\"" for h in sorted(list(all_handouts))])
        
        with open(adv_idx, "w") as f:
            f.write(f"""---
title: "{campaign_title}"
params:
  kind: "adventure"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Aventura principal da campanha {campaign_title}."
npcs:
{npcs_yaml}
locations:
{locations_yaml}
handouts:
{handouts_yaml}
---
""")

    elif choice == "2" or choice == "3":
        target_chaps = []
        if choice == "2":
            target_chaps = chapters
        else:
            chap_choice = int(input(f"Selecione o capítulo (0-{len(chapters)-1}): ").strip())
            target_chaps = [chapters[chap_choice]]
            
        for chap in target_chaps:
            chap_title = chap.get("name")
            adv_slug = slugify(chap_title)
            
            adv_dir, sessions_dir = create_adventure_structure(campaign_slug, adv_slug, chap_title)
            
            loc_slug = adv_slug
            write_location_stub(campaign_slug, loc_slug, chap_title)
            adventure_locations = {f"/campaigns/{campaign_slug}/locations/{loc_slug}/"}
            adventure_npcs = set()
            adventure_monsters = set()
            adventure_handouts = set()
            
            sess_slug = "001-inicio"
            session_title = "Sessão 01 - Início"
            
            sess_dir, scenes_dir = create_session_structure(adv_dir, sess_slug, session_title)
                
            scenes = []
            current_scene_title = "Introdução"
            current_scene_entries = []
            
            for entry in chap.get("entries", []):
                if isinstance(entry, dict) and entry.get("type") in ["section", "entries"]:
                    if current_scene_entries:
                        scenes.append((current_scene_title, current_scene_entries))
                        current_scene_entries = []
                    current_scene_title = entry.get("name") or "Cena"
                    current_scene_entries.extend(entry.get("entries", []))
                else:
                    current_scene_entries.append(entry)
                    
            if current_scene_entries:
                scenes.append((current_scene_title, current_scene_entries))
                
            for s_idx, (s_title, s_entries) in enumerate(scenes):
                scene_slug = f"{s_idx+1:02d}-{slugify(s_title)}"
                scene_file = os.path.join(scenes_dir, f"{scene_slug}.md")
                
                ctx = {
                    "campaign_creatures": set(),
                    "campaign_items": set(),
                    "monsters": set(),
                    "spells": set(),
                    "items": set(),
                    "locations": set()
                }
                
                content_markdown = ""
                for entry in s_entries:
                    res = parse_entry(entry, campaign_slug, slug, ctx)
                    if res:
                        content_markdown += res + "\n\n"
                
                scene_npcs, scene_spec_monsters, scene_spec_items, scene_handouts = handle_campaign_entities(
                    campaign_slug, slug, ctx["campaign_creatures"], ctx["campaign_items"], ctx["monsters"], bestiary_data, adventure_npcs, adventure_monsters, adventure_handouts
                )
                
                scene_monsters = [f"/compendium/monsters/{m}/" for m, _, _ in ctx["monsters"]]
                for m_ref in scene_spec_monsters:
                    if m_ref not in scene_monsters:
                        scene_monsters.append(m_ref)
                for i_ref in scene_spec_items:
                    scene_monsters.append(i_ref)
                    
                scene_locations = [f"/campaigns/{campaign_slug}/locations/{loc_slug}/"]
                
                with open(scene_file, "w") as f:
                    npcs_yaml = "\n".join([f"  - \"{n}\"" for n in scene_npcs])
                    monsters_yaml = "\n".join([f"  - \"{m}\"" for m in scene_monsters])
                    locations_yaml = "\n".join([f"  - \"{l}\"" for l in scene_locations])
                    handouts_yaml = "\n".join([f"  - \"{h}\"" for h in scene_handouts])
                    
                    f.write(f"""---
title: "Cena {s_idx+1} - {s_title}"
params:
  kind: "scene"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Cena operacional para conduzir na sessão."
npcs:
{npcs_yaml}
locations:
{locations_yaml}
compendium_refs:
{monsters_yaml}
handouts:
{handouts_yaml}
---

### Descrição e Elementos Importantes

{content_markdown}
""")
            
            adv_idx = os.path.join(adv_dir, "_index.md")
            npcs_yaml = "\n".join([f"  - \"{n}\"" for n in sorted(list(adventure_npcs))])
            locations_yaml = "\n".join([f"  - \"{l}\"" for l in sorted(list(adventure_locations))])
            handouts_yaml = "\n".join([f"  - \"{h}\"" for h in sorted(list(adventure_handouts))])
            
            with open(adv_idx, "w") as f:
                f.write(f"""---
title: "{chap_title}"
params:
  kind: "adventure"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Aventura independente importada do capítulo {chap_title}."
npcs:
{npcs_yaml}
locations:
{locations_yaml}
handouts:
{handouts_yaml}
---
""")

    print(f"\n[Sucesso] Importação concluída! Campanha criada em content/campaigns/{campaign_slug}/")

if __name__ == "__main__":
    main()
