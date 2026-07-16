## 1. Catálogo Hugo de personagens

- [x] 1.1 Definir um output JSON dedicado para personagens no `hugo.yaml` e criar o template correspondente.
- [x] 1.2 Filtrar o catálogo para páginas `character` construídas com `visibility: players` ou `public`, omitindo GM, archived, visibilidade ausente e drafts fora do build.
- [x] 1.3 Incluir no catálogo título, URL canônica, resumo, campanha e imagem opcional com JSON válido e URLs compatíveis com `baseURL`.
- [x] 1.4 Criar testes do catálogo cobrindo inclusão player/public, exclusão GM e ausência de personagens elegíveis.

## 2. Shell e manifest da extensão

- [x] 2.1 Criar `static/owlbear-character-sheet/manifest.json` com `manifest_version: 1`, versão inicial `1.0.0`, nome, autor, descrição, ícone, popover e dimensões válidas sob o prefixo de publicação `/gmvault/`, sem usar `gm-vault` como identidade da extensão.
- [x] 2.2 Criar o shell estático em `static/owlbear-character-sheet/index.html` com estrutura semântica para status, seleção de personagem e iframe.
- [x] 2.3 Criar CSS leve e responsivo para o popover, seletor, estado vazio, status e iframe sem overflow horizontal.
- [x] 2.4 Importar uma versão fixa do SDK Owlbear no JavaScript do shell, aguardar `OBR.onReady` e tratar execução fora do Owlbear sem falha fatal.
- [x] 2.5 Buscar o catálogo JSON, renderizar apenas entradas válidas e mostrar estados de carregamento, vazio e erro.
- [x] 2.6 Persistir a seleção em `localStorage` com chave baseada no ID do jogador quando disponível e permitir trocar de ficha.
- [x] 2.7 Carregar a URL selecionada em um único iframe e invalidar preferências que não existam mais no catálogo.

## 3. Ponte da extensão e Dice+

- [x] 3.1 Definir canal, versão, tipos de mensagem, origem esperada, source `io.github.filipeaguiar.character-sheet` e limites de timeout em um módulo central.
- [x] 3.2 Vincular a ponte ao `contentWindow` do iframe ativo após o carregamento e destruir o vínculo ao trocar personagem ou descarregar o shell.
- [x] 3.3 Validar `event.source`, origem, versão, tipo, destino e notação antes de aceitar qualquer solicitação da ficha.
- [x] 3.4 Implementar readiness do Dice+ em `dice-plus/isReady`, filtrando eco do request, resposta incorreta e timeout.
- [x] 3.5 Implementar envio para `dice-plus/roll-request` com identidade de `OBR.player`, `rollId`, target, notação, popup, timestamp e source estável.
- [x] 3.6 Implementar listeners únicos para `io.github.filipeaguiar.character-sheet/roll-result` e `/roll-error`, correlacionando cada resposta com iframe, request e ação.
- [x] 3.7 Implementar timeout, erro estruturado e limpeza de listeners, timers e pendências no ciclo de vida da extensão.

## 4. Aprimoramento progressivo da ficha

- [x] 4.1 Expor metadados estruturados de notação em salvaguardas, perícias, ataques, danos e ações explicitamente configuradas, mantendo os valores como texto padrão.
- [x] 4.2 Criar cliente versionado `postMessage` para handshake, solicitação, resultado, erro e timeout, sem importar o SDK Owlbear na ficha.
- [x] 4.3 Transformar somente valores elegíveis em controles após readiness confirmado, usando o próprio número ou fórmula e sem botão textual “Rolar”.
- [x] 4.4 Implementar estados acessíveis de pronto, rolando, concluído, erro e timeout com resultado associado à ação correta.
- [x] 4.5 Garantir que fichas abertas fora da extensão ou sem Dice+ permaneçam integralmente legíveis e sem controles indisponíveis.
- [x] 4.6 Adicionar estilos responsivos, foco visível e estados que não dependam apenas de cor.

## 5. Testes, documentação e publicação

- [ ] 5.1 Criar testes do shell para catálogo, seleção persistida, preferência inválida e fallback fora do Owlbear.
- [ ] 5.2 Criar testes da ponte com `OBR.broadcast` falso cobrindo readiness, eco, request, identidade, resultado, erro, timeout e limpeza.
- [ ] 5.3 Criar testes do cliente da ficha cobrindo aprimoramento progressivo, payload, múltiplas rolagens, correlação e mensagens rejeitadas.
- [x] 5.4 Validar teclado, foco, live regions, largura do popover e ausência de overflow em iframe estreito.
- [x] 5.5 Documentar instalação pela URL do manifest, seleção de personagem, dependência opcional do Dice+ e diagnóstico básico.
- [x] 5.6 Executar testes relacionados, `hugo --gc --minify` e verificar manifest, catálogo, assets e ausência de dependência SDK nas páginas comuns.
- [ ] 5.7 Testar manualmente no Owlbear sem Dice+, com Dice+ e com dois jogadores usando seleções locais diferentes.
