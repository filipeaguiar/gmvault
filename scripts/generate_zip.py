import os
import glob
import zipfile
from pathlib import Path

def generate_characters_zip():
    public_dir = Path("public/exports/forge")
    static_dir = Path("static/exports/forge")
    static_dir.mkdir(parents=True, exist_ok=True)
    
    zip_path = static_dir / "personagens.zip"
    print(f"Gerando ZIP em: {zip_path}")
    
    # Encontrar todos os JSONs individuais de personagens na pasta de build public/
    json_files = glob.glob(str(public_dir / "*.json"))
    
    # Filtrar apenas os personagens (excluir statblocks.json e test-creatures.json)
    char_files = [
        f for f in json_files 
        if "statblocks.json" not in f and "test-creatures.json" not in f and "personagens.zip" not in f
    ]
    
    if not char_files:
        print("Aviso: Nenhum arquivo JSON de personagem encontrado em public/exports/forge/. Execute o build do Hugo antes.")
        return False
        
    with zipfile.ZipFile(zip_path, "w") as z:
        for f in char_files:
            filename = os.path.basename(f)
            z.write(f, filename)
            print(f"  Adicionado: {filename}")
            
    print(f"ZIP gerado com sucesso contendo {len(char_files)} personagens.")
    return True

if __name__ == "__main__":
    generate_characters_zip()
