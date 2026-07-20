## Context

Características de classe e subclasse são páginas canônicas do compêndio, enquanto as páginas de classe exibem a progressão como links. A consulta de opções pelo jogador exige navegar repetidamente entre páginas e perde o contexto do nível em que cada característica é recebida.

## Goals / Non-Goals

**Goals:**
- Exibir, por nível, o título e a descrição renderizada de cada característica resolvível.
- Reutilizar o conteúdo canônico com `site.GetPage`, sem duplicar texto nos arquivos de classe ou subclasse.
- Manter fallback de link ou caminho bruto para referências sem página.
- Respeitar visibilidade para não incluir páginas GM em páginas player-facing.

**Non-Goals:**
- Não alterar Markdown canônico, relações, URLs ou importadores.
- Não substituir páginas individuais de característica.
- Não criar controles interativos novos para escolhas de classe.

## Decisions

- **Partial compartilhado:** criar um partial que recebe uma URL de característica, resolve a página, mostra título localizado e conteúdo, e centraliza a regra de fallback e visibilidade.
- **Progressão como estrutura:** layouts de classe e subclasse usam os links já presentes no Markdown para montar cards ou blocos de característica sob cada nível, evitando novo front matter.
- **Conteúdo sem cabeçalho duplicado:** o partial renderiza `.Content`, não o layout completo da página relacionada; a página de origem mantém o nível como cabeçalho principal.
- **Interface expansível:** cada característica usa `details` para conservar escaneabilidade; o primeiro item de cada nível pode permanecer aberto por CSS/HTML quando aplicável.

## Risks / Trade-offs

- **Páginas longas** → usar blocos expansíveis e espaçamento compacto.
- **Referência inválida** → exibir o texto do link ou caminho, sem falhar o build.
- **Visibilidade mista** → filtrar conteúdo GM de páginas player/public e não criar links para ele.
