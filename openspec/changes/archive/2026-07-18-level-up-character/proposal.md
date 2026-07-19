## Why

O `edit_character.py` permite adicionar equipamentos e magias, mas não possui opção para subir de nível. Jogadores precisam manualmente atualizar `level`, `class_level`, `proficiency_bonus`, `hp`, `hp_max`, `hp_current`, `spell_slots`, `actions` e outras estatísticas — processo propenso a erros e que ignora novas características de classe.

## What Changes

- Adicionar opção "Subir de nível" no menu do `edit_character.py`
- Recalcular automaticamente: nível, bônus de proficiência, HP, slots de magia
- Buscar e exibir novas características de classe/subclasse disponíveis no novo nível
- Oferecer escolha de Talentos/ASI nos níveis apropriados (4, 8, 12, 16, 19)
- Atualizar ações e referências do compêndio

## Capabilities

### New Capabilities

- `level-up`: Fluxo interativo de subida de nível que recalcular estatísticas e aplica características novas

### Modified Capabilities

(nenhuma mudança em specs existentes)

## Impact

- `edit_character.py`: Nova função `level_up_character()` e entrada no menu
- `dnd_utils.py`: Funções auxiliares para buscar características por nível
- Arquivos de personagem: Campos `level`, `class_level`, `proficiency_bonus`, `hp*`, `spell_slots`, `actions`, `feature_actions` são atualizados
