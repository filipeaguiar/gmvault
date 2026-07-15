## Why

As fichas de personagem geradas pelo Hugo são consultadas dentro da extensão `gm-vault`, mas atualmente a realização de testes, ataques, salvamentos e danos exige trocar manualmente para o Dice+. Isso interrompe o fluxo da sessão e impede que a ficha apresente o resultado da rolagem no contexto da ação executada.

O Owlbear Rodeo oferece comunicação entre extensões pelo `OBR.broadcast`, e o Dice+ documenta canais específicos para verificar disponibilidade, enviar rolagens e receber resultados ou erros. A integração deve usar esses contratos sem acoplar o conteúdo Markdown ao serviço de rolagem.

## What Changes

- Adicionar uma capacidade de integração entre a ficha da personagem e o Dice+ por meio da extensão `gm-vault`.
- Expor ações de rolagem na ficha para expressões de dados compatíveis com Dice+, incluindo testes, salvamentos, ataques e danos quando houver dados estruturados para a ação.
- Verificar a disponibilidade do Dice+ pelo canal `dice-plus/isReady` antes de enviar uma rolagem.
- Enviar solicitações pelo canal `dice-plus/roll-request` com identificador único, jogador, destino, notação, origem e comportamento de popup.
- Escutar os canais específicos de resultado e erro derivados do identificador da extensão `gm-vault`.
- Mostrar estado de carregamento, resultado e erro na ficha sem bloquear a consulta dos demais dados do personagem.
- Definir uma ponte estável entre o JavaScript estático da ficha Hugo e o código da extensão que possui acesso ao SDK do Owlbear Rodeo.
- Manter funcionamento degradado quando a ficha for aberta fora do Owlbear Rodeo ou quando o Dice+ não estiver instalado.
- Documentar permissões, origem da mensagem, correlação por `rollId` e limpeza dos listeners.

## Capabilities

### New Capabilities

- `owlbear-dice-plus-bridge`: Comunicação segura e tolerante a falhas entre fichas renderizadas pelo Hugo, a extensão `gm-vault`, o SDK do Owlbear Rodeo e os canais públicos de integração do Dice+.

### Modified Capabilities

Nenhuma. A integração adiciona ações à ficha, mas não altera o contrato editorial ou o modelo de conteúdo existente.

## Impact

- **Extensão `gm-vault`**: deverá inicializar o SDK do Owlbear Rodeo, verificar o Dice+, encaminhar solicitações da ficha e devolver resultados ou erros.
- **JavaScript e CSS do site Hugo**: deverão fornecer controles de rolagem, estados visuais e uma API de ponte sem dependências pesadas.
- **Templates e dados de personagem**: poderão adicionar metadados de notação e rótulos às ações sem duplicar regras de rolagem.
- **Build estático**: continuará funcionando fora do Owlbear Rodeo; o código deverá detectar a ausência da ponte ou do SDK.
- **APIs externas**: integração com `@owlbear-rodeo/sdk` e com os canais documentados do Dice+:
  - `dice-plus/isReady`
  - `dice-plus/roll-request`
  - `{source}/roll-result`
  - `{source}/roll-error`
- **Dependência operacional**: o Dice+ precisa estar instalado e disponível na sala do Owlbear Rodeo para que as rolagens sejam executadas.

Referências consultadas:

- Owlbear Rodeo SDK: https://github.com/owlbear-rodeo/sdk
- API de broadcast do SDK: `src/api/BroadcastApi.ts`, com `sendMessage`, `onMessage` e destinos `REMOTE`, `LOCAL` e `ALL`.
- Documentação da extensão Dice+: https://extensions.owlbear.rodeo/dice-plus
