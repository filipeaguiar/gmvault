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

### Fase 6: Identificação e Lista Consolidada de Cenas (Primeira Etapa)
O agente deve ler o arquivo de transcrição bruta `.txt` na íntegra e estruturar a lista cronológica completa de cenas da sessão:
1. Mapeie cada cena identificando os pontos de transição (mudanças de localidade, início de um combate, novos desafios ou transições narrativas).
2. Para cada cena identificada, monte uma lista detalhada contendo:
   - **ID da Cena**: Numeração sequencial.
   - **Localidade**: Onde a cena ocorre no mundo do RPG.
   - **Participantes**: Quais personagens de jogadores e NPCs estão presentes e ativos na cena.
   - **Acontecimentos**: Os principais eventos, falas importantes e testes de dados ocorridos.

### Fase 7: Revisão Cruzada e Cobertura Completa (Segunda Etapa)
Antes de iniciar qualquer redação literária, o agente deve reler a transcrição bruta `.txt` original e compará-la detalhadamente com a lista de cenas gerada na Fase 6:
- Verifique se alguma cena intermediária, evento, conversa ou rolagem de dados relevante foi ignorada ou resumida em excesso na primeira passagem.
- Caso identifique lacunas, atualize a lista de cenas inserindo novos trechos de eventos.
- A fase de redação só deve começar quando o agente confirmar 100% de cobertura factual de toda a extensão da transcrição.

### Fase 8: Processamento Incremental e Redação de Prosa por Cena (Terceira Etapa)
Apenas após validar a cobertura da lista de cenas, o agente inicia a redação do capítulo. A escrita deve ser realizada **cena por cena, separadamente e em ordem sequencial**:
1. Processe cada cena de forma isolada, redigindo sua prosa com alta densidade literária, sem pressa e sem sintetizar excessivamente as informações.
2. Mantenha os diálogos significativos em discurso direto (travessões ou aspas), eliminando apenas gagueiras ou ruídos fora de personagem.
3. Rastreie a continuidade espacial e o estado dos personagens entre a cena anterior e a atual.
4. Repita esse processo de redação dedicada para cada cena individualmente, acumulando a prosa até que todas as cenas da lista tenham sido completamente processadas.

### Fase 9: Gravação e Polimento do Markdown Consolidado (Quarta Etapa)
Una a prosa de todas as cenas processadas em um único texto contínuo e aplique o template em `.agent/skills/rpg-session-narrator/templates/output_template.md`.
1. Faça uma revisão final na prosa consolidada para suavizar as quebras de parágrafos entre cenas, assegurando que o texto flua como um capítulo de livro contínuo e unificado (sem divisões de títulos ou listas).
2. Salve o arquivo na pasta `journal/` da campanha (`content/campaigns/<campaign-slug>/journal/`), respeitando o maior número de capítulo sequencial existente (`NNN-slug-da-sessao.md`).
3. Configure no frontmatter apenas a chave `params.kind: "journal_entry"` (não insira a chave `kind` de nível superior), com `draft: false`, `visibility: "players"` e `status: "ready"`.

### Fase 10: Relatório de Processamento
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
