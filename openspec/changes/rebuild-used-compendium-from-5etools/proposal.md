## Why

O compêndio contém centenas de páginas antigas, stubs e documentos sem uso, gerados por versões diferentes dos importadores. A campanha e os personagens atuais possuem 171 referências diretas e dependem de mais 20 regras alcançadas por referências internas do próprio compêndio; esse fechamento de 191 entidades deve ser reconstruído no formato vigente, com proveniência verificável no 5e.tools e tradução consistente.

## What Changes

- Criar um fluxo de inventário que derive as referências-raiz presentes nas campanhas e personagens e calcule recursivamente as dependências entre páginas do compêndio.
- Reconstruir as 191 páginas atualmente necessárias — 171 referências diretas e 20 dependências transitivas — usando exclusivamente dados do 5e.tools, preservando seus slugs e URLs internas.
- Registrar em cada página a entidade e a publicação-fonte selecionadas no 5e.tools.
- Priorizar entidades `XPHB` quando houver versão nessa fonte, permitindo fallback para `PHB` e, depois, para outra fonte explícita disponível no 5e.tools; Goblin continuará usando uma fonte não-PHB disponível no catálogo.
- Respeitar as fontes declaradas pelos dados de `JttRC` para monstros e itens da campanha, sem promover automaticamente versões `MM` para `XMM`.
- Criar um manifesto revisável antes da substituição, com referência interna, tipo, nome, fonte escolhida e resultado da resolução.
- **BREAKING**: remover do repositório as 263 páginas de entidade atuais que não pertencem ao fechamento transitivo das referências usadas por campanhas e personagens; preservar `_index.md`.
- Atualizar os geradores/importadores para produzir o novo formato e impedir que dados descritivos do compêndio sejam obtidos de outra fonte.
- Adicionar um perfil de tradução para `deepseek-v4-pro` e substituir o uso preferencial do alias obsoleto `deepseek-chat`.
- Auditar e atualizar o glossário com os termos encontrados nas entidades selecionadas, mantendo revisão editorial e validações de saídas proibidas.
- Executar download, geração e tradução em staging, com validação de YAML, referências, schemas, build Hugo e diff antes da promoção ao conteúdo definitivo.

## Capabilities

### New Capabilities
- `compendium-rebuild`: descoberta de referências usadas, resolução exclusiva via 5e.tools, manifesto, staging, remoção de páginas sem uso e promoção validada.

### Modified Capabilities
- `compendium`: páginas reutilizáveis passam a exigir proveniência 5e.tools e formato estruturado vigente.
- `import-tools`: importadores passam a resolver conteúdo descritivo do compêndio exclusivamente no 5e.tools, com prioridade de fontes determinística.
- `create-character-interactive`: a criação de personagens passa a preservar a fonte 5e.tools escolhida para cada referência e a priorizar XPHB com fallback controlado.
- `draft-translation`: o glossário passa a ser auditável contra o corpus selecionado e a tradução deve preservar metadados de proveniência.
- `translation-profiles-and-strategies`: passa a existir um perfil DeepSeek V4 Pro selecionável para tradução de alta qualidade.

## Impact

- Afeta `content/compendium/`, `dnd_utils.py`, `import_campaign.py`, `import_dndbeyond.py`, `create_character.py`, `translate_drafts.py`, `translation_config.json`, `translation_glossary.json`, testes e documentação operacional.
- Remove conteúdo não referenciado e substitui páginas necessárias, exigindo backup/staging e revisão do manifesto antes da promoção.
- Mantém as URLs das 191 entidades diretas ou transitivamente usadas para não quebrar campanhas, fichas e dependências internas do compêndio.
- Passa a depender da disponibilidade do mirror comunitário do 5e.tools durante a reconstrução e da API DeepSeek durante a tradução.
- O material baixado pode derivar de publicações comerciais e continuará em draft até revisão editorial.