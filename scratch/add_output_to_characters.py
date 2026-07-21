import os
import sys
from pathlib import Path
import frontmatter

sys.path.append(os.getcwd())
from edit_character import read_body_bytes, save_character

char_dir = Path("content/campaigns/journeys-through-the-radiant-citadel/characters")
characters = ["detios-canto-baixo", "durin", "einvor", "nyx-clair", "pinky", "violeta"]

print("--- Adicionando 'outputs: [HTML, ForgeChar]' aos personagens ---")
for slug in characters:
    filepath = char_dir / f"{slug}.md"
    if not filepath.exists():
        print(f"Aviso: {filepath} não existe.")
        continue
        
    post = frontmatter.load(filepath)
    post.metadata["outputs"] = ["HTML", "ForgeChar"]
    
    # Gravar usando o método seguro
    body_bytes = read_body_bytes(filepath)
    save_character(filepath, post, body_bytes)
    print(f"Atualizado outputs de {slug}.md")

print("--- Processamento concluído ---")
