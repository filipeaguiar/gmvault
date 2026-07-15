## Context

Atualmente, os arquivos de fichas de personagens no gmvault são gerados e sobrescritos integralmente pelo importador D&D Beyond (`import_dndbeyond.py`). No entanto, os mestres e jogadores precisam de flexibilidade para editar suas fichas à mão livre diretamente nos arquivos Markdown locais no repositório (ex: adicionar magias no grimório, equipar novos itens ou subir níveis). Um novo utilitário independente se faz necessário para identificar alterações na ficha e sincronizar o compêndio de RPG de forma autônoma por meio do download de metadados do 5e.tools.

## Goals / Non-Goals

**Goals:**
- Criar um script Python `scripts/sync_character.py` que aceita um arquivo de personagem Markdown.
- Identificar novos itens sob as listas `spells`, `equipment`, `classes_progression` ou `feats` no YAML do personagem.
- Buscar e baixar stubs ausentes a partir do 5e.tools para o compêndio local.
- Atualizar a chave `compendium_refs` da ficha do personagem, registrando as novas referências.
- Preservar integralmente quaisquer outros campos (como atributos, PV, etc.) e a seção de biografia em prosa abaixo do YAML frontmatter.

**Non-Goals:**
- Recalcular atributos finais ou interagir com a API do D&D Beyond (esse fluxo de geração permanece restrito ao `import_dndbeyond.py`).
- Traduzir os stubs baixados em tempo de execução (as páginas baixadas continuam como rascunhos em inglês para posterior processamento pelo `translate_drafts.py`).

## Decisions

### 1. Script de Sincronização Desacoplado (`sync_character.py`)
- **Opção Escolhida**: Desenvolvimento de um script Python isolado no diretório `scripts/` do projeto. O script carrega o frontmatter, compara as entradas com a pasta local `content/compendium/` e a lista `compendium_refs`, executa o download das faltantes usando a lógica do 5e.tools e re-grava o Markdown.
- **Alternativa Considerada**: Integrar a verificação de links de compêndio ausentes diretamente no build do Hugo. Embora automática, esta opção é inviável, pois o Hugo é um compilador de arquivos estáticos puramente declarativo e não possui mecanismos para realizar requisições HTTP ou gravar novos arquivos Markdown locais em tempo de compilação.

## Risks / Trade-offs

- **[Risco] Corrupção do Formato do Markdown ao Re-gravar o Frontmatter**: Ao atualizar o YAML frontmatter e salvar o arquivo, bibliotecas automáticas de gravação podem apagar comentários, reordenar campos ou excluir a biografia em prosa que existia abaixo do bloco de delimitadores `---`.
  - *Mitigação*: O script `sync_character.py` lerá o arquivo em texto puro, localizará cirurgicamente as duas ocorrências de `---` que delimitam o frontmatter, fará o parse do YAML apenas dessa seção usando PyYAML, atualizará o campo `compendium_refs` e, ao re-escrever o arquivo, concatenará o novo bloco frontmatter YAML formatado com o texto original da biografia (que é mantido guardado na memória e gravado integralmente sem alteração de um único caractere).
