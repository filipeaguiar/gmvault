## 1. Core Logic (dnd_utils.py)

- [x] 1.1 Implementar a função utilitária `extract_class_resource_info(class_name, level, attributes)` em `dnd_utils.py` para carregar o JSON de cache, ler o `classTableGroups` e extrair o número correto de usos baseados no nível.
- [x] 1.2 Implementar a lógica de normalização de termos ("Ki" / "Ki Points" / "Focus Points" -> "Pontos de Foco") e mapeamento estático do tipo de recarga (reset).

## 2. Character Creation (create_character.py)

- [x] 2.1 Atualizar `create_character.py` para invocar a nova função de extração ao gerar a lista de ações padrão e de classe do personagem (`char_info.actions`).
- [x] 2.2 Validar a injeção correta de `max_uses` e `reset` em personagens recém-criados.

## 3. Character Level Up and Sync (edit_character.py)

- [x] 3.1 Atualizar a função `level_up_character` em `edit_character.py` para aplicar as novas regras e atualizar o campo `max_uses` de ações de recurso existentes.
- [x] 3.2 Atualizar a função `synchronize_character_compendium` em `edit_character.py` para adicionar retroativamente a ação do recurso de classe caso ela esteja ausente do Markdown.

## 4. Verification and Local Build

- [x] 4.1 Testar localmente os fluxos de criação e de subida de nível de um personagem exemplo (como o Monge Durin ou Bárbaro Durin) para validar o front matter Markdown resultante.
- [x] 4.2 Rodar a verificação local com build do Hugo (`hugo --gc --minify`) para garantir a integridade da renderização e conformidade com os critérios de aceite do projeto.
