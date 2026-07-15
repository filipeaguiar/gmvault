## 1. Contrato e cliente do iframe

- [x] 1.1 Definir constantes, versão, tipos de mensagem e limites de timeout do contrato `gm-vault/dice` em um módulo JavaScript sem dependência do SDK.
- [x] 1.2 Implementar o cliente no iframe usando `window.parent.postMessage`, `requestId`/`rollId` e `targetOrigin` configurável, com fallback seguro quando o parent não fornecer a ponte.
- [x] 1.3 Implementar recebimento de eventos de disponibilidade, resultado e erro, filtrando por versão, tipo e identificador de solicitação.
- [x] 1.4 Garantir que listeners, timers e solicitações pendentes do cliente sejam removidos quando a página for descarregada ou o controlador for destruído.

## 2. Adaptador da extensão gm-vault

- [x] 2.1 Identificar o ponto de inicialização da superfície que cria o iframe e registrar a origem permitida da ficha e a referência exata ao iframe.
- [x] 2.2 Definir e documentar uma constante estável para `source` dos canais específicos do Dice+; o manifest atual não possui `id`, portanto usar inicialmente `gm-vault` e validar o recebimento dos canais em uma sala real.
- [x] 2.3 Implementar o listener pai para validar origem, `event.source`, versão, tipo, payload e ações permitidas antes de encaminhar mensagens.
- [x] 2.4 Implementar a verificação `dice-plus/isReady` com `requestId`, timeout e resposta de disponibilidade para o iframe.
- [x] 2.5 Implementar o envio de `dice-plus/roll-request` com identidade obtida por `OBR.player`, `rollId` único, `rollTarget`, notação, `showResults`, timestamp e `source` oficial.
- [x] 2.6 Implementar listeners únicos para `${source}/roll-result` e `${source}/roll-error`, correlacionar por `rollId` e responder somente ao iframe solicitante.
- [x] 2.7 Limpar listeners do SDK, listener de `message`, timers e mapa de pendências ao fechar ou recarregar a superfície da extensão.

## 3. Ações roláveis na ficha

- [x] 3.1 Mapear as ações atuais da ficha e definir metadados estruturados para testes, salvamentos, ataques, danos e outras ações com notação Dice+ válida.
- [x] 3.2 Adicionar controles acessíveis às ações que possuam metadados de rolagem, sem criar controles para texto sem fórmula validada.
- [x] 3.3 Integrar os controles ao cliente do iframe e implementar estados indisponível, pronto, preparando, rolando, concluído e erro.
- [x] 3.4 Renderizar total, resumo e dados agrupados recebidos do Dice+ como texto seguro, preservando o contexto da ação e permitindo nova tentativa após erro ou timeout.
- [x] 3.5 Adicionar estilos leves e responsivos para os controles, estados, foco visível e mensagens de indisponibilidade.
- [x] 3.6 Incluir o JavaScript e CSS nos layouts necessários sem tornar o SDK do Owlbear uma dependência do build Hugo.

## 4. Testes e compatibilidade

- [x] 4.1 Criar testes do cliente do iframe com uma ponte falsa, cobrindo payload, correlação por `rollId`, rejeição de mensagens inválidas e limpeza.
- [x] 4.2 Criar testes do adaptador host com `OBR.broadcast` simulado, cobrindo readiness, request, resultado, erro, timeout e identidade do jogador.
- [x] 4.3 Testar múltiplas rolagens simultâneas e garantir que cada resultado seja entregue somente à ação e ao iframe corretos.
- [x] 4.4 Testar ficha fora do Owlbear, Dice+ ausente e payload de ação inválido, confirmando que o conteúdo continua legível e que não há erro não tratado.
- [x] 4.5 Executar `hugo --gc --minify` e os testes relacionados, verificando que o build não importa `@owlbear-rodeo/sdk`.
- [ ] 4.6 Testar manualmente em uma sala Owlbear com Dice+ instalado, incluindo popup, rolagem visível e retorno de erro.
