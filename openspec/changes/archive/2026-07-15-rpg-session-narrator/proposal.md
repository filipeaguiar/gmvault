## Why

Transformar transcrições brutas de áudio de sessões de RPG em narrativas escritas em prosa literária exige um esforço manual considerável do Mestre (GM). A automação desse fluxo economiza tempo na preparação das sessões e mantém um diário de campanha consistente, tratando problemas inerentes a transcrições de plataformas como o Google Meet, como ruídos técnicos, erros de reconhecimento fonético de nomes próprios e falas de múltiplos participantes sob um único microfone (do Mestre).

## What Changes

- Criação de uma nova skill local `.agent/skills/rpg-session-narrator/SKILL.md` para guiar o agente no processamento e estruturação de narrativas literárias.
- Introdução de um arquivo de configuração/memória persistente (`memory.yaml`) para registrar metadados da campanha, correspondências entre participantes e personagens, variantes fonéticas de NPCs/termos e preferências de estilo de escrita.
- Desenvolvimento de um script auxiliar em Python (`process_transcript.py`) para realizar o pré-processamento, segmentação em blocos/cenas, correção fonética de nomes de fantasia e resolução heurística de vozes sob o mesmo microfone.
- Criação de um template padrão de saída Markdown para integrar a narrativa de sessão na pasta de aventuras da campanha.
- Criação de um cenário de teste para validação local da normalização e resolução de ambiguidades.

## Capabilities

### New Capabilities

- `rpg-session-narrator`: Capability para gerenciar a memória persistente da campanha, pré-processar e corrigir transcrições brutas de RPG, resolver autoria de voz em microfones compartilhados e estruturar crônicas literárias em Markdown compatíveis com o gmvault.

### Modified Capabilities

Nenhuma.

## Impact

- Criação do diretório `.agent/skills/rpg-session-narrator/` e de seus respectivos arquivos de skill, scripts e templates.
- Não afeta a infraestrutura do Hugo ou os scripts de importação do 5e.tools e do D&D Beyond.
