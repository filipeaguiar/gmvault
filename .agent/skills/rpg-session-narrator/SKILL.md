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

### Fase 6: Mapeamento Consolidado de Eventos (Primeira Etapa)
Antes de iniciar a redação do texto literário, o agente SHALL fazer uma leitura completa de todas as cenas e dados do JSON intermediário para mapear a linha do tempo (timeline) completa da sessão:
1. Identifique e organize cronologicamente o máximo de eventos, interações e acontecimentos possíveis de toda a sessão de jogo.
2. Mapeie exatamente quais personagens e NPCs estavam envolvidos ativamente ou presentes em cada um desses eventos.
3. Rastreie a continuidade espacial (locais visitados) e o estado físico ou mecânico dos personagens (sucessos/falhas em testes, ferimentos, itens obtidos).
4. Mantenha essa estrutura de eventos consolidada em sua memória de contexto para guiar a escrita unificada.

### Fase 7: Redação Sincronizada em Prosa Literária (Segunda Etapa)
Apenas após concluir o mapeamento consolidado de todos os eventos da sessão, o agente deve proceder para a escrita do capítulo em prosa literária contínua, observando as seguintes regras:
- **Continuidade Unificada:** Escreva o texto de forma a fluir organicamente de um evento para o próximo, garantindo que o encadeamento espacial e temporal dos fatos faça sentido literário completo (estilo romance).
- **Estilo Narrativo:** Use o tom configurado (ex: terceira pessoa, tempo passado, prosa de fantasia envolvente formatada como capítulo de livro contínuo).
- **Sem Mecânicas ou Seções:** Remova termos como "rolou dado", "teste de Percepção", etc., traduzindo-os em ações. O texto deve fluir de forma inteiramente contínua, sem subtítulos ou seções para resumos, listas de personagens/NPCs ou observações.
- **Preservação de Fatos:** Não altere decisões tomadas, não transforme falhas de dados em acertos, não invente ações que não constam no arquivo.
- **Diálogos:** Preserve os diálogos originais ditos pelos jogadores como personagens em discurso direto (usando travessões ou aspas) sempre que possível. Unifique falas fracionadas ou limpe pequenas gagueiras para fluidez, mas mantenha a interpretação original e falas dos personagens.

### Fase 8: Gravação do Markdown Consolidado (Capítulo do Journal)
O arquivo Markdown final deve ser gerado usando o template de saída configurado em `.agent/skills/rpg-session-narrator/templates/output_template.md`.
O arquivo final deve ser salvo no diretório `journal/` da campanha (`content/campaigns/<campaign-slug>/journal/`).
O nome do arquivo deve seguir o padrão de numeração sequencial de capítulos. Para definir o nome:
1. Examine a pasta `journal/` para ver quais arquivos numerados já existem (ex: `001-chegada.md`, `002-primeira-missao.md`).
2. Identifique o maior índice de capítulo existente (ex: se o maior é 002, o próximo será 003).
3. Salve o novo capítulo com o nome formatado como `NNN-slug-da-sessao.md` (ex: `003-o-mercado-noturno.md`).
4. Defina no frontmatter o campo `params.kind: "journal_entry"` (não utilize a chave `kind` no nível superior, pois ela foi removida nas versões modernas do Hugo), com `draft: false`, `visibility: "players"` e `status: "ready"`.
**IMPORTANTE:** Nunca sobrescreva silenciosamente um arquivo existente. Se ele existir, pergunte se deve substituir ou criar uma nova versão (ex: `*-v2.md`).

### Fase 9: Relatório de Processamento
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
