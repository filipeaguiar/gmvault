---
name: rpg-session-narrator
description: Transforma transcrições de sessões de RPG em prosa literária em Markdown, normalizando termos de fantasia, resolvendo falas presenciais com microfone compartilhado e mantendo fidelidade aos acontecimentos.
---

# RPG Session Narrator — Skill Instrucional do Agente

Esta skill permite ao agente Antigravity processar transcrições brutas de sessões de RPG e transformá-las em narrativas literárias estruturadas. Ela utiliza uma abordagem híbrida: um script Python auxiliar faz a limpeza, a normalização de termos baseada em um léxico de memória e a resolução heurística do microfone compartilhado, enquanto a IA do agente realiza a redação artística final baseada em dados intermediários.

## 1. Ativação e Modos de Uso

A skill é ativada quando o usuário solicita explicitamente a narração de uma sessão de RPG ou quando ele chama comandos como:

- `Configurar campanha` ou `rpg-session-narrator setup`: Roda a configuração interativa de metadados da campanha, jogadores e NPCs.
- `Adicionar jogador` / `Adicionar NPC`: Cadastra novos personagens/entidades na memória persistente.
- `Revisar memória` / `Corrigir memória`: Visualiza e atualiza o estado de `memory.yaml`.
- `Processar sessão` ou `Processar transcrição`: Inicia o fluxo de narração de uma transcrição.
- `Reprocessar sessão`: Gera novamente o Markdown de uma sessão com base em um JSON intermediário existente ou após ajustes na memória.

---

## 2. Fluxo de Trabalho Passo a Passo

### Fase 1: Carregamento de Configurações e Memória
Ao iniciar qualquer operação, o agente deve ler o arquivo de memória persistente `.agent/skills/rpg-session-narrator/memory.yaml`.
Se o arquivo não existir ou se faltarem informações estruturais essenciais (como nome do mestre, nome da campanha, sistema ou lista mínima de jogadores/personagens), execute a **Fase 2 (Configuração Inicial)**.

### Fase 2: Configuração Inicial Interativa
Se as configurações obrigatórias estiverem ausentes, o agente deve coletar interativamente as informações do usuário. Em vez de perguntar individualmente em turnos separados do chat, o agente deve apresentar as perguntas estruturadas de forma concisa e pedir para o usuário preencher (dando a ele a opção de preencher em formato de tabela ou lista).
As perguntas obrigatórias cobrem:
1. Nome do Mestre/Usuário e seu nome na transcrição.
2. Nome da campanha e Sistema utilizado.
3. Diretório de arquivos de aventuras e de narrativas de sessão.
4. Mapeamento de Jogadores (Nome, Aliases na transcrição, Nome do Personagem, Aliases do personagem, se costuma jogar remoto).
5. Mapeamento de NPCs (Nome canônico, Aliases, erros comuns de escrita/fonética).
6. Termos de fantasia recorrentes (Locais, deuses, facções com variantes comuns).
7. Estilo da narrativa, Pessoa (primeira ou terceira), Tempo verbal (passado ou presente) e preferência de preservação de diálogos diretos importantes.

Toda informação cadastrada deve ser salva de volta no `memory.yaml` chamando o script Python:
`python3 .agent/skills/rpg-session-narrator/scripts/process_transcript.py setup` (ou salvando diretamente pelo agente).

### Fase 3: Perguntas Específicas da Sessão
Antes de processar uma transcrição, o agente deve solicitar ao usuário:
1. O caminho do arquivo de transcrição (ex: `transcriptions/sessao-12.txt`).
2. A data da sessão (ex: `2026-07-14`).
3. O número ou título da sessão (ex: `12` ou `O Mercado Noturno`).
4. Jogadores presentes nesta sessão.
5. **Perguntas sobre Participantes Presenciais (Obrigatório!):** Quais jogadores estavam fisicamente ao lado do mestre e utilizaram o mesmo microfone?
6. NPCs ou termos novos introduzidos nesta sessão específica.
7. Algum trecho/cena a ser explicitamente descartado (como papo inicial de intervalo, etc.).

Crie um arquivo JSON temporário contendo esses parâmetros em `/tmp/session_config.json` para passar ao script Python:
```json
{
  "date": "YYYY-MM-DD",
  "session_number": 12,
  "session_title": "Título da Sessão",
  "transcript_path": "caminho/para/transcricao.txt",
  "players_present": ["NomeJogador1", "NomeJogador2"],
  "shared_microphone": {
    "transcript_label": "Nome do Mestre na Transcrição",
    "possible_speakers": [
      {"type": "game_master", "name": "Nome Mestre"},
      {"type": "player", "name": "Jogador Presencial 1", "character": "Nome Personagem"}
    ]
  }
}
```

### Fase 4: Processamento pelo Script Python
O agente deve propor a execução do script Python para fazer a análise preliminar da transcrição:
```bash
python3 .agent/skills/rpg-session-narrator/scripts/process_transcript.py process \
  --transcript "/caminho/completo/transcricao.txt" \
  --session-config "/tmp/session_config.json" \
  --output-json "/tmp/intermediate_session.json"
```
Este comando realizará:
- Limpeza de avisos de sistema e ruídos de conexão.
- Normalização léxica-fonética baseada na memória.
- Resolução heurística preliminar de autoria no microfone compartilhado.
- Divisão da transcrição em cenas cronológicas com representação intermediária JSON.

### Fase 5: Resolução de Incertezas / Confirmação do Usuário
O arquivo `/tmp/intermediate_session.json` conterá um array de `uncertainties`.
O agente deve ler esse JSON e apresentar as ambiguidades ao usuário em uma tabela formatada:
```markdown
| ID | Fala/Trecho | Interpretação Proposta | Confirmação |
|---|---|---|---|
| 1 | "Eu vou tentar arrombar a fechadura." | Brom (Jogador Presencial João) | [Mestre / João / Manter ambíguo] |
| 2 | "Yana, se afaste de si abre um corpo." | NPC Yana e localidade Siabsungkoh | [Siabsungkoh / Outro] |
```
O usuário poderá responder de forma compacta (ex: `1: João, 2: Siabsungkoh`).
Após o feedback do usuário, o agente atualiza as atribuições correspondentes nas falas das cenas do JSON intermediário. Se novas grafias incorretas foram confirmadas pelo usuário, registre-as como aliases no `memory.yaml`.

### Fase 6: Camada de Estruturação e Mapeamento de Cenas (Camada 1)
O agente deve realizar a primeira passagem sobre a transcrição bruta `.txt` para delimitar e mapear as cenas cronologicamente:
1. Identifique os pontos de transição (mudanças de localidade, início de combates, desafios ou avanços narrativos).
2. Para cada cena, crie uma ficha de metadados crua contendo:
   - **ID da Cena** (numeração sequencial).
   - **Localidade** no mundo de jogo.
   - **Participantes prováveis** (nomes reais dos jogadores e NPCs envolvidos).
   - **Resumo curto de eventos**.

### Fase 7: Camada de Verificação Factual e Validação de Autoria (Camada 2)
O agente realiza a segunda passagem, executando uma revisão estrita e de cobertura factológica:
- **Verificação de Cobertura:** Releia a transcrição bruta e compare-a com a lista de cenas para garantir que nenhum evento secundário, teste de dado importante ou ação relevante tenha sido esquecido. A cobertura da transcrição deve ser de 100%.
- **Validação de Autoria:** Mapeie de forma rígida cada ação e rolagem de dados à pessoa real que a realizou, garantindo a correspondência estrita com seu respectivo personagem fictício (conforme o mapeamento do `memory.yaml`). É expressamente proibido transferir ações ou falas entre personagens de jogadores.

### Fase 8: Camada de Extração de Diálogos e Voz dos Personagens (Camada 3)
O agente realiza a terceira passagem focada no enriquecimento dramático e humorístico:
- **Diálogos Notáveis:** Vasculhe a transcrição em busca de diálogos marcantes em discurso direto, interações engraçadas, piadas internas, falas icônicas dos personagens ou reações hilárias aos testes de dados (como hesitações e gagueiras causadas pelas mecânicas).
- **Registro de Voz:** Anote e transcreva essas falas literalmente, associando-as como marcadores obrigatórios nas fichas de cenas criadas na Fase 6 para que sejam obrigatoriamente integradas na redação final.

### Fase 9: Camada de Redação Incremental por Cena (Camada 4)
Com os metadados factuais validados (Fase 7) e os diálogos notáveis extraídos (Fase 8), o agente inicia a escrita do capítulo. A redação é executada **de forma isolada, cena por cena**:
1. Escreva o rascunho de prosa literária de cada cena individualmente, garantindo alta densidade e detalhamento factual, sem tentar resumir ou acelerar o texto.
2. Integre de forma orgânica e literal os diálogos notáveis em discurso direto (travessões ou aspas).
3. Salve a prosa de cada cena temporariamente no contexto ou em arquivos de rascunho (ex: `/tmp/cena_NN.md`).
4. Repita até que todas as cenas listadas tenham sua prosa rústica redigida por completo.

### Fase 10: Camada de Polimento, Continuidade e Ritmo Estilístico (Camada 5)
O agente unifica a prosa de todas as cenas e executa a camada final de polimento literário:
- **Continuidade e Fluidez:** Suavize as quebras de transição entre as cenas, garantindo que o texto flua como um romance de fantasia contínuo e contundente.
- **Remoção de Termos Técnicos:** Traduza qualquer termo mecânico residual em prosa literária imersiva.
- **Revisão de Ritmo:** Garanta que a segunda metade do capítulo tenha a mesma riqueza estilística e densidade da primeira metade.

### Fase 11: Gravação do Markdown Final (Capítulo do Journal)
O texto polido e consolidado deve ser gravado usando o template em `.agent/skills/rpg-session-narrator/templates/output_template.md`.
1. Salve o arquivo final no diretório `journal/` da campanha (`content/campaigns/<campaign-slug>/journal/`), nomeando-o de acordo com a sequência de capítulos (`NNN-slug-da-sessao.md`).
2. Defina no frontmatter apenas a chave `params.kind: "journal_entry"` com `draft: false`, `visibility: "players"` e `status: "ready"`.

### Fase 12: Relatório de Processamento
Apresente um relatório final da execução contendo:
- Nome do arquivo gerado e tamanho da prosa.
- Quantidade de cenas estruturadas.
- NPCs identificados e normalizados.
- Aliases adicionados à memória.
- Ambiguidades resolvidas e pendências salvas.

---

## 3. Regras de Fidelidade Factual (Obrigatórias)

O agente SHALL seguir estritamente as seguintes regras na redação:
1. **Não inventar acontecimentos:** A história deve bater exatamente com os fatos da sessão de RPG.
2. **Fidelidade aos dados:** Se um jogador falhou em um teste mecânico de dado, a narrativa deve descrever uma falha ou impedimento na ação correspondente.
3. **Não alterar a agência dos jogadores:** A autoria das ações de personagens pertence unicamente às declarações dos respectivos jogadores.
4. **Sem meta-conhecimento:** Não revele segredos que o mestre sabia nos bastidores, mas que não foram expostos verbalmente em jogo.
5. **Sem adivinhações de sentimentos/pensamentos:** Não atribua pensamentos íntimos ou sentimentos aos personagens sem base nas declarações verbais do jogador.
6. **Vínculo Rígido de Autoria:** É expressamente proibido trocar os atores das ações. Cada rolagem de dado, declaração de intenção ou fala em jogo deve ser atribuída exclusivamente ao personagem cujo jogador realizou a ação na transcrição bruta. O agente deve consultar obrigatoriamente a tabela de correspondência em `players` no `memory.yaml` para validar a correspondência entre a pessoa real que fala e o personagem fictício.
