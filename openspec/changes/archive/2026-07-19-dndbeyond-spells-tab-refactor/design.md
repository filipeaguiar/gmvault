## Context

A change anterior descrevia uma UI ampla para “spellcasting universal”, mas o escopo real é mais específico: a ficha precisa **persistir a lista de magias do personagem** e usar **localStorage apenas para o estado operacional da aba** (preparadas, sempre prontas, aprendidas não preparadas, filtros e seleção visual). O Markdown não precisa gravar o estado tático de uso em sessão.

Os scripts de criação/edição/importação precisam ser capazes de adicionar magias automaticamente quando a classe ou uma fonte adicional as conceder, e também permitir entrada manual quando a classe exigir escolha do usuário. A organização visual deve ser leve, com separação entre magias prontas para uso e magias aprendidas, e não precisa alterar o modelo permanente da ficha a cada preparo/despreparo.

## Goals / Non-Goals

**Goals:**

- Persistir a lista de magias do personagem no frontmatter/dados da ficha.
- Carregar e salvar o estado operacional da aba em `localStorage`.
- Permitir adição automática e manual de magias nos scripts.
- Exibir a lista de magias de forma escaneável, com filtros por nível e separação visual por estado de uso.
- Consultar 5e.tools para determinar como cada classe lida com magias.
- Manter compatibilidade com personagens legados que ainda usam `char_info.spells`, `char_info.class_spells` e `spell_slots`.

**Non-Goals:**

- Persistir em Markdown o estado operacional da aba para uso em sessão.
- Reescrever a arquitetura inteira da ficha de personagem.
- Inventar regras de conjuração sem consultar 5e.tools.
- Remover suporte aos campos legados enquanto a migração não estiver concluída.

## Decisions

### 1. Separar lista persistida de magias e estado operacional

A ficha terá um conjunto persistido de magias do personagem, mas o estado de “preparada”, “sempre pronta” ou “não preparada” será guardado no navegador. Isso mantém a ficha estável e evita sobrescrever Markdown por ações de mesa.

### 2. Usar `localStorage` como fonte de estado da aba

A UI da aba de spells lerá/escreverá estado local no navegador para preservar filtros, separação visual e marcações de preparo durante a navegação. O estado é de sessão, não de verdade permanente.

### 3. Centralizar a regra de conjuração no 5e.tools

A classificação de cada classe será consultada no 5e.tools para decidir se a lista é preparada, conhecida, espontânea, pact, híbrida ou feature-granted. Isso evita codificar exceções duplicadas em scripts e layouts.

### 4. Manter compatibilidade com o contrato legado

`char_info.spells`, `char_info.class_spells` e `spell_slots` continuarão sendo lidos como fallback. O novo contrato deve poder coexistir com eles enquanto os scripts migram gradualmente.

### 5. UI simples e leve

A aba deve continuar escaneável e útil em sessão, mas sem depender de uma arquitetura pesada. A prioridade é: lista, filtros, separação visual e ações mínimas necessárias.

## Risks / Trade-offs

- **[Personagens legados sem lista persistida nova]** → manter fallback para os campos antigos e degradar a UI de forma compatível.
- **[Múltiplas fontes de magia no mesmo personagem]** → separar origem da magia e estado operacional na UI para não misturar preparo com aquisição.
- **[`localStorage` ser apagado]** → o personagem continua recuperável; apenas o estado operacional da aba é perdido.
- **[Regras de classe divergentes entre fontes]** → consultar 5e.tools e registrar o perfil de conjuração por classe/feature.

## Migration Plan

1. Definir o contrato de dados persistidos da lista de magias.
2. Implementar o estado operacional da aba em `localStorage`.
3. Ajustar scripts para adicionar magias automaticamente ou manualmente, conforme a classe.
4. Atualizar a UI para separar prontas para uso e aprendidas não preparadas.
5. Validar compatibilidade com personagens legados.

## Final Decisions

- A definição de cada magia permanece no compêndio; a ficha persiste apenas referências e metadados operacionais mínimos (`ref`, origem, nível e estado inicial).
- Scripts de criação, edição e importação materializam referências para o compêndio e usam o perfil de conjuração para classificar a entrada.
- `localStorage` é a fonte de verdade para preparo/despreparo, filtros, espaços marcados e a organização operacional durante a sessão; nenhuma interação da aba regrava Markdown.
- A interface separa magias prontas das que podem ser gerenciadas e também mostra a origem nos badges.
- O suporte a `char_info.spells`, `class_spells` e `spell_slots` permanece como leitura de compatibilidade; a lista persistida de `spells` tem precedência quando disponível.

## Delivery Scope

Não é necessário dividir a entrega em fases adicionais: o contrato de dados, os scripts, a UI e a persistência local foram implementados e validados como uma mudança coesa.
