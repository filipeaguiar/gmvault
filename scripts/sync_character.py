#!/usr/bin/env python3
import os
import sys
import argparse
import re
import yaml

# Adiciona o diretório raiz ao path para importar a lógica do D&D Beyond
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from import_dndbeyond import fetch_from_5etools, slugify
except ImportError as e:
    print(f"Erro ao importar funções do import_dndbeyond: {e}")
    sys.exit(1)

def parse_markdown_file(file_path):
    """
    Lê o arquivo Markdown e divide cirurgicamente o YAML frontmatter
    do corpo de texto (biografia/prosa), preservando tudo exatamente.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Expressão regular para achar o YAML delimitado por --- no topo
    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
    match = pattern.match(content)
    
    if not match:
        raise ValueError("O arquivo não possui um YAML frontmatter válido delimitado por '---'.")
        
    yaml_str = match.group(1)
    body_str = match.group(2)
    
    try:
        frontmatter = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Erro ao processar o YAML do frontmatter: {e}")
        
    return frontmatter, body_str

def save_markdown_file(file_path, frontmatter, body_str):
    """
    Grava de volta o Markdown juntando o frontmatter YAML atualizado
    e o corpo original, sem danificar comentários ou biografia.
    """
    # Converter frontmatter de volta em YAML string
    yaml_str = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    
    # Monta o conteúdo final delimitado por ---
    new_content = f"---\n{yaml_str}---\n{body_str}"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza e atualiza o compêndio local a partir de adições manuais na ficha de personagem."
    )
    parser.add_argument("character_file", type=str, help="Caminho para o arquivo Markdown do personagem (ex: content/campaigns/.../characters/pinky.md)")
    
    args = parser.parse_args()
    
    file_path = args.character_file
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)
        
    print(f"Lendo a ficha de personagem: {file_path}...")
    try:
        frontmatter, body_str = parse_markdown_file(file_path)
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        sys.exit(1)
        
    char_info = frontmatter.get("char_info", {})
    compendium_refs = frontmatter.get("compendium_refs", [])
    if not isinstance(compendium_refs, list):
        compendium_refs = []
        
    existing_refs = set(compendium_refs)
    new_refs = []
    
    # 1. Processar Magias (spells)
    spells = char_info.get("spells", [])
    if isinstance(spells, list):
        for spell in spells:
            spell_name = ""
            if isinstance(spell, dict):
                spell_name = spell.get("name")
            elif isinstance(spell, str):
                spell_name = spell
                
            if spell_name:
                slug = slugify(spell_name)
                expected_ref = f"/compendium/spells/{slug}/"
                expected_file = f"content/compendium/spells/{slug}.md"
                
                if expected_ref not in existing_refs or not os.path.exists(expected_file):
                    print(f"Detectada nova magia ou stub ausente: '{spell_name}'")
                    ref = fetch_from_5etools("spell", spell_name)
                    if ref:
                        new_refs.append(ref)
                        if isinstance(spell, dict):
                            spell["ref"] = ref
                            
    # 2. Processar Equipamentos/Itens (equipment)
    equipment = char_info.get("equipment", [])
    if isinstance(equipment, list):
        for item in equipment:
            item_name = ""
            if isinstance(item, dict):
                item_name = item.get("name")
            elif isinstance(item, str):
                item_name = item
                
            if item_name:
                slug = slugify(item_name)
                expected_ref_item = f"/compendium/items/{slug}/"
                expected_ref_magic = f"/compendium/magic-items/{slug}/"
                
                expected_file_item = f"content/compendium/items/{slug}.md"
                expected_file_magic = f"content/compendium/magic-items/{slug}.md"
                
                ref_exists = (expected_ref_item in existing_refs or 
                              expected_ref_magic in existing_refs)
                file_exists = (os.path.exists(expected_file_item) or 
                               os.path.exists(expected_file_magic))
                               
                if not ref_exists or not file_exists:
                    print(f"Detectado novo item ou stub ausente: '{item_name}'")
                    ref = fetch_from_5etools("magic_item", item_name)
                    if not ref:
                        ref = fetch_from_5etools("item", item_name)
                    if ref:
                        new_refs.append(ref)
                        if isinstance(item, dict):
                            item["ref"] = ref

    # 3. Processar Classes (classes_progression)
    classes_prog = char_info.get("classes_progression", [])
    if isinstance(classes_prog, list):
        for cl in classes_prog:
            cls_name = ""
            subcls_name = ""
            if isinstance(cl, dict):
                cls_name = cl.get("name")
                subcls_name = cl.get("subclass")
            elif isinstance(cl, str):
                cls_name = cl
                
            if cls_name:
                slug = slugify(cls_name)
                expected_ref = f"/compendium/classes/{slug}/"
                expected_file = f"content/compendium/classes/{slug}.md"
                
                if expected_ref not in existing_refs or not os.path.exists(expected_file):
                    print(f"Detectada nova classe ou stub ausente: '{cls_name}'")
                    ref = fetch_from_5etools("class", cls_name)
                    if ref:
                        new_refs.append(ref)
            
            if subcls_name:
                slug_sub = slugify(subcls_name)
                expected_ref_sub = f"/compendium/classes/{slug_sub}/"
                expected_file_sub = f"content/compendium/classes/{slug_sub}.md"
                
                if expected_ref_sub not in existing_refs or not os.path.exists(expected_file_sub):
                    print(f"Detectada nova subclasse ou stub ausente: '{subcls_name}'")
                    ref = fetch_from_5etools("subclass", subcls_name)
                    if ref:
                        new_refs.append(ref)

    # 4. Processar Talentos (feats)
    feats = char_info.get("feats", [])
    if not feats:
        feat_str = char_info.get("feat", "")
        if feat_str:
            feats = [f.strip() for f in feat_str.split(",") if f.strip()]
            
    if isinstance(feats, list):
        for feat in feats:
            feat_name = ""
            if isinstance(feat, dict):
                feat_name = feat.get("name")
            elif isinstance(feat, str):
                feat_name = feat
                
            if feat_name:
                slug = slugify(feat_name)
                expected_ref = f"/compendium/feats/{slug}/"
                expected_file = f"content/compendium/feats/{slug}.md"
                
                if expected_ref not in existing_refs or not os.path.exists(expected_file):
                    print(f"Detectado novo talento ou stub ausente: '{feat_name}'")
                    ref = fetch_from_5etools("feat", feat_name)
                    if ref:
                        new_refs.append(ref)

    # 5. Adicionar referências novas ao compendium_refs do frontmatter
    if new_refs:
        added_refs = []
        for r in new_refs:
            if r not in existing_refs and r not in added_refs:
                added_refs.append(r)
                
        if added_refs:
            compendium_refs.extend(added_refs)
            frontmatter["compendium_refs"] = sorted(list(set(compendium_refs)))
            print(f"Sincronização concluída! {len(added_refs)} nova(s) referência(s) adicionada(s) ao compendium_refs.")
            
            save_markdown_file(file_path, frontmatter, body_str)
            print("Ficha do personagem salva com sucesso.")
        else:
            print("Nenhuma referência nova precisou ser gravada na ficha do personagem.")
    else:
        print("Tudo sincronizado! Nenhuma nova entidade pendente encontrada.")

if __name__ == "__main__":
    main()
