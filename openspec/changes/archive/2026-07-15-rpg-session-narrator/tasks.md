## 1. Directory Setup & Configuration

- [x] 1.1 Criar o diretório da skill `.agent/skills/rpg-session-narrator/` e suas subpastas `scripts/`, `templates/` e `tests/`.
- [x] 1.2 Criar o arquivo de memória persistente `memory.yaml` contendo o esquema especificado de metadados da campanha, jogadores, NPCs e termos.
- [x] 1.3 Criar o arquivo principal da skill `SKILL.md` contendo as diretrizes de ativação, comportamento do agente, fluxos interativos e regras de fidelidade de prosa.
- [x] 1.4 Criar o template Markdown de saída em `templates/output_template.md`.

## 2. Helper Script Development

- [x] 2.1 Criar a estrutura do script auxiliar Python `scripts/process_transcript.py` para carregar a memória YAML e ler a transcrição bruta.
- [x] 2.2 Implementar a limpeza de ruídos técnicos, timestamps e segmentação da transcrição em cenas/blocos de tamanho controlado.
- [x] 2.3 Implementar a normalização léxica-fonética para substituir aliases incorretos e variantes pelos termos canônicos mapeados na memória.
- [x] 2.4 Implementar a heurística de autoria de fala para microfone compartilhado (GM e jogadores presenciais).
- [x] 2.5 Implementar a geração da representação intermediária estruturada em formato JSON com marcação de incertezas.

## 3. Testing & Documentation

- [x] 3.1 Criar um cenário de validação e arquivo de teste em `tests/test_narrator.py` com uma transcrição fictícia cobrindo microfone compartilhado, nomes com erros de reconhecimento, dados e regras.
- [x] 3.2 Executar os testes locais e garantir que a lógica de resolução e normalização funcione corretamente.
- [x] 3.3 Criar o arquivo de instruções de uso `README.md` da skill e documentar como rodar e configurá-la.
