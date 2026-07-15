## Context

O projeto `gmvault` é uma wiki estática baseada em Hugo para organizar campanhas de RPG. A criação de crônicas de sessões a partir de transcrições de áudio (geralmente do Google Meet) atualmente exige processamento manual pesado. Esta mudança introduz uma skill automatizada local (`rpg-session-narrator`) para normalizar, segmentar e narrar em prosa literária as sessões, preservando a memória de termos e personagens.

## Goals / Non-Goals

**Goals:**
- Criar a definição de skill do Antigravity em `.agent/skills/rpg-session-narrator/SKILL.md`.
- Implementar um script Python auxiliar em `.agent/skills/rpg-session-narrator/scripts/process_transcript.py` para pré-processar as transcrições grandes, estruturar as cenas em JSON e limpar ruídos.
- Implementar suporte para normalização de nomes próprios/fantasy baseados no léxico de `memory.yaml`.
- Desenvolver heurísticas de resolução de falas do GM que pertençam a jogadores presenciais compartilhando o mesmo microfone.
- Gerar arquivos Markdown compatíveis com o gmvault na pasta correta.
- Prover testes automatizados em `.agent/skills/rpg-session-narrator/tests/` para verificar as correções.

**Non-Goals:**
- Integração direta com a API do Google Meet ou download automático de áudios.
- Utilização de APIs pagas de IA externas de forma obrigatória (o script rodará localmente, e as etapas de geração de prosa se apoiarão na própria IA do agente Antigravity executando a skill).
- Modificar o sistema de build do Hugo ou o parser do site.

## Decisions

- **Uso de YAML para memória persistente (`memory.yaml`):** Facilidade de leitura e edição manual pelo GM. Alternativas consideradas: SQLite (complexo e não legível diretamente por humanos em arquivos de texto plano) ou JSON (difícil de comentar e formatar manualmente).
- **Abordagem Híbrida (Script Python + IA do Agente):** O script Python realiza a limpeza determinística de ruídos, segmentação cronológica exata, substituição léxica de aliases e estruturação em JSON. A IA do agente lê o JSON intermediário e redige a prosa literária final. Isso reduz o tamanho do contexto da IA e garante fidelidade factual e alta qualidade na escrita.
- **Heurísticas de Microfone Compartilhado:** O script analisará as falas atribuídas ao mestre, cruzando pronomes, nomes de personagens cadastrados, estilo de fala do mestre (perguntas e descrições) e as ações declaradas em primeira pessoa que batam com as ações dos personagens presenciais.

## Risks / Trade-offs

- **Limitação de Contexto:** Transcrições muito grandes podem causar estouro de contexto. *Mitigação*: O script Python realiza uma segmentação física em arquivos JSON menores (cenas de até ~15-20 KB), permitindo que a IA processe e gere o texto por blocos se necessário.
- **Falsos Positivos na Resolução de Voz:** A atribuição de voz baseada em heurísticas pode falhar. *Mitigação*: Manter um log de incertezas no JSON intermediário e exibir as ambiguidades relevantes em uma tabela compacta ao usuário para confirmação rápida antes da redação final.
