## Why

A ficha pode exibir a progressão, mas o mestre ainda precisa consultar manualmente a classe e aplicar cada ganho ao subir de nível. Como o compêndio local já contém as classes, subclasses e features XPHB, o editor pode identificar os ganhos aplicáveis e adicioná-los ao estado operacional da ficha de forma consistente.

## What Changes

- Adicionar uma operação de subida de nível ao editor local de personagem.
- Determinar, a partir das páginas e dados XPHB locais, as features de classe e subclasse obtidas no novo nível.
- Atualizar os campos operacionais afetados, incluindo nível, bônus de proficiência, pontos de vida, espaços de magia e ações/features referenciadas.
- Apresentar escolhas obrigatórias ao usuário e não inventar decisões que dependem de escolha do jogador, como talentos, magias, invocações ou opções de feature.
- Mostrar um resumo confirmável das alterações antes de gravar a ficha.

## Capabilities

### New Capabilities
- `character-level-up`: Processo local e interativo para aplicar uma subida de nível usando progressões XPHB e conteúdo do compêndio.

### Modified Capabilities
- `edit-character-interactive`: O editor passa a oferecer e persistir a operação de subida de nível.
- `rpg-character-sheet`: A ficha passa a representar os recursos e referências operacionais adicionados durante uma subida de nível.

## Impact

Afeta `edit_character.py`, `dnd_utils.py`, dados estruturados em `char_info`, o compêndio de classes/subclasses/features e testes de criação, edição e renderização de fichas. Não requer backend ou dependências de navegador.
