## Context

O layout `forge_statblock.html` gera uma exportação JSON de statblocks para a plataforma Battle System Forge. O compêndio global reconstrói os monstros estruturando `saves` e `skills` como mapas YAML no front matter das páginas. O layout, contudo, assume que esses campos são strings brutas e tenta extraí-los via regex e split por vírgulas, o que corrompe e anula os dados exportados. Além disso, as velocidades estruturadas com o prefixo "walk" e as habilidades de monstros formatadas em cabeçalhos nível 3 (`###`) são descartadas. Este design resolve essas falhas de forma direta no layout Hugo.

## Goals / Non-Goals

**Goals:**
- Implementar suporte condicional a mapas e strings para `saves` e `skills` no layout `forge_statblock.html`.
- Corrigir a regex de velocidade de caminhada para tolerar o prefixo `"walk"`.
- Implementar algoritmo de parser de ações e características que suporte cabeçalhos `##` e `###` no corpo do markdown, mantendo compatibilidade com negritos legados.

**Non-Goals:**
- Modificar a estrutura de dados gerada pelo reconstrutor de compêndio ou pelo importador.
- Alterar o layout da wiki voltado a visualização humana no navegador.

## Decisions

### Decisão 1: Checagem dinâmica de tipos com `reflect.IsMap`
Hugo fornece a função `reflect.IsMap` para detectar tipos complexos de dicionário. Usaremos essa função no template para bifurcar a lógica de extração: se for mapa, iteramos pelas chaves; se for string, aplicamos as expressões regulares clássicas.
* *Alternativa considerada*: Alterar os scripts Python para uniformizar tudo como string. *Razão de rejeição*: A modelagem estruturada (YAML map) é mais limpa e útil para o Hugo gerar outros tipos de listagem estruturada.

### Decisão 2: Regex de Velocidade Aprimorada
O layout tentará casar a substring `"walk [número]"` na velocidade. Se encontrar, extrai o número. Caso contrário, faz o fallback para casar dígitos diretamente no início da string (padrão de string contendo apenas o número da caminhada).

### Decisão 3: Parser de Markdown por Níveis
O script lerá o corpo bruto e o dividirá por `\n## `. Se a seção maior for identificada (ex: `Ações`), ela será dividida por `\n### ` para processar as subseções individuais. A primeira linha de cada subseção será o nome e o resto será a descrição. Se não houver cabeçalhos `### ` na seção, ela aplicará o parser legado baseado em negritos na mesma linha.

## Risks / Trade-offs

- **[Risk]** Ações com múltiplos parágrafos podem ter seu espaçamento modificado na exportação.
  - *Mitigação*: Delimitar as linhas com quebras de linha normais no helper `forge_roll_parser.html`.
- **[Risk]** Quebras no build do Hugo por uso incorreto de funções de reflexão.
  - *Mitigação*: Usar `reflect.IsMap` de forma segura protegida por defaults.
