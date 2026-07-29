import re

with open('layouts/partials/kinds/character.html', 'r') as f:
    content = f.read()

# Locate the actions block
actions_start_str = '    {{ with .Params.char_info.actions }}'
actions_end_str = '    {{ else }}\n      <p>Nenhuma ação listada.</p>\n    {{ end }}\n'

actions_start_idx = content.find(actions_start_str)
actions_end_idx = content.find(actions_end_str, actions_start_idx) + len(actions_end_str)

actions_block = content[actions_start_idx:actions_end_idx]

# Remove it from current location
content = content[:actions_start_idx] + content[actions_end_idx:]

# Find where to place it: after spells, before the closing </div> of tab-actions.
spells_end_str = '    {{ if $hasSpells }}\n      <div style="margin-top: 30px;">{{ partial "helpers/character-spells.html" . }}</div>\n    {{ end }}\n\n  </div>'
new_spells_end_str = '    {{ if $hasSpells }}\n      <div style="margin-top: 30px;">{{ partial "helpers/character-spells.html" . }}</div>\n    {{ end }}\n\n' + actions_block + '\n  </div>'

content = content.replace(spells_end_str, new_spells_end_str)

with open('layouts/partials/kinds/character.html', 'w') as f:
    f.write(content)
