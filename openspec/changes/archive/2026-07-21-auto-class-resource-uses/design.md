## Context

O RPG Campaign Vault renderiza fichas de personagens de forma estática com Hugo. Habilidades especiais de classe com usos limitados (como Fúria, Ki/Foco, Inspiração Bárdica) podem ser acompanhadas usando caixas de seleção na aba de **Ações**, desde que tenham o campo `max_uses > 0` e `reset` definidos em `char_info.actions` no front matter. 
Este design estabelece como extrair de forma robusta e automatizada essas informações dos arquivos de cache do 5e.tools (JSON) e aplicá-las às fichas tanto na criação quanto na subida de nível ou sincronização.

## Goals / Non-Goals

**Goals:**
- Identificar colunas estruturadas de recursos de classe no JSON do 5e.tools (ex: "Ki Points", "Focus Points", "Rages", "Bardic Inspiration").
- Injetar ou atualizar os campos `max_uses` e `reset` nas ações correspondentes do personagem na criação (`create_character.py`) e na subida de nível/sincronização (`edit_character.py`).
- Garantir a criação da ação de recurso caso ela ainda não esteja listada na ficha do personagem (sincronização retroativa).
- Normalizar a nomenclatura antiga "Ki" para o termo moderno **"Foco"** / **"Pontos de Foco"** para a classe Monge.

**Non-Goals:**
- Persistir o estado atual de caixas de seleção marcadas no servidor (isso é gerido puramente pelo navegador/estado do cliente).
- Alterar o rastreador de espaços de magia (spell slots) que já possui fluxo e visualização próprios na aba de Grimório.

## Decisions

### Decisão 1: Modularização da lógica em `dnd_utils.py`
Para evitar duplicação entre `create_character.py` and `edit_character.py`, a lógica de resolução de recursos de classe será adicionada como uma nova função utilitária em `dnd_utils.py` chamada `resolve_class_resource_uses(class_name, level, con_or_cha_mod=0)`.
* *Alternativa considerada*: Codificar isso separadamente em cada arquivo. *Razão de rejeição*: Dificulta a manutenção e a consistência das regras.

### Decisão 2: Normalização de nomenclaturas
* **Ki / Ki Points / Focus Points** (Monge) -> Nome da Ação: `"Pontos de Foco"`, Referência: `"/compendium/rules/ki/"`, Reset: `"Descanso Curto ou Longo"`.
* **Rages** (Bárbaro) -> Nome da Ação: `"Fúria (Rage)"` ou `"Fúria"`, Referência: `"/compendium/rules/rage/"`, Reset: `"Descanso Longo"`.
* **Bardic Inspiration** (Bardo) -> Nome da Ação: `"Inspiração Bárdica"`, Referência: `"/compendium/rules/bardic-inspiration/"`, Reset: `"Descanso Longo"` (Nível 1-4) ou `"Descanso Curto ou Longo"` (Nível 5+ via *Font of Inspiration*), Usos: baseados em Carisma (regra legada) ou bônus de proficiência.

### Decisão 3: Tolerância a Falhas
Caso o arquivo de cache de classe correspondente não seja encontrado ou falhe no parse, o sistema SHALL emitir um aviso no console e manter a execução sem quebrar o processo, aplicando `max_uses: 0` como fallback.

## Risks / Trade-offs

- **[Risk]** Nomes de colunas no 5e.tools mudando no futuro.
  - *Mitigação*: Usar correspondências de substring case-insensitive e tolerância a falhas.
- **[Risk]** Sobrescrever edições manuais feitas pelo usuário.
  - *Mitigação*: Somente atualizar valores de `max_uses` e `reset` se o valor do nível mudou ou se o campo for nulo/padrão, respeitando a intenção de quem sincroniza.
