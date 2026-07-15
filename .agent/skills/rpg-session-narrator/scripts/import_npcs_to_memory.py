#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
from pathlib import Path

def import_npcs(campaign_slug, memory_path=None, project_root=None):
    if not project_root:
        project_root = str(Path(__file__).resolve().parents[4])
    
    if not memory_path:
        memory_path = os.path.join(project_root, ".agent", "skills", "rpg-session-narrator", "memory.yaml")
        
    npcs_dir = os.path.join(project_root, "content", "campaigns", campaign_slug, "npcs")
    
    if not os.path.exists(npcs_dir):
        print(f"Erro: Diretório de NPCs não encontrado em {npcs_dir}", file=sys.stderr)
        return False
        
    if not os.path.exists(memory_path):
        print(f"Erro: Arquivo de memória não encontrado em {memory_path}", file=sys.stderr)
        return False
        
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory = yaml.safe_load(f)
    except Exception as e:
        print(f"Erro ao carregar a memória: {e}", file=sys.stderr)
        return False
        
    if not memory:
        memory = {}
        
    if "npcs" not in memory or memory["npcs"] is None:
        memory["npcs"] = []
        
    existing_npc_names = {n.get("canonical_name", "").lower(): n for n in memory["npcs"]}
    
    imported_count = 0
    for filename in os.listdir(npcs_dir):
        if filename == "_index.md" or not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(npcs_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            parts = content.split('---')
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                if not frontmatter:
                    continue
                    
                title = frontmatter.get("title")
                if title:
                    title_clean = title.strip()
                    if title_clean.lower() not in existing_npc_names:
                        summary = frontmatter.get("summary") or frontmatter.get("stats_meta") or ""
                        new_npc = {
                            "canonical_name": title_clean,
                            "aliases": [],
                            "common_transcription_errors": [],
                            "pronouns": "",
                            "description": summary,
                            "role": "npc",
                            "notes": f"Importado automaticamente do arquivo {filename}"
                        }
                        memory["npcs"].append(new_npc)
                        existing_npc_names[title_clean.lower()] = new_npc
                        imported_count += 1
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}", file=sys.stderr)
            
    try:
        with open(memory_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(memory, f, allow_unicode=True, sort_keys=False)
        print(f"Sucesso: {imported_count} NPCs importados para a memória persistente.")
        return True
    except Exception as e:
        print(f"Erro ao salvar a memória atualizada: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    campaign = "journeys-through-the-radiant-citadel"
    if len(sys.argv) > 1:
        campaign = sys.argv[1]
    import_npcs(campaign)
