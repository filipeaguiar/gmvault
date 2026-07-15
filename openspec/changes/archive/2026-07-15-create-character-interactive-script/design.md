## Context

O projeto conta com o script `import_dndbeyond.py` que baixa dados de uma API e usa lógicas internas para calcular HP, CA, proficiências, e gerar um Markdown completo com itens do compêndio extraídos do 5e.tools.
A nova necessidade é permitir a criação completa via linha de comando sem depender de um char ID externo.

## Goals / Non-Goals

**Goals:**
- Criar um script `create_character.py` que guie o usuário pelas etapas de criação (nome, classe, raça, atributos, equipamento, magias).
- Reutilizar as funções de busca do 5e.tools (`fetch_from_5etools`) para popular o compêndio localmente com os dados inseridos.
- Formatar o YAML utilizando `PyYAML` adequadamente.

**Non-Goals:**
- Implementar interface visual (GUI) ou web. 
- Validação estrita das regras de D&D (ex: impedir usuário de ter +30 de Força), a responsabilidade da integridade final cai sobre o próprio GM/jogador.

## Decisions

- **CLI Interativo:** Utilizar `input()` simples ou bibliotecas como `Rich` para coletar as respostas (dependendo do que o projeto já possuir instalado; utilizaremos built-ins ou bibliotecas padrão quando possível).
- **Importação de funções:** Extrairemos funções genéricas (`fetch_from_5etools`, `dump_yaml_indented`, `slugify`) para um módulo `utils.py` ou os reaproveitaremos via importação do próprio `import_dndbeyond.py` (ou `import_campaign.py`) se a modularidade assim permitir sem causar referências circulares.

## Risks / Trade-offs

- **Risco:** O usuário pode digitar nomes de raças ou itens com erros de digitação (typos), o que causará falha na busca ao 5e.tools.
- **Mitigação:** O script pode exibir um aviso quando o item não for encontrado e simplesmente gerar o link que falhará no build, mas deixará para o GM criar manualmente a página do compêndio.
