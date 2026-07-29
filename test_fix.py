import re

with open('layouts/partials/kinds/character.html', 'r') as f:
    content = f.read()

start_str = '    {{ with .Params.char_info.actions }}\n      {{ range . }}\n        {{ $name := .name | default "" }}\n'
end_str = '      </div>\n    </div>\n    {{ end }}\n'

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

consumables_block = content[start_idx:end_idx]

content = content[:start_idx] + content[end_idx:]

target_str = '        {{ $consumablesScratch.Add "names" (slice (lower $name)) }}\n      {{ end }}\n    {{ end }}\n'
target_idx = content.find(target_str) + len(target_str)

content = content[:target_idx] + consumables_block + content[target_idx:]

with open('layouts/partials/kinds/character.html', 'w') as f:
    f.write(content)
