import os
import subprocess
import json
from pathlib import Path
import frontmatter

# Importar as funções de leitura e salvamento seguro do edit_character.py
import sys
sys.path.append(os.getcwd())
from edit_character import read_body_bytes, save_character

char_dir = Path("content/campaigns/journeys-through-the-radiant-citadel/characters")
characters = ["detios-canto-baixo", "durin", "einvor", "nyx-clair", "pinky", "violeta"]

# 1. Equipar todos os itens nas fichas markdown dos personagens no disco e adicionar Rapier ao Pinky
print("--- Passo 1: Atualizando fichas Markdown dos personagens no disco ---")
for slug in characters:
    filepath = char_dir / f"{slug}.md"
    if not filepath.exists():
        print(f"Aviso: arquivo {filepath} não encontrado.")
        continue
        
    post = frontmatter.load(filepath)
    char_info = post.get("char_info")
    if not isinstance(char_info, dict):
        print(f"Aviso: {slug}.md não possui char_info.")
        continue
        
    # Equipar todos os equipamentos
    equipment = char_info.get("equipment") or []
    if isinstance(equipment, list):
        for item in equipment:
            if isinstance(item, dict):
                item["equipped"] = True
                
        # Caso especial do Pinky: adicionar Rapier
        if slug == "pinky":
            has_rapier = False
            for item in equipment:
                if isinstance(item, dict) and item.get("name", "").lower() == "rapier":
                    item["equipped"] = True
                    has_rapier = True
            if not has_rapier:
                equipment.append({
                    "equipped": True,
                    "name": "Rapier",
                    "quantity": 1,
                    "ref": "/compendium/items/rapier/"
                })
                print("Adicionada Rapier aos equipamentos de Pinky no Markdown.")
                
            # Adicionar ref ao compendium_refs do Pinky
            refs = post.get("compendium_refs") or []
            if "/compendium/items/rapier/" not in refs:
                refs.append("/compendium/items/rapier/")
                post["compendium_refs"] = refs

    char_info["equipment"] = equipment
    
    # Salvar a ficha usando o método seguro que preserva o corpo original bytes
    body_bytes = read_body_bytes(filepath)
    save_character(filepath, post, body_bytes)
    print(f"Ficha {slug}.md salva com sucesso (itens equipados).")

# 2. Modificar temporariamente os layouts para o Hugo gerar a exportação completa de personagens
print("\n--- Passo 2: Modificando temporariamente layouts do Hugo ---")

index_path = Path("layouts/index.forge.json")
index_backup = index_path.read_text()

statblock_path = Path("layouts/partials/helpers/forge_statblock.html")
statblock_backup = statblock_path.read_text()

# Escrever layouts temporários
temp_index_content = """{{- $characters := slice -}}
{{- $monsters := slice -}}
{{- range site.Pages -}}
  {{- $kind := partial "helpers/kind.html" . -}}
  {{- if eq $kind "character" -}}
    {{- $characters = $characters | append . -}}
  {{- else if eq $kind "monster" -}}
    {{- $monsters = $monsters | append . -}}
  {{- end -}}
{{- end -}}

{{- $characters = sort (sort (sort $characters "Permalink") "Title") "Weight" -}}
{{- $monsters = sort (sort (sort $monsters "Permalink") "Title") "Weight" -}}
{{- $records := slice -}}
{{- range $characters -}}
  {{- $records = $records | append (partial "helpers/forge_statblock.html" .) -}}
{{- end -}}
{{- range $monsters -}}
  {{- $records = $records | append (partial "helpers/forge_statblock.html" .) -}}
{{- end -}}
{{- $records | jsonify (dict "indent" "  ") -}}
"""
index_path.write_text(temp_index_content)

temp_statblock_content = statblock_backup.replace(
    "{{- $inParty := false -}}",
    "{{- $inParty := $isCharacter -}}"
).replace(
    '"com.battle-system.forge/in-party" false',
    '"com.battle-system.forge/in-party" $inParty'
).replace(
    '"favorite" false',
    '"favorite" $inParty'
)
statblock_path.write_text(temp_statblock_content)

# 3. Rodar build do Hugo para compilar o JSON temporário com os personagens
print("\n--- Passo 3: Compilando exportação temporária com Hugo ---")
try:
    subprocess.run(["hugo", "--gc", "--minify"], check=True)
    print("Hugo compilado com sucesso.")
except subprocess.CalledProcessError as e:
    print("Erro ao compilar o Hugo:", e)
    # Restaurar layouts antes de fechar
    index_path.write_text(index_backup)
    statblock_path.write_text(statblock_backup)
    sys.exit(1)

# 4. Extrair os personagens individuais do JSON compilado e salvá-los separadamente
print("\n--- Passo 4: Separando arquivos JSON individuais de cada personagem ---")
statblocks_file = Path("public/exports/forge/statblocks.json")
if not statblocks_file.exists():
    print("Erro: public/exports/forge/statblocks.json não existe.")
    # Restaurar layouts
    index_path.write_text(index_backup)
    statblock_path.write_text(statblock_backup)
    sys.exit(1)

data = json.load(statblocks_file.open())

export_dir = Path("static/exports/forge")
export_dir.mkdir(parents=True, exist_ok=True)

# Mapeamento do nome amigável do personagem para o seu nome de arquivo JSON correspondente
slug_map = {
    "Detios Canto Baixo": "detios",
    "Durin": "durin",
    "Einvor": "einvor",
    "Nyx Clair": "nyx",
    "Nix Clair": "nyx",
    "Pinky": "pinky",
    "Violeta": "violeta"
}

for item in data:
    name = item.get("name")
    if name in slug_map:
        file_slug = slug_map[name]
        dest_file = export_dir / f"{file_slug}.json"
        
        # Como queremos exportar individualmente como um dicionário JSON único (ou como um array contendo um único item)
        # O Forge suporta importar tanto um objeto individual quanto um array de objetos.
        # Vamos salvar como um dicionário individual único (objeto) para facilitar o import individual limpo.
        with open(dest_file, "w") as f:
            json.dump(item, f, indent=2, ensure_ascii=False)
        print(f"Salvo arquivo JSON individual de {name} em: {dest_file}")

# 5. Restaurar layouts originais de produção (monsters-only)
print("\n--- Passo 5: Restaurando layouts de produção (apenas monstros) ---")
index_path.write_text(index_backup)
statblock_path.write_text(statblock_backup)

# 6. Rodar o build final do Hugo para copiar os novos arquivos estáticos individuais para a pasta public
print("\n--- Passo 6: Compilando build final de produção com Hugo ---")
try:
    subprocess.run(["hugo", "--gc", "--minify"], check=True)
    print("Build final de produção compilado com sucesso.")
except subprocess.CalledProcessError as e:
    print("Erro ao compilar o build final:", e)
    sys.exit(1)

print("\n=== Automação concluída com sucesso! ===")
