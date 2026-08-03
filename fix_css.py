import re

with open("assets/css/character-sheet.css", "r") as f:
    content = f.read()

# The media query starts at @media (max-width: 600px), html.vtt-iframe {
# We want to find the closing brace at the very end of the file.
# And we want to move it up.
# Looking at the file, the last `}` is at the very end.

lines = content.split('\n')

# Find the last brace
last_brace_idx = -1
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip() == '}':
        last_brace_idx = i
        break

# Find the place to insert the new brace
# We'll insert it right after the `.card-item-title-row` rule that is part of the mobile spacing:
#   .card-item-title-row {
#     margin-bottom: 2px !important;
#   }
# Let's find this exact block
target_idx = -1
for i in range(len(lines)):
    if ".card-item-title-row" in lines[i] and "margin-bottom: 2px !important;" in lines[i+1]:
        target_idx = i + 2 # line with `  }`
        break

if target_idx != -1 and last_brace_idx != -1:
    lines.pop(last_brace_idx)
    lines.insert(target_idx + 1, "}\n/* Moved from bottom to close media query earlier */")
    
    with open("assets/css/character-sheet.css", "w") as f:
        f.write('\n'.join(lines))
    print("Fixed!")
else:
    print(f"Could not find target block. target_idx: {target_idx}, last_brace_idx: {last_brace_idx}")
