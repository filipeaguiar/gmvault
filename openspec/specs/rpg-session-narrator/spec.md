# rpg-session-narrator Specification

## Purpose
TBD - created by archiving change rpg-session-narrator. Update Purpose after archive.
## Requirements
### Requirement: Persistent Memory Configuration
O sistema SHALL ler e persistir uma estrutura de dados de configuração (memória da campanha) em formato YAML contendo metadados da campanha, mapeamento de jogadores para personagens, aliases de voz e termos de fantasia com erros comuns.

#### Scenario: Missing configuration initialization
- **WHEN** a skill é executada e o arquivo de memória persistente não existe ou carece de campos obrigatórios
- **THEN** o sistema SHALL interagir com o usuário solicitando os dados obrigatórios de configuração e gravando-os em `memory.yaml`.

#### Scenario: Manual metadata updates
- **WHEN** o usuário solicitar comandos ou frases de ativação para gerenciar a memória
- **THEN** o sistema SHALL permitir a revisão e correção direta de nomes, aliases, NPCs e termos cadastrados.

### Requirement: Sharing Microphone Resolution
O sistema SHALL implementar heurísticas para analisar falas registradas sob o nome do GM (microfone compartilhado) e tentar atribuí-las ao respectivo jogador presencial.

#### Scenario: Contextual voice attribution
- **WHEN** uma fala sob o nome do mestre declarar uma ação em primeira pessoa típica de um personagem presencial cadastrado
- **THEN** o sistema SHALL associar provisoriamente a fala a esse personagem, registrando o nível de confiança.

#### Scenario: Ambiguity resolution fallback
- **WHEN** uma fala sob o microfone compartilhado for ambígua e não puder ser resolvida com segurança
- **THEN** o sistema SHALL usar formulações narrativas neutras sem inventar autoria e apresentar a dúvida na tabela de ambiguidades para confirmação do usuário.

### Requirement: Phonetic Term Normalization
O sistema SHALL analisar o texto da transcrição em busca de termos próprios e corrigir falhas de reconhecimento por aproximação fonética baseando-se no léxico da memória.

#### Scenario: Correction of fantasy names
- **WHEN** termos correspondentes a erros comuns como "se abre um corpo" forem detectados na transcrição
- **THEN** o sistema SHALL normalizar para o termo canônico "Siabsungkoh" após análise contextual para evitar corrupções cegas de palavras comuns.

### Requirement: Text Segmenting and Structuring
O sistema SHALL segmentar transcrições grandes em blocos cronológicos por cenas para processamento intermediário.

#### Scenario: Multi-stage block processing
- **WHEN** uma transcrição com mais de 100 KB for fornecida para processamento
- **THEN** o sistema SHALL dividi-la sem quebrar falas ao meio, extrair metadados estruturados de eventos, dados e participantes por cena e gerar um JSON intermediário.

### Requirement: Prosaic Narrative Writing
O sistema SHALL converter a estrutura intermediária consolidada em uma crônica literária em prosa, em formato Markdown, respeitando regras estritas de fidelidade aos fatos.

#### Scenario: Output file generation
- **WHEN** consolidando a narrativa de uma sessão
- **THEN** o sistema SHALL salvar o resultado em formato Markdown na pasta correta da aventura da campanha, contendo cabeçalho YAML, resumo, prosa literária livre de jargões de regras/dados, e tabelas de NPCs/pendências, sem sobrescrever arquivos silenciosamente.

