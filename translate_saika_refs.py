import os
import yaml
import subprocess

saika_file = 'content/campaigns/journeys-through-the-radiant-citadel/characters/saika.md'

with open(saika_file, 'r') as f:
    content = f.read()
    if content.startswith('---'):
        end = content.find('\n---', 3)
        yaml_content = content[3:end]
        data = yaml.safe_load(yaml_content)
        refs = data.get('compendium_refs', [])

        for ref in refs:
            rel_path = ref.strip('/')
            target1 = f"content/{rel_path}.md"
            target2 = f"content/{rel_path}/_index.md"
            target = target1 if os.path.exists(target1) else (target2 if os.path.exists(target2) else None)
            
            if target:
                print(f"Translating {target}")
                subprocess.run(["python3", "translate_drafts.py", "--scope", "compendium", "--path", target, "--translate-frontmatter", "--apply"])
            else:
                print(f"Not found: {ref}")
