## Why

Atualmente, ao criar um personagem manualmente através do script `create_character.py`, o usuário precisa digitar manualmente todas as habilidades e características de classe no campo de ações ou editá-las depois na ficha. Automatizar a extração dessas características diretamente dos dados estruturados do 5e.tools para o nível selecionado garante fichas mais ricas, completas e alinhadas ao compêndio local sem esforço manual redundante.

## What Changes

- **Extração Automática de Características**: Integrar a leitura das tabelas de progressão de classe do 5e.tools (usando o nível do personagem) para identificar as habilidades de classe e subclasse concedidas.
- **Extração de Fórmulas de Rolagem (Dice+)**: Identificar fórmulas de dados estruturadas nas características de classe/subclasse (ex: Sneak Attack, Second Wind) e mapeá-las na ficha para habilitação automática do Dice+.
- **Resolução de Escolhas Interativas**: Apresentar prompts interativos quando uma habilidade da classe exigir escolhas (como Estilos de Luta, Invocações de Bruxo, Metamagia ou outras opções de classe).
- **Geração de Conteúdo no Compêndio**: Gerar stubs correspondentes em `content/compendium/rules/` para cada habilidade extraída e associá-los automaticamente a `compendium_refs` do personagem.
- **Populamento de Ações na Ficha**: Inserir as habilidades operacionais no campo `char_info.actions` da ficha gerada, contendo referências corretas ao compêndio e suas respectivas fórmulas de rolagem.

## Capabilities

### New Capabilities

- `extract-class-features`: Download, parsing, escolhas interativas e geração de conteúdo/referências de características de classe e subclasse com base nos dados do 5e.tools para o nível do personagem.

### Modified Capabilities

- None

## Impact

- `create_character.py`: Fluxo de criação estendido para realizar o download dos arquivos de classe detalhados, parsear a progressão de nível, exibir escolhas e salvar as ações/referências.
- `dnd_utils.py`: Funções utilitárias adicionadas ou modificadas para lidar de forma consistente com dados do 5e.tools de classes.
- Conteúdo: Criação de arquivos Markdown na pasta `content/compendium/rules/` para as características mapeadas.
