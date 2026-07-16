## Context

Atualmente, o script `create_character.py` baixa e cacheia o índice e dados básicos de classes do 5e.tools (como dado de vida e perícias), mas não aproveita a tabela de progressão de habilidades de classe e subclasse contidas nos JSONs detalhados (ex: `class-fighter.json`). As características de classe são representadas no 5e.tools como objetos sob as chaves `classFeature` e `subclassFeature`.
Este design propõe a implementação de um parser para essas estruturas para mapear e extrair as habilidades correspondentes ao nível do personagem, oferecendo prompts de escolha quando aplicável e gravando-as no compêndio e na ficha de forma automatizada.

## Goals / Non-Goals

**Goals:**
- Mapear e extrair automaticamente todas as características de classe e subclasse para o nível escolhido do personagem a partir dos dados estruturados do 5e.tools.
- Implementar prompts de escolha no terminal interativo para características que oferecem opções (ex: Fighting Styles, Eldritch Invocations).
- Gerar stubs no compêndio local em `content/compendium/rules/` para características ausentes.
- Associar as características extraídas às ações e referências de compêndio da ficha gerada.

**Non-Goals:**
- Validar pré-requisitos complexos de talentos ou habilidades multiclasse de forma estrita.
- Atualizar retroativamente fichas existentes fora do fluxo de criação.
- Implementar uma interface gráfica complexa para a escolha de características.

## Decisions

### 1. Parsear `classFeature` e `subclassFeature` do 5e.tools
As características da classe e subclasse serão extraídas dos arquivos JSON baixados do 5e.tools. Mapearemos o array de `classFeature` e `subclassFeature` correspondendo ao campo `level` de cada característica com o nível do personagem (menor ou igual).

### 2. Fluxo de Escolhas Interativas no Terminal
Para características que oferecem escolhas (detectadas por chaves de `choose` ou nomes específicos no JSON de classe), o script listará as opções disponíveis e solicitará a escolha numérica ao usuário, com suporte a fallback manual (digitação simples).

### 3. Extração e Detecção de Fórmulas de Rolagem
O parser de características de classe e subclasse SHALL inspecionar as descrições ou propriedades textuais das habilidades à procura de notações de dados válidas (como `1d10`, `2d6`, etc.) para preenchê-las automaticamente no campo `roll_formula` da ação. Ex: "Sneak Attack" mapeia a progressão de dados a cada nível ímpar.

### 4. Suporte a `roll_formula` nos Layouts de Ações da Ficha
O template de exibição de personagem (`layouts/partials/kinds/character.html`) será atualizado na seção de Ações/Recursos para verificar a presença do campo `roll_formula` nas ações. Caso esteja presente, renderizará um elemento com o atributo `data-roll-notation`, permitindo o aprimoramento progressivo da rolagem.

### 5. Geração e Vinculação de Regras do Compêndio
Características serão salvas como regras com `kind: rule` e `visibility: public`. O script usará a função utilitária `fetch_from_5etools` estendida para gerar esses stubs se não existirem no compêndio local.

## Risks / Trade-offs

- **[Risco]** Estrutura irregular ou complexa do JSON de classes do 5e.tools quebrando o parser.  
  *Mitigação:* Implementar um bloco try-catch robusto que, em caso de erro de parsing, apenas registra o título da característica como string simples e segue para a próxima, sem interromper o script de criação.
- **[Risco]** Sobrescrever regras do compêndio local que foram traduzidas ou refinadas manualmente.  
  *Mitigação:* Usar `publish_compendium_page` que verifica se o arquivo já existe no caminho local antes de tentar baixar ou gerar novamente o stub.
