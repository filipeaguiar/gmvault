## Why

Conteúdo importado de 5e.tools e D&D Beyond frequentemente entra no vault como `draft: true` e em inglês, exigindo revisão manual extensa antes de uso. Um script local de tradução com Argos Translate pode acelerar a preparação editorial mantendo termos específicos de D&D consistentes em português.

## What Changes

- Criar um novo script Python para localizar arquivos Markdown com `draft: true`.
- Traduzir conteúdo textual de inglês para português usando a biblioteca Argos Translate.
- Preservar YAML front matter estrutural e campos que não devem ser traduzidos automaticamente.
- Tokenizar termos específicos de D&D antes da tradução automática para evitar traduções inconsistentes.
- Aplicar glossário de termos de D&D após a tradução substituindo tokens por traduções controladas.
- Permitir execução segura com modo dry-run, escopo por `compendium` ou `campaign`, limitação por caminho e confirmação antes de sobrescrever arquivos.
- Marcar arquivos traduzidos com metadados editoriais para revisão humana.
- Não alterar layouts Hugo nem o modelo de navegação do site.

## Capabilities

### New Capabilities
- `draft-translation`: tradução local de páginas Markdown em draft usando Argos Translate, tokenização e glossário de termos de RPG/D&D.

### Modified Capabilities
- `import-tools`: documenta que o fluxo de importação passa a ter uma etapa posterior opcional de tradução de drafts importados.

## Impact

- Novo script Python, previsto como `translate_drafts.py`.
- Possível novo arquivo de glossário versionado, por exemplo `translation_glossary.json` ou `translation_glossary.yaml`.
- Dependência Python opcional: `argostranslate`.
- Conteúdo Markdown em `content/compendium/**/*.md` quando o escopo for `compendium`.
- Conteúdo Markdown em `content/campaigns/<campaign-slug>/**/*.md` quando o escopo for `campaign`.
- Documentação operacional em `AGENTS.md` ou README se a implementação decidir registrar uso e cuidados.
