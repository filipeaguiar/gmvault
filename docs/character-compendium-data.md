# Dados de personagem e compêndio

## Contrato referencial

O front matter de uma ficha separa dados próprios do personagem de conteúdo compartilhado:

- `char_info`: atributos, modificadores, CA, HP, deslocamentos, sentidos, idiomas, perícias, moedas e estado operacional.
- `char_info.actions[].ref`: URL interna da regra da ação ou característica. A entrada mantém `name`, `source`, `max_uses` e `reset`.
- `char_info.equipment[].ref`: URL interna do item ou item mágico. A entrada mantém quantidade, equipado e fórmulas calculadas.
- `char_info.spells[].ref`: URL interna da magia. A entrada mantém nome, nível, origem, preparo, preparo permanente, conhecimento, capacidade de preparo e uso.
- `char_info.spellcasting`: perfil operacional da conjuração da ficha, incluindo modo, habilidade, listas de refs e progressão de slots.
- `char_info.classes_progression`: identidade e nível da classe; detalhes compartilhados são resolvidos pela referência da classe ou das regras.
- `compendium_refs`: conjunto de URLs internas das entidades relacionadas que não possuem uma entrada individual com `ref`.

Precedência de resolução:

1. `ref` explícito da entrada;
2. referência equivalente em `compendium_refs`;
3. fallback de `description` somente para conteúdo legado sem página resolvível.

URLs devem ser caminhos internos absolutos, terminando em `/`, por exemplo `/compendium/rules/sneak-attack/`.

## Auditoria de Pinky

| Campo ou grupo | Classificação | Tratamento |
|---|---|---|
| `class`, `race`, `size`, `alignment` | identidade | manter na ficha e referenciar compêndio |
| `ac`, `hp`, `speed`, `senses`, `languages` | estatística | manter na ficha |
| `stats`, `mods`, `saves`, `skills`, `currencies` | cálculo/estado | manter na ficha |
| `actions[].max_uses`, `reset`, `source` | estado operacional | manter na ficha |
| `actions[].description` | regra compartilhada | substituir por `ref` quando houver nota validada |
| `equipment[].quantity`, `equipped`, fórmulas | estado operacional | manter na ficha |
| `equipment[].name`, `description` | entidade compartilhada | resolver pela entrada `ref` |
| `spells[].level`, `prepared`, `usage` | estado operacional | manter na ficha e resolver conteúdo por `ref` |
| `feat` | lista de entidades | manter como compatibilidade, preferir refs individuais |
| corpo Markdown | biografia | preservar integralmente |

Referências existentes que precisam de revisão durante a migração:

- `Sneak Attack`, `Cunning Action`, `Steady Aim` e as demais características de classe já possuem algumas notas em `content/compendium/rules/`.
- `Healing Hands`, `Firearm Specialist`, `Vex` e `Slow` precisam de correspondência validada ou de notas específicas antes da remoção de suas descrições.
- `Musket, +3` e `Pistol, +2` não possuem atualmente páginas locais correspondentes; não remover suas fórmulas nem descrições legadas até criar ou localizar notas válidas.
- `Padded` possui referências duplicadas entre `items` e `magic-items`; a migração deve escolher uma referência canônica sem remover o item do inventário.

## Processadores

`import_dndbeyond.py` deve gerar o formato acima para fichas novas e refletir os dados da fonte externa sem exceções de personagem. `scripts/sync_character.py` pode completar refs, mas só remove uma descrição quando a página existe e possui conteúdo. `translate_drafts.py` deve proteger URLs e metadados referenciais e traduzir o conteúdo da nota do compêndio, não expandir a ficha.

Correções editoriais específicas, como raça e nível de Pinky, são aplicadas depois da importação, diretamente na ficha ou por uma ferramenta de correção explícita. Elas não devem ser incorporadas ao algoritmo geral de importação.
