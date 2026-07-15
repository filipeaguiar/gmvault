# RPG Session Narrator Skill

Esta skill para o agente Antigravity automatiza a transformação de transcrições de sessões de RPG de mesa (por exemplo, exportações de texto de áudios do Google Meet) em crônicas narrativas e diários em prosa literária em formato Markdown. Ela foi projetada sob medida para a estrutura de campanhas do projeto RPG Campaign Vault (`gmvault`).

## Recursos Principais

1. **Memória de Campanha Persistente (`memory.yaml`)**: Salva preferências do Mestre, aliases de transcrição de jogadores, nomes canônicos e variações de NPCs, locais e termos de fantasia para reutilização entre sessões.
2. **Resolução de Microfone Compartilhado**: Detecta falas de jogadores presenciais que utilizam o mesmo microfone físico do mestre e aparecem com o nome do mestre na transcrição, utilizando heurísticas avançadas (verbos em primeira pessoa, referências a fichas, perguntas do GM anteriores e continuidade de rolagem de dados).
3. **Normalização Fonética e Ortográfica**: Mapeia termos de fantasia incorretamente transcritos e nomes próprios (ex: "se abre um corpo" -> "Siabsungkoh") baseando-se no léxico da memória de campanha.
4. **Segmentação Cronológica em Cenas**: Divide transcrições de arquivos grandes em blocos cronológicos estruturados para evitar estouro da janela de contexto.
5. **Redação Artística Fiel**: Transforma o JSON estruturado intermediário em prosa contínua (estilo capítulo de livro, sem subdivisões de resumos ou tabelas), mantendo estrita fidelidade factual e preservando as interpretações e falas em discurso direto dos personagens em jogo sempre que possível.

---

## Arquivos Criados no Diretório da Skill

- `SKILL.md`: Arquivo principal que define o comportamento da skill, fases de trabalho e regras de fidelidade para o agente Antigravity.
- `memory.yaml`: Arquivo YAML contendo a memória persistente dos metadados da campanha, jogadores, NPCs e termos.
- `templates/output_template.md`: Template Markdown padrão para as crônicas de narrativas geradas.
- `scripts/process_transcript.py`: Script auxiliar Python que realiza a limpeza, normalização léxica, resolução de microfone compartilhado e estruturação em JSON intermediário.
- `tests/test_narrator.py`: Unittests Python para validar os mecanismos de limpeza, normalização e resolução de autoria de voz.

---

## Como Utilizar a Skill

### 1. Configurando a Campanha

Antes de processar a primeira sessão, você deve configurar a campanha executando:
```bash
python3 .agent/skills/rpg-session-narrator/scripts/process_transcript.py setup
```
O script fará perguntas interativas sobre metadados, jogadores, NPCs e pronomes, e salvará as respostas em `memory.yaml`. Você também pode editar o arquivo `memory.yaml` manualmente a qualquer momento.

Para revisar as configurações atuais:
```bash
python3 .agent/skills/rpg-session-narrator/scripts/process_transcript.py review
```

### 2. Processando uma Sessão

Para processar uma transcrição:
1. Certifique-se de que o arquivo da transcrição bruta (ex: `sessao_12_bruta.txt`) está na pasta `transcriptions/` na raiz do projeto.
2. Ative a skill no chat com o comando: `Processar sessão` ou descrevendo o caminho da transcrição.
3. O agente fará perguntas rápidas específicas daquela sessão (como data, número, e quais jogadores estavam presenciais dividindo o microfone do mestre).
4. O script Python processará a transcrição e gerará um JSON estruturado intermediário.
5. O agente exibirá uma tabela contendo ambiguidades de autoria de voz não resolvidas deterministicamente para você confirmar rapidamente (ex: quem disse "Eu ataco" sob o microfone do mestre).
6. Após sua confirmação, o agente gerará a crônica em prosa literária contínua no estilo configurado (sem subtítulos ou tabelas) e a salvará como um novo capítulo numerado na pasta do diário da campanha (ex: `content/campaigns/<campaign>/journal/003-nome-da-sessao.md`), preservando os diálogos originais dos personagens em discurso direto.

---

## Executando os Testes

Para garantir que a lógica de resolução e normalização fonética esteja intacta, você pode executar o script de testes:
```bash
python3 .agent/skills/rpg-session-narrator/tests/test_narrator.py
```
O script testará cenários fictícios de limpeza de ruídos, substituições fonéticas e a heurística de continuidade de rolagem de dados em microfones compartilhados.
