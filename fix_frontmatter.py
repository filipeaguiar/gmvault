import os
import glob
import yaml

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return
        
    parts = content.split('---', 2)
    if len(parts) < 3:
        return
        
    frontmatter_text = parts[1]
    try:
        data = yaml.safe_load(frontmatter_text)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return
        
    new_frontmatter = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    new_content = f"---\n{new_frontmatter}---\n{parts[2].lstrip()}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Formatted {filepath}")

for filepath in glob.glob("content/campaigns/*/characters/*.md"):
    process_file(filepath)
