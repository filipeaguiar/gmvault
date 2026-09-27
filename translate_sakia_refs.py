import os
import yaml
import subprocess

sakia_file = None
for root, dirs, files in os.walk('content/campaigns'):
    for file in files:
        if file.lower().startswith('sakia') and file.endswith('.md'):
            sakia_file = os.path.join(root, file)
            break
    if sakia_file:
        break

if not sakia_file:
    print("Sakia file not found")
    exit(1)

print(f"Found {sakia_file}")

with open(sakia_file, 'r') as f:
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
