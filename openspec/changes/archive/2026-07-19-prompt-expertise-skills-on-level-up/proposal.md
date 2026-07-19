## Why

A progressão de nível já recalcula bônus de perícias, mas não registra a escolha de Expertise quando essa característica é adquirida. Sem uma pergunta explícita, a ficha não reflete quais duas perícias recebem o dobro do bônus de proficiência.

## What Changes

- Detectar a característica de classe `Expertise` recebida no nível de destino.
- Solicitar exatamente duas perícias já proficientes e ainda sem Expertise.
- Marcar as escolhas na ficha e recalcular seus bônus com o dobro da proficiência.
- Impedir a confirmação da subida de nível caso a escolha obrigatória seja cancelada ou inválida.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `character-level-up`: exigir e aplicar a seleção de perícias para Expertise durante a subida de nível.
- `edit-character-interactive`: apresentar a escolha de Expertise no fluxo interativo de subida de nível.

## Impact

Afeta `edit_character.py`, a representação `char_info.skills` das fichas locais e os testes de plano e execução de subida de nível. Não altera dependências externas nem a estrutura Markdown fora do front matter da ficha.
