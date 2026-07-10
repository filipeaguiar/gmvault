#!/usr/bin/env python3
import urllib.request
import json
import os
import sys
import re
import unicodedata
import argparse

DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"
IMG_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/master/"

# Lista de fontes conhecidas do D&D para ignorar se aparecerem como argumento de exibição nas tags
KNOWN_SOURCES = {
    "phb", "mm", "dmg", "scag", "vgm", "xge", "toa", "mtof", "tcoe", "vrgr", 
    "jttrc", "cos", "erlw", "wbw", "bgdia", "idrotf", "lmop", "oota", "typt", 
    "ggr", "ftd", "scc", "aag", "bam", "dltso", "pactc", "sat", "bmt", "kftgv"
}

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '', text.replace(' ', '-'))
    return text

def format_dice_rolls(text):
    # Envelopa rolagens em colchetes duplos [[formula]] de forma limpa.
    # Captura padrões como 1d6, 3d4+3, 2d10 - 1, etc.
    def dice_repl(match):
        formula = match.group(1).replace(" ", "") # remove espaços internos na fórmula de dados
        return f"[[{formula}]]"

    # Regex para capturar XdY com opcional +Z ou -Z (permitindo espaços)
    # Evita casamentos parciais e não captura se já precedido por [[
    pattern = r'(?<!\[\[)\b(\d+d\d+(?:\s*[\+\-]\s*\d+)?)\b(?!\]\])'
    return re.sub(pattern, dice_repl, text)

def parse_5etools_tag(tag_name, inner_text):
    args = inner_text.split('|')
    default_val = args[0]
    
    if tag_name in ["spell", "monster", "item", "condition", "race", "class", "feat", "creature"]:
        if len(args) > 1:
            # Se o último argumento for igual a uma fonte conhecida, usamos o primeiro argumento
            last_arg = args[-1]
            if last_arg.lower() in KNOWN_SOURCES:
                return default_val.replace('-', ' ').title()
            
            # Se houver 3 argumentos e o segundo for a fonte, e o terceiro o display
            if len(args) > 2 and args[1].lower() in KNOWN_SOURCES:
                return args[2]
                
            return last_arg
        return default_val.replace('-', ' ').title()
        
    elif tag_name == "area":
        # {@area Aroon Family Pepper Challenge.|05c|x} -> Retorna o nome amigável da área (arg1)
        return default_val
        
    elif tag_name == "dc":
        # {@dc 12} -> CD 12
        return f"CD {default_val}"
        
    # Se houver mais de um argumento e não for fonte, tenta usar o último como label
    if len(args) > 1:
        last_arg = args[-1]
        if last_arg.lower() not in KNOWN_SOURCES:
            return last_arg
            
    return default_val

def clean_5etools_tags(text):
    # Envelopa as rolagens de dados e danos explícitas antes de limpá-las
    # {@dice 1d6+2} -> [[1d6+2]]
    # {@damage 2d6} -> [[2d6]]
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

    # Limpar outras tags genéricas usando o resolvedor refinado
    def tag_repl(match):
        tag_name = match.group(1)
        inner_text = match.group(2)
        return parse_5etools_tag(tag_name, inner_text)
        
    cleaned = re.sub(r'\{@(\w+) ([^\}]+)\}', tag_repl, text)
    
    # Aplica formatação de dados no texto que sobrou (rolagens soltas)
    cleaned = format_dice_rolls(cleaned)
    return cleaned

def download_image(img_path, campaign_slug):
    filename = img_path.split("/")[-1]
    local_dir = f"static/images/campaigns/{campaign_slug}"
    local_file = os.path.join(local_dir, filename)
    
    if os.path.exists(local_file):
        return
        
    os.makedirs(local_dir, exist_ok=True)
    # Encodar espaços e caracteres especiais no path da imagem
    import urllib.parse
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

def parse_entry(entry, campaign_slug):
    if isinstance(entry, str):
        return clean_5etools_tags(entry)
        
    elif isinstance(entry, dict):
        entry_type = entry.get("type")
        
        if entry_type == "section":
            name = entry.get("name", "")
            content_lines = []
            if name:
                name_clean = clean_5etools_tags(name)
                content_lines.append(f"\n## {name_clean}\n")
            for sub in entry.get("entries", []):
                res = parse_entry(sub, campaign_slug)
                if res:
                    content_lines.append(res)
            return "\n".join(content_lines)
            
        elif entry_type == "entries":
            name = entry.get("name", "")
            content_lines = []
            if name:
                name_clean = clean_5etools_tags(name)
                content_lines.append(f"\n### {name_clean}\n")
            for sub in entry.get("entries", []):
                res = parse_entry(sub, campaign_slug)
                if res:
                    content_lines.append(res)
            return "\n".join(content_lines)
            
        elif entry_type in ["inset", "insetReadaloud"]:
            name = entry.get("name", "")
            content_lines = []
            if name:
                name_clean = clean_5etools_tags(name)
                content_lines.append(f"> ### {name_clean}")
            for sub in entry.get("entries", []):
                res = parse_entry(sub, campaign_slug)
                if res:
                    for line in res.split("\n"):
                        content_lines.append(f"> {line}")
            return "\n".join(content_lines)
            
        elif entry_type == "list":
            content_lines = []
            for item in entry.get("items", []):
                res = parse_entry(item, campaign_slug)
                if res:
                    content_lines.append(f"* {res}")
            return "\n".join(content_lines)
            
        elif entry_type == "table":
            caption = entry.get("caption")
            headers = entry.get("colHeaders", [])
            rows = entry.get("rows", [])
            
            content_lines = []
            if caption:
                caption_clean = clean_5etools_tags(caption)
                content_lines.append(f"\n**Tabela: {caption_clean}**\n")
                
            if headers:
                clean_headers = [clean_5etools_tags(h) for h in headers]
                content_lines.append("| " + " | ".join(clean_headers) + " |")
                content_lines.append("| " + " | ".join(["---"] * len(clean_headers)) + " |")
                
            for row in rows:
                clean_row = []
                for cell in row:
                    clean_row.append(parse_entry(cell, campaign_slug))
                content_lines.append("| " + " | ".join(clean_row) + " |")
                
            return "\n".join(content_lines)
            
        elif entry_type == "image":
            title = entry.get("title") or entry.get("name") or "Imagem"
            title_clean = clean_5etools_tags(title)
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
                res = parse_entry(item, campaign_slug)
                if res:
                    content_lines.append(res)
            return "\n".join(content_lines)
            
    return ""

def create_directory_structure(campaign_slug):
    paths = [
        f"content/campaigns/{campaign_slug}/adventures",
        f"content/campaigns/{campaign_slug}/journal",
        f"content/campaigns/{campaign_slug}/characters",
        f"content/campaigns/{campaign_slug}/npcs",
        f"content/campaigns/{campaign_slug}/locations",
        f"content/campaigns/{campaign_slug}/factions"
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
            
            with open(idx, "w") as f:
                f.write(f"""---
title: "{title}"
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
    
    # 1. _index.md da Aventura
    adv_idx = os.path.join(adv_dir, "_index.md")
    if not os.path.exists(adv_idx):
        with open(adv_idx, "w") as f:
            f.write(f"""---
title: "{adv_title}"
kind: "adventure"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Aventura independente importada do capítulo {adv_title}."
---
""")
            
    # 2. _index.md intermediário de Sessões (sessions/_index.md)
    sessions_idx = os.path.join(sessions_dir, "_index.md")
    if not os.path.exists(sessions_idx):
        with open(sessions_idx, "w") as f:
            f.write(f"""---
title: "Sessões de {adv_title}"
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
    
    # 1. _index.md da Sessão
    sess_idx = os.path.join(sess_dir, "_index.md")
    if not os.path.exists(sess_idx):
        with open(sess_idx, "w") as f:
            f.write(f"""---
title: "{session_title}"
kind: "session"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Planejamento para a sessão."
---
""")
            
    # 2. _index.md intermediário de Cenas (scenes/_index.md)
    scenes_idx = os.path.join(scenes_dir, "_index.md")
    if not os.path.exists(scenes_idx):
        with open(scenes_idx, "w") as f:
            f.write(f"""---
title: "Cenas de {session_title}"
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

def main():
    parser = argparse.ArgumentParser(description="Importador de Campanhas do 5e.tools")
    parser.add_argument("slug", help="Slug da aventura no 5e.tools (ex: jttrc, lmop)")
    args = parser.parse_args()
    
    slug = args.slug
    adv_meta, adv_data = fetch_adventure_data(slug)
    
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
        # Cria a Aventura principal e a pasta intermediária de sessões
        adv_dir, sessions_dir = create_adventure_structure(campaign_slug, campaign_slug, campaign_title)
            
        for c_idx, chap in enumerate(chapters):
            chap_title = chap.get("name")
            session_slug = f"{c_idx+1:03d}-{slugify(chap_title)}"
            session_title = f"Sessão {c_idx+1} - {chap_title}"
            
            # Cria a Sessão e a pasta intermediária de cenas
            sess_dir, scenes_dir = create_session_structure(adv_dir, session_slug, session_title)
                
            # As subseções do capítulo viram cenas
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
                
            # Escreve as Cenas
            for s_idx, (s_title, s_entries) in enumerate(scenes):
                scene_slug = f"{s_idx+1:02d}-{slugify(s_title)}"
                scene_file = os.path.join(scenes_dir, f"{scene_slug}.md")
                
                content_markdown = ""
                for entry in s_entries:
                    res = parse_entry(entry, campaign_slug)
                    if res:
                        content_markdown += res + "\n\n"
                        
                with open(scene_file, "w") as f:
                    f.write(f"""---
title: "Cena {s_idx+1} - {s_title}"
kind: "scene"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Cena operacional para conduzir na sessão."
---

### Descrição e Elementos Importantes

{content_markdown}
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
            
            # Cria a Aventura e a pasta intermediária de sessões
            adv_dir, sessions_dir = create_adventure_structure(campaign_slug, adv_slug, chap_title)
            
            # Sob antologia, criamos uma Sessão 01 padrão contendo as cenas
            sess_slug = "001-inicio"
            session_title = "Sessão 01 - Início"
            
            # Cria a Sessão e a pasta intermediária de cenas
            sess_dir, scenes_dir = create_session_structure(adv_dir, sess_slug, session_title)
                
            # As subseções do capítulo viram cenas
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
                
            # Escreve as Cenas
            for s_idx, (s_title, s_entries) in enumerate(scenes):
                scene_slug = f"{s_idx+1:02d}-{slugify(s_title)}"
                scene_file = os.path.join(scenes_dir, f"{scene_slug}.md")
                
                content_markdown = ""
                for entry in s_entries:
                    res = parse_entry(entry, campaign_slug)
                    if res:
                        content_markdown += res + "\n\n"
                        
                with open(scene_file, "w") as f:
                    f.write(f"""---
title: "Cena {s_idx+1} - {s_title}"
kind: "scene"
draft: true
titulo_pt_br: ""
visibility: "gm"
status: "ready"
summary: "Cena operacional para conduzir na sessão."
---

### Descrição e Elementos Importantes

{content_markdown}
""")

    print(f"\n[Sucesso] Importação concluída! Campanha criada em content/campaigns/{campaign_slug}/")

if __name__ == "__main__":
    main()
