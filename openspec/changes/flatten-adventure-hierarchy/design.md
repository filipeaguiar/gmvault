## Context

Atualmente, o repositório e o site estático organizam campanhas contendo Aventuras, que contêm Sessões, que por sua vez contêm Cenas (estrutura de 3 níveis). Isso introduz arquivos e diretórios vazios/redundantes de sessões intermediárias (como a subpasta `001-inicio/` e arquivos `001-inicio/_index.md`) que poluem a árvore de arquivos e adicionam cliques desnecessários na interface.

## Goals / Non-Goals

**Goals:**
- Eliminar o nível "Sessão" da exibição do site, listando as Cenas diretamente sob as Aventuras na linha do tempo de preparos de jogo.
- Achatamento da geração do JSON do `gm-vault` para que as Cenas pertençam diretamente à categoria da Aventura.
- Adaptar o importador Python para gerar as cenas de novos capítulos na raiz do diretório de cada Aventura.
- Preservar retrocompatibilidade total com cenas antigas aninhadas sob subpastas de sessões legadas.

**Non-Goals:**
- Não removeremos o layout `kinds/session.html` do Hugo, pois sessões legadas ainda necessitam dele para renderização direta, se acessadas por permalink.
- Não alteraremos o comportamento das campanhas no Modo 1 ("Livro Inteiro como Única Aventura"), onde cada capítulo vira de fato uma sessão.

## Decisions

### 1. Coleta Recursiva de Cenas no Hugo
- **Escolha:** Usar `.RegularPagesRecursive` ou iteração aninhada de `.Pages` sob sessões e aventuras para coletar todas as cenas filhas e descendentes.
- **Razão:** Isso garante que tanto as novas cenas (salvas diretamente na pasta da aventura) quanto as cenas legadas (salvas dentro de pastas de sessões) sejam listadas unificadamente na timeline da aventura.

### 2. Achatamento de Categorias no Exportador JSON
- **Escolha:** Refatorar o helper `gmvault_adventure_category.html` para buscar todas as cenas descendentes usando o prefixo do link da aventura e inseri-las na categoria `"Cenas de <Aventura>"`.
- **Razão:** Permite a importação fluida de todas as cenas na ferramenta externa do `gm-vault` sem requerer nós ou pastas intermediárias de sessões.

### 3. Remoção de create_session_structure no Modo 2 do Importador
- **Escolha:** Setar a variável de diretório `scenes_dir` diretamente para `adv_dir` em `import_campaign.py`.
- **Razão:** Evita a criação física de subpastas `001-inicio` e arquivos `_index.md` de rascunhos de sessão órfãs na antologia.

## Risks / Trade-offs

- **[Risco]** Perda de traduções anteriores localizadas sob `001-inicio/`.  
  *Mitigação:* Migrar fisicamente via shell e git checkout todos os arquivos Markdown traduzidos em português das pastas de sessões para a raiz da aventura correspondente antes de remover as pastas legadas.
