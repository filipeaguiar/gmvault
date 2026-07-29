import re

def main():
    path = 'layouts/partials/kinds/character.html'
    with open(path, 'r') as f:
        content = f.read()

    # 1. We need to extract the equipment iteration block.
    # It starts at: `{{ with .Params.char_info.equipment }}`
    # Ends right before `{{ if $weapons }}`
    equip_start_str = '    {{ with .Params.char_info.equipment }}\n      {{ $scratch := newScratch }}'
    equip_start_idx = content.find(equip_start_str)
    weapons_if_str = '      {{ if $weapons }}'
    weapons_if_idx = content.find(weapons_if_str, equip_start_idx)
    
    equip_logic = content[equip_start_idx:weapons_if_idx]
    
    # Let's change the start of the equip_logic to not use 'with' but a loop
    new_equip_logic = equip_logic.replace(
        '{{ with .Params.char_info.equipment }}',
        '{{ $weapons := slice }}\n  {{ $armors := slice }}\n  {{ $consumables := slice }}\n  {{ $other := slice }}\n  {{ with .Params.char_info.equipment }}'
    )
    # the end of equip_logic sets the variables, but they must override the outer ones
    new_equip_logic = new_equip_logic.replace('{{ $weapons := $scratch.Get "weapons" }}', '{{ $weapons = $scratch.Get "weapons" }}')
    new_equip_logic = new_equip_logic.replace('{{ $armors := $scratch.Get "armors" }}', '{{ $armors = $scratch.Get "armors" }}')
    new_equip_logic = new_equip_logic.replace('{{ $consumables := $scratch.Get "consumables" }}', '{{ $consumables = $scratch.Get "consumables" }}')
    new_equip_logic = new_equip_logic.replace('{{ $other := $scratch.Get "other" }}', '{{ $other = $scratch.Get "other" }}\n  {{ end }}')
    
    # Remove the equip_logic from the original string
    content = content[:equip_start_idx] + content[weapons_if_idx:]
    
    # 2. Extract the weapons HTML
    armors_if_str = '      {{ if $armors }}'
    armors_if_idx = content.find(armors_if_str)
    
    weapons_html = content[equip_start_idx:armors_if_idx]
    
    # Remove the weapons from the original string
    content = content[:equip_start_idx] + content[armors_if_idx:]
    
    # Fix the `{{ else }}` and `{{ end }}` at the end of tab-equip, because we closed the `with` block in the new_equip_logic!
    # Let's find the end of tab-equip.
    tab_equip_end_str = '    {{ else }}\n      <p>Nenhum equipamento listado.</p>\n    {{ end }}\n  </div>'
    new_tab_equip_end = '    {{ if not (or $armors $consumables $other) }}\n      <p>Nenhum equipamento listado.</p>\n    {{ end }}\n  </div>'
    content = content.replace(tab_equip_end_str, new_tab_equip_end)
    
    # 3. Find where to inject the logic and the extracted tabs.
    # We inject `new_equip_logic` right before `<div class="char-sticky-wrapper">`
    # Wait, the logic requires `$calculatedMods`, which is defined around line 80.
    # Inject it before `<!-- TAB 3: Ações -->`
    tab3_start_str = '  <!-- TAB 3: Ações -->'
    tab3_start_idx = content.find(tab3_start_str)
    
    content = content[:tab3_start_idx] + new_equip_logic + '\n' + content[tab3_start_idx:]
    
    # Now inject `weapons_html` into `tab-actions`
    tab3_end_str = '    {{ else }}\n      <p>Nenhuma ação listada.</p>\n    {{ end }}\n  </div>'
    new_tab3_end_str = '    {{ else }}\n      <p>Nenhuma ação listada.</p>\n    {{ end }}\n\n    {{ partial "helpers/character-spell-slots.html" . }}\n\n' + weapons_html + '\n    {{ if $hasSpells }}\n      <div style="margin-top: 30px;">{{ partial "helpers/character-spells.html" . }}</div>\n    {{ end }}\n\n  </div>'
    
    content = content.replace(tab3_end_str, new_tab3_end_str)
    
    # 4. Remove TAB 5 (Grimoire)
    tab5_start_str = '  <!-- TAB 5: Grimório (only if has spells) -->'
    tab6_start_str = '  <!-- TAB 6: Classe -->'
    tab5_start_idx = content.find(tab5_start_str)
    tab6_start_idx = content.find(tab6_start_str)
    
    content = content[:tab5_start_idx] + content[tab6_start_idx:]
    
    # 5. Remove the Grimoire tab button
    grimoire_btn_str = '      {{ if $hasSpells }}\n      <button class="char-tab-btn" onclick="openCharTab(event, \'tab-grimoire\')" title="Grimório"><i class="ra ra-book" style="font-size: 1.3em;"></i></button>\n      {{ end }}\n'
    content = content.replace(grimoire_btn_str, '')
    
    with open(path, 'w') as f:
        f.write(content)
    
    print("Done refactoring character.html")

if __name__ == '__main__':
    main()
