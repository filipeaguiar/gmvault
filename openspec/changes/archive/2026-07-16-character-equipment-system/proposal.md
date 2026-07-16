## Why

O inventário e a aba de equipamentos da ficha de personagem atualmente são estáticos, sem detalhes importantes de mecânica (como alcance, propriedades de armas, categoria de armadura) e não alteram dinamicamente os atributos calculados da ficha (como Força ou CA). Esta proposta visa integrar a extração detalhada de itens no importador e processar semanticamente modificadores de equipamentos equipados (como bônus de CA ou modificações de atributos).

## What Changes

- **Importador Avançado de Itens**: Atualizar o script `import_dndbeyond.py` para obter e mapear metadados adicionais de itens de inventário, incluindo propriedades de combate (propriedades, alcance, tipo de dano), categorias e modificadores mágicos (modificadores de atributos e CA).
- **Semântica de Equipamento Equipado**: Alterar o cálculo de atributos e CA no template da ficha (`layouts/partials/kinds/character.html`) para aplicar dinamicamente os efeitos de itens equipados (ex: Luvas de Força de Gigante definindo Força para 21, ou Escudos/Armaduras aplicando bônus e fórmulas de CA).
- **Interface da Aba de Equipamentos**: Expandir a aba de equipamentos para exibir visualmente propriedades de armas (Finesse, Arremesso, etc.), alcance, categoria e seções claras para itens ativos/equipados e inativos, com estados visuais premium.
- **Formato Estruturado no Frontmatter**: Padronizar as entradas de equipamentos no YAML frontmatter sob `.Params.char_info.equipment` contendo atributos limpos e tipados.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- `rpg-character-sheet`: Exigir que a ficha de personagem calcule dinamicamente CA e atributos com base em modificadores semânticos de equipamentos equipados, e exiba propriedades detalhadas na aba de Equipamentos.
- `import-tools`: Exigir que o importador de personagem extraia propriedades avançadas e modificadores de equipamentos do inventário do D&D Beyond e os grave de forma estruturada no frontmatter.

## Impact

- **layouts/partials/kinds/character.html**: Refatoração do cálculo inicial de atributos (para permitir sobreposições/bônus de itens) e do cálculo da CA. Atualização do layout da aba "Equipamentos".
- **import_dndbeyond.py**: Inclusão de lógicas de extração e mapeamento de propriedades de armas, armaduras e modificadores mágicos.
- **assets/css/character-sheet.css**: Estilização dos novos blocos e metadados na aba de equipamentos.
