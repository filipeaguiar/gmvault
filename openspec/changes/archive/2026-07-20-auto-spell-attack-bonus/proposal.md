## Why

As fichas já enviam a fórmula de ataque mágico ao Dice+, mas dependem de `char_info.spell_attack_bonus` preenchido manualmente. Os dados estruturados já contêm o bônus de proficiência e os modificadores de atributo necessários para calcular automaticamente o ataque de magias como *Eldritch Blast*.

## What Changes

- Calcular o bônus de ataque mágico de fichas de conjurador de classe única a partir de proficiência e modificador do atributo de conjuração.
- Persistir o atributo de conjuração no perfil gerado pelos fluxos locais de criação e edição de personagem.
- Usar o bônus explícito `spell_attack_bonus` como sobrescrita quando ele representar um valor configurado para a ficha.
- Preservar compatibilidade de renderização para fichas legadas que não tenham atributo de conjuração resolvível.
- Continuar enviando ao Dice+ a notação final já calculada, sem alterar o protocolo da extensão.
- Delimitar o primeiro escopo para classe única; cálculo por magia para multiclasse e modificadores de dano como *Agonizing Blast* ficam fora desta mudança.

## Capabilities

### New Capabilities
- `automatic-spell-attack-bonus`: Resolve e expõe o bônus de ataque mágico de uma ficha a partir de seus dados estruturados de conjuração.

### Modified Capabilities
- `interactive-character-sheet-spells`: Os controles de ataque de magia passam a aceitar bônus derivado automaticamente além do valor explícito legado.
- `create-character-interactive`: Novas fichas persistem o atributo de conjuração necessário para o cálculo automático.
- `edit-character-interactive`: Edições e sincronizações preservam ou atualizam o atributo de conjuração da ficha.

## Impact

Afeta `dnd_utils.py`, `create_character.py`, `edit_character.py`, o partial Hugo `layouts/partials/helpers/spell-rolls.html`, as fichas geradas e os testes de perfil de conjuração e renderização de magias. Não introduz dependências, backend ou alterações no protocolo Owlbear/Dice+.
