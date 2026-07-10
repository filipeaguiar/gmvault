## Why

Atualmente, o script de importação de campanhas (`import_campaign.py`) apenas gera arquivos de "stub" vazios para localidades, sem conteúdo útil ou associação aos mapas correspondentes disponíveis nos dados de origem (5e.tools). Isso exige trabalho manual exaustivo para catalogar os pontos de interesse e fazer o upload de mapas. Automatizar o enriquecimento dessas localidades e identificar/vincular os mapas trará ganho de produtividade e consistência nas campanhas importadas.

## What Changes

- **Enriquecimento de Localidades**: Modificar o gerador de localidades para incluir informações adicionais no front matter ou corpo (ex: relação de cenas/sub-áreas associadas, descrição inicial da seção quando disponível).
- **Heurística de Detecção de Mapas**: Implementar lógica para identificar imagens de mapas com base no título da imagem (ex: "map", "player map", "tactical map") e nos metadados da aventura.
- **Geração de Handouts de Mapas**: Tratar imagens de mapas identificadas como novos handouts de forma automatizada, atribuindo visibilidade apropriada baseada no tipo de mapa (`gm` para mapas com grade/mestre, `players` para mapas livres de spoiler).
- **Vínculo Automático de Mapas**: Associar os handouts de mapas gerados às respectivas localidades e cenas correspondentes em seus campos front matter `handouts`.
- **Preservação de Compatibilidade**: Garantir que as importações legadas ou novas que não possuam mapas continuem funcionando normalmente sem quebras.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `import-tools`: Definir novos requisitos para que os scripts de importação cataloguem localizações de forma enriquecida e vinculem seus respectivos mapas como handouts estruturados.

## Impact

- `import_campaign.py`: Principal script modificado para implementar as heurísticas de localização e download/associação de mapas.
- Arquitetura de conteúdo: Criação de novos arquivos markdown de handout em `content/campaigns/<campaign-slug>/handouts/` dedicados aos mapas.
- Layouts e templates Hugo: Adaptação leve opcional nos layouts de localidade/cena para renderizar imagens de mapa associadas ou listar as sub-áreas (cenas) pertencentes àquela localidade.
