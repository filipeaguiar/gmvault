## Context

O `edit_character.py` já possui funções para ler/editar fichas e o `create_character.py` já calcula todas as estatísticas iniciais. A subida de nível é essencialmente uma re-execução parcial da criação, aplicada ao nível seguinte.

Dados do 5e.tools já disponíveis:
- `classFeature`: características por nível em `class_data["classFeature"]`
- `subclassFeature`: características de subclasse em `class_data["subclassFeature"]`
- `calculate_spell_slots()`: slots por nível
- `extract_roll_formula()`: fórmulas de dados para características

## Goals / Non-Goals

**Goals:**
- Recalcular estatísticas automaticamente (HP, proficiência, slots)
- Buscar novas características de classe no novo nível
- Oferecer Talentos/ASI quando aplicável
- Manter compatibilidade com fichas existentes

**Non-Goals:**
- Multiclasse (mantido para futura expansão)
- Mudança de classe/subclasse
- Recálculo de atributos (permanecem os mesmos)

## Decisions

**Reutilizar funções existentes do `create_character.py`**
- `calculate_skills_data()`, `calculate_saves_data()` já existem
- `select_feats_for_level()` já gerencia Talentos de nível
- `extract_roll_formula()` já extrai fórmulas de características

**Fluxo em 5 passos:**
1. Ler ficha atual e incrementar nível
2. Recalcular proficiência e HP (com rolagem ou média)
3. Buscar características novas da classe/subclasse
4. Oferecer Talentos/ASI se nível divisível por 4
5. Recalcular slots de magia e salvar

**Opção de HP:**
- Rolagem do dado de vida + CON modifier
- Valor médio (automático)
- Valor fixo (usuário digita)

## Risks / Trade-offs

- **Fichas antigas podem ter campos ausentes** → Função `level_up_character` deve ser defensiva com `.get()` e defaults
- **Características podem ter escolhas (Fighting Style, Metamagic)** → Reutilizar `prompt_choices_for_feature()` do `create_character.py`
- **Subclasses podem ter features em níveis diferentes** → Verificar ambos `classFeature` e `subclassFeature`
