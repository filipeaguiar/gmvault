# Papéis editoriais de conteúdo

O front matter pode declarar `params.content_role` para indicar que uma página tem função editorial especial dentro da árvore de conteúdo.

Valor implementado:

```yaml
type: scene
params:
  content_role: introduction
```

`introduction` identifica material introdutório, como introdução geral, antecedentes, ganchos e orientação ao mestre. Templates agregam essas páginas na página principal do contexto correspondente e as removem das grades de navegação para evitar duplicação.

Ausência de `content_role` significa conteúdo normal. Valores desconhecidos devem ser tratados como conteúdo normal.

A classificação por título é permitida apenas no importador como heurística conservadora. Depois da importação, os templates devem usar somente o valor explícito do front matter.
