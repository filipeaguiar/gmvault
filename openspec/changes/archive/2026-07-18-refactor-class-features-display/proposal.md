## Why

A seção de "Habilidades de Classe" na ficha do personagem usa um layout simples (`class-feature-card`) que não segue o padrão visual das outras seções (equipamentos, magias). Isso cria inconsistência visual e dificulta a identificação rápida de informações como nível, fonte e tipo de característica.

## What Changes

- Refatorar `class-feature-card` para usar a mesma estrutura de `equipment-card`
- Adicionar ícone estilizado com container colorido
- Adicionar badges para nível e fonte (classe/subclasse)
- Usar `equipment-stat-grid` para metadados quando aplicável
- Manter compatibilidade com conteúdo existente do compêndio

## Capabilities

### New Capabilities

(nenhuma)

### Modified Capabilities

- `character-sheet`: Seção de características de classe usa padrão visual de equipment-card

## Impact

- `layouts/partials/kinds/character.html`: Atualizar HTML da seção de features
- `assets/css/character-sheet.css`: Adicionar estilos para feature-card no novo padrão
- Nenhum dado de personagem é afetado
