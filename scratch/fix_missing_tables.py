import os
import re
import json
from pathlib import Path
import frontmatter

# Regex de tags do 5e.tools
tag_map = {
    "spell": "spells",
    "item": "items",
    "feat": "feats",
    "condition": "conditions",
    "rule": "rules",
    "monster": "monsters",
    "class": "classes",
    "race": "species"
}

def clean_tags(text):
    if not isinstance(text, str):
        return str(text)
    
    # Substitui {@spell Aid|XPHB} por [Aid](/compendium/spells/aid/)
    def repl(match):
        tag = match.group(1)
        parts = match.group(2).split('|')
        name = parts[0]
        slug = name.lower().replace(" ", "-").replace("'", "").replace("/", "-")
        folder = tag_map.get(tag, "rules")
        return f"[{name}](/compendium/{folder}/{slug}/)"
        
    pattern = re.compile(r"\{@(spell|item|feat|condition|rule|monster|class|race) ([^\}]+)\}")
    text = pattern.sub(repl, text)
    
    # Limpa tags menores
    text = re.sub(r"\{@dice ([^\}]+)\}", r"**\1**", text)
    text = re.sub(r"\{@damage ([^\}]+)\}", r"**\1**", text)
    text = re.sub(r"\{@b ([^\}]+)\}", r"**\1**", text)
    text = re.sub(r"\{@i ([^\}]+)\}", r"*\1*", text)
    text = re.sub(r"\{@[a-zA-Z0-9]+ ([^\}]+)\}", r"\1", text)
    return text

def format_cell(cell):
    if cell is None:
        return ""
    if isinstance(cell, str):
        return clean_tags(cell)
    if isinstance(cell, (int, float)):
        return str(cell)
    if isinstance(cell, dict):
        t = cell.get("type")
        if t == "dice":
            to_roll = cell.get("toRoll", [])
            rolls = []
            for r in to_roll:
                rolls.append(f"{r.get('number')}d{r.get('faces')}")
            return ", ".join(rolls)
        elif t == "bonus":
            val = cell.get("value", 0)
            return f"+{val}" if val >= 0 else str(val)
        elif t == "cell":
            entry = cell.get("entry", "")
            return format_cell(entry)
        else:
            return clean_tags(str(cell))
    if isinstance(cell, list):
        return ", ".join(format_cell(c) for c in cell)
    return str(cell)

def render_table(table_data):
    caption = table_data.get("caption")
    col_labels = table_data.get("colLabels") or []
    rows = table_data.get("rows") or []
    
    headers = [clean_tags(h) for h in col_labels]
    markdown_lines = []
    
    if caption:
        markdown_lines.append(f"\n### Tabela: {clean_tags(caption)}")
        
    markdown_lines.append("| " + " | ".join(headers) + " |")
    markdown_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for row in rows:
        formatted_row = [format_cell(c) for c in row]
        if len(formatted_row) < len(headers):
            formatted_row += [""] * (len(headers) - len(formatted_row))
        markdown_lines.append("| " + " | ".join(formatted_row) + " |")
        
    return "\n" + "\n".join(markdown_lines) + "\n"

# 1. Corrigir tabelas de subclasses/regras na pasta content/compendium/rules/
print("=== Iniciando varredura de tabelas de características/regras ===")
rules_dir = Path("content/compendium/rules")
classes_dir = Path("content/compendium/classes")

# Varre os arquivos de cache de classe
for cache_file in classes_dir.glob("*.json_cache.json"):
    print(f"Lendo cache: {cache_file.name}")
    try:
        data = json.load(cache_file.open())
    except Exception as e:
        print(f"Erro ao ler cache {cache_file.name}: {e}")
        continue

    # Buscar características em classFeature e subclassFeature
    features = data.get("classFeature", []) + data.get("subclassFeature", [])
    for feat in features:
        name = feat.get("name")
        entries = feat.get("entries") or []
        
        # Encontrar tabelas nas entries
        tables = []
        for entry in entries:
            if isinstance(entry, dict) and entry.get("type") == "table":
                tables.append(entry)
                
        if not tables:
            continue
            
        # Calcular o slug do nome da regra
        slug = name.lower().replace(" ", "-").replace("'", "").replace("/", "-")
        rule_file = rules_dir / f"{slug}.md"
        
        # Se a regra não estiver no rules, tentar ver se está como arquivo direto ou subpasta
        if not rule_file.exists():
            # Tentar varrer caminhos com caracteres especiais
            # Ex: "Genie's Vessel" -> genies-vessel.md
            slug_alt = name.lower().replace("'", "").replace(" ", "-").replace("/", "-")
            rule_file = rules_dir / f"{slug_alt}.md"
            
        if rule_file.exists():
            content = rule_file.read_text()
            # Se o arquivo já contém uma tabela renderizada, pula para não duplicar
            if "|" in content and "---" in content:
                print(f"  [Ignorado] Regra {name} ({rule_file.name}) já possui tabela.")
                continue
                
            print(f"  [Atualizando] Injetando {len(tables)} tabela(s) em {name} ({rule_file.name})")
            
            # Renderizar as tabelas em markdown
            rendered_tables = ""
            for t in tables:
                rendered_tables += render_table(t)
                
            # Adicionar ao final do arquivo Markdown
            # Vamos preservar a biografia e cabeçalho, adicionando as tabelas antes dos delimitadores se houver ou ao final do corpo
            updated_content = content.rstrip() + "\n" + rendered_tables
            rule_file.write_text(updated_content)

print("\n=== Tabelas de regras/subclasses atualizadas com sucesso! ===\n")

# 2. Adicionar tabelas de progressão de classe nos arquivos content/compendium/classes/
print("=== Iniciando geração de tabelas de progressão de classe ===")

classes_to_process = {
    "barbarian": "Barbarian",
    "bard": "Bard",
    "monk": "Monk",
    "rogue": "Rogue",
    "sorcerer": "Sorcerer"
}

FRONT_MATTER_PATTERN = re.compile(
    rb"\A---[ \t]*(?:\r\n|\n).*?^(?:---|\.\.\.)[ \t]*(?P<body>(?:\r\n|\n)?.*)\Z",
    re.DOTALL | re.MULTILINE
)

def get_prof_bonus(lvl):
    if lvl <= 4: return "+2"
    elif lvl <= 8: return "+3"
    elif lvl <= 12: return "+4"
    elif lvl <= 16: return "+5"
    else: return "+6"

def parse_class_features_from_md(body_text):
    # Dicionário do nível (1 a 20) para a lista de features markdown
    features_by_level = {i: [] for i in range(1, 21)}
    
    # Encontrar seções "## Nível X" ou "## Level X"
    sections = re.split(r"^##\s+(?:Nível|Level)\s+(\d+)", body_text, flags=re.MULTILINE)
    
    if len(sections) > 1:
        # A primeira parte é antes do Nível 1
        for idx in range(1, len(sections), 2):
            lvl = int(sections[idx])
            sec_content = sections[idx+1]
            
            # Encontrar links markdown na seção
            # Ex: - [Rage](/compendium/rules/rage/)
            links = re.findall(r"-\s+(\[[^\]]+\]\([^\)]+\))", sec_content)
            features_by_level[lvl] = links
            
    return features_by_level

for key, class_name in classes_to_process.items():
    md_file = classes_dir / f"{key}.md"
    cache_file = classes_dir / f".class-{key}.json_cache.json"
    
    if not md_file.exists() or not cache_file.exists():
        print(f"Erro: Arquivo ou cache de {class_name} não encontrado.")
        continue
        
    print(f"Gerando tabela de classe para: {class_name}")
    
    try:
        data = json.load(cache_file.open())
    except Exception as e:
        print(f"Erro ao ler cache {cache_file.name}: {e}")
        continue
        
    # Encontrar a classe XPHB (2024) ou o fallback
    class_data = None
    for c in data.get("class", []):
        if c.get("source") == "XPHB":
            class_data = c
            break
    if not class_data and data.get("class"):
        class_data = data["class"][0]
        
    if not class_data:
        print(f"Erro: Dados de classe {class_name} não encontrados no cache.")
        continue
        
    class_table_groups = class_data.get("classTableGroups") or []
    
    # Carregar o markdown da classe
    content_bytes = md_file.read_bytes()
    match = FRONT_MATTER_PATTERN.match(content_bytes)
    if not match:
        print(f"Erro ao ler front matter do markdown {md_file.name}")
        continue
        
    body_bytes = content_bytes[match.start("body"):]
    body_text = body_bytes.decode("utf-8")
    
    # Se o markdown da classe já possui a tabela de progressão, pula
    if "| Nível |" in body_text or "| Level |" in body_text:
        print(f"  [Ignorado] Classe {class_name} já possui tabela de progressão.")
        continue
        
    # Parsear as características do Markdown por nível
    features_by_lvl = parse_class_features_from_md(body_text)
    
    # Extrair colunas e linhas extras de classTableGroups
    extra_headers = []
    # Lista de 20 listas, uma para cada nível
    extra_rows = [[] for _ in range(20)]
    
    for group in class_table_groups:
        col_labels = group.get("colLabels") or []
        rows = group.get("rows") or []
        
        for col in col_labels:
            extra_headers.append(clean_tags(col))
            
        for lvl_idx in range(20):
            if lvl_idx < len(rows):
                row_data = rows[lvl_idx]
                if isinstance(row_data, list):
                    for cell in row_data:
                        extra_rows[lvl_idx].append(format_cell(cell))
                else:
                    extra_rows[lvl_idx].append(format_cell(row_data))
            else:
                extra_rows[lvl_idx] += [""] * len(col_labels)
                
    # Construir cabeçalhos finais
    headers = ["Nível", "Bônus de Proficiência", "Características"] + extra_headers
    
    # Construir linhas da tabela
    table_lines = []
    table_lines.append("| " + " | ".join(headers) + " |")
    table_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for lvl in range(1, 21):
        lvl_str = f"{lvl}º"
        prof = get_prof_bonus(lvl)
        feats = ", ".join(features_by_lvl[lvl]) if features_by_lvl[lvl] else "—"
        
        row_cells = [lvl_str, prof, feats] + extra_rows[lvl-1]
        if len(row_cells) < len(headers):
            row_cells += [""] * (len(headers) - len(row_cells))
        table_lines.append("| " + " | ".join(row_cells) + " |")
        
    table_md = "\n## Progressão de Classe\n\n" + "\n".join(table_lines) + "\n\n"
    
    # Injetar a tabela logo no início do corpo da classe (antes do primeiro ## Nível 1)
    # Se houver algum texto introdutório, colocamos depois dele
    updated_body_text = table_md + body_text
    
    # Salvar o markdown de volta preservando o front matter
    header_bytes = content_bytes[:match.start("body")]
    md_file.write_bytes(header_bytes + updated_body_text.encode("utf-8"))
    print(f"Tabela de progressão inserida com sucesso em {md_file.name}")

print("\n=== Progresso de classes concluído com sucesso! ===")
