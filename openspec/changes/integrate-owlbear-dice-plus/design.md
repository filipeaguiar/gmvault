## Context

As fichas são páginas estáticas geradas pelo Hugo e abertas em um iframe criado pela extensão `gm-vault` no Owlbear Rodeo. O repositório atual contém o site e seus templates, mas não contém um aplicativo JavaScript completo da extensão anfitriã. Portanto, a integração precisa separar a camada visual da ficha da camada pai que possui acesso ao SDK `@owlbear-rodeo/sdk`.

O SDK do Owlbear expõe `OBR.broadcast.sendMessage(channel, data, options)` e `OBR.broadcast.onMessage(channel, callback)`. O Dice+ usa estes canais:

- `dice-plus/isReady` para uma solicitação de disponibilidade e resposta correlacionada por `requestId`;
- `dice-plus/roll-request` para solicitações de rolagem;
- `{source}/roll-result` para resultados, em que `source` é o identificador da extensão solicitante;
- `{source}/roll-error` para erros.

A documentação do Dice+ exige que uma solicitação contenha `rollId`, `playerId`, `playerName`, `rollTarget`, `diceNotation`, `showResults`, `timestamp` e `source`. O resultado contém `totalValue`, `rollSummary` e grupos individuais de dados.

## Goals / Non-Goals

**Goals:**

- Permitir que ações renderizadas na ficha solicitem rolagens ao Dice+.
- Receber resultados e erros sem depender de parsing do texto exibido pelo Dice+.
- Manter a ficha utilizável fora do Owlbear Rodeo e sem Dice+.
- Isolar o SDK do Owlbear no adaptador da extensão `gm-vault`.
- Correlacionar cada solicitação com `rollId` e impedir que um resultado seja exibido na ação errada.
- Preservar segurança básica no limite entre página estática e extensão, validando origem, formato e ações permitidas.
- Permitir testes locais da ficha usando um adaptador falso, sem exigir o Owlbear Rodeo.

**Non-Goals:**

- Implementar um novo motor de dados ou duplicar a física e a notação do Dice+.
- Persistir histórico de rolagens no Hugo, no GitHub ou em um banco de dados.
- Substituir a interface ou as configurações do Dice+.
- Transformar `visibility` do Hugo em mecanismo de autenticação.
- Suportar rolagens arbitrárias digitadas pelo usuário no MVP.
- Criar ou empacotar uma extensão Owlbear completa dentro deste repositório se o código anfitrião continuar externo.

## Decisions

### 1. Usar um adaptador de ponte entre a ficha e o SDK

O JavaScript do Hugo consumirá uma interface pequena, por exemplo `window.GMVaultDiceBridge.requestRoll(request)`, e não importará `@owlbear-rodeo/sdk`. O código da extensão `gm-vault` instalará esse adaptador e será o único responsável por chamar `OBR.broadcast`.

Essa escolha evita acoplar um site estático a um bundler da extensão e permite que o mesmo HTML funcione em navegador comum. A alternativa de importar o SDK diretamente nos assets Hugo é rejeitada porque exigiria um contexto Owlbear em toda visualização, dificultaria testes e misturaria responsabilidades.

### 2. Usar `postMessage` entre o iframe e a extensão pai

Como a ficha é carregada em um iframe, a ficha usará `window.parent.postMessage` com um envelope versionado, como `{ type: "gm-vault/dice-roll-request", version: 1, request }`. A extensão pai registrará um listener de `message`, validará `event.origin`, `event.source`, o tipo, os campos e a origem esperada antes de encaminhar a solicitação. A resposta será enviada de volta ao `event.source` usando o `targetOrigin` exato da ficha, nunca `*`.

A camada Hugo terá apenas o cliente da ponte e a interface visual. Não será necessário expor o SDK no iframe nem criar uma dependência de npm no build Hugo. Sem um parent compatível, os botões serão desabilitados com uma mensagem explicativa em vez de falharem silenciosamente.

### 3. Centralizar listeners e correlação no host

O host criará um único listener para `${GM_VAULT_EXTENSION_ID}/roll-result` e outro para `${GM_VAULT_EXTENSION_ID}/roll-error`, mantendo um mapa de `rollId` para solicitações pendentes e para a janela/iframe solicitante. A ficha recebe apenas o evento correspondente à sua solicitação.

O manifest publicado em `https://owlbear-gm-vault.netlify.app/manifest.json` não possui campo `id`. Portanto, o host deverá definir uma constante estável e segura para canais, inicialmente `GM_VAULT_EXTENSION_ID = "gm-vault"`, ou outro valor documentado caso o Owlbear atribua um identificador diferente. A ficha poderá receber esse valor apenas como configuração do host, mas nunca deverá inferi-lo de dados fornecidos por uma mensagem não validada.

O host também fará a verificação de disponibilidade em `dice-plus/isReady`, com `requestId` único e timeout curto. Solicitações não serão enviadas quando a verificação expirar ou indicar que o Dice+ não está disponível. Listeners e timers serão removidos ao desmontar a superfície da extensão.

A alternativa de cada botão assinar diretamente os canais é rejeitada porque multiplicaria listeners, dificultaria limpeza e permitiria que uma ficha recebesse resultados de outra ação.

### 4. Usar a notação documentada e dados estruturados da ficha

Cada ação rolável receberá uma notação validada em atributo ou configuração estruturada, além de um rótulo legível. O MVP usará notações compatíveis com Dice+ e enviará `showResults: true` por padrão para manter a animação/popup nativo; o resultado recebido será usado para atualizar o resumo na ficha. A origem será um identificador estável de `gm-vault`, e `rollTarget` terá `everyone` como padrão configurável.

A ficha não construirá notações a partir de texto livre. Atributos, bônus, proficiência, vantagem e fórmulas de dano deverão ser calculados pelo gerador ou por dados explícitos do personagem antes de chegar ao botão.

### 5. Renderizar resultados como texto seguro e progressivo

O controlador exibirá estados `indisponível`, `preparando`, `rolando`, `concluído` e `erro`. Valores numéricos, `rollSummary` e rótulos serão inseridos como texto, nunca como HTML fornecido pela mensagem. O resultado poderá mostrar o total e o resumo; os grupos individuais ficam disponíveis para uma apresentação posterior sem alterar o contrato.

### 6. Manter compatibilidade fora do Owlbear

O build Hugo não terá dependência nova obrigatória. A ausência de `GMVaultDiceBridge`, `postMessage` habilitado ou Dice+ produzirá uma ação não disponível, mas não impedirá a leitura da ficha. A CSS da integração será leve e respeitará a aparência existente da ficha.

## Risks / Trade-offs

- **[Risco]** O código da extensão `gm-vault` não está neste repositório e pode usar outro modelo de iframe ou ciclo de vida. **Mitigação:** documentar um contrato versionado de ponte, manter um adaptador falso e separar tarefas do site das tarefas do host.
- **[Risco]** O contrato do Dice+ pode mudar ou a extensão pode não estar instalada na sala. **Mitigação:** usar verificação por `isReady`, timeout, validação do payload e estado de indisponibilidade sem bloquear a ficha.
- **[Risco]** `postMessage` pode aceitar mensagens de origem indevida. **Mitigação:** restringir origens permitidas, validar `source` e esquema dos dados no host e não confiar em `playerId` vindo da página.
- **[Risco]** Uma ação pode permanecer em estado de rolagem se o Dice+ fechar ou perder a mensagem. **Mitigação:** timeout de solicitação, limpeza do mapa de pendências e retorno ao estado acionável com erro recuperável.
- **[Risco]** Exibir o resultado customizado pode divergir do popup do Dice+. **Mitigação:** usar campos documentados (`totalValue`, `rollSummary`, `groups`) e manter `showResults` configurável.
- **[Trade-off]** A ficha não poderá iniciar rolagens arbitrárias no MVP. **Mitigação:** manter uma API de dados explícita para que futuras ações possam ser adicionadas com validação.

## Migration Plan

1. Adicionar o contrato da ponte e o controlador JavaScript aos assets do Hugo, inicialmente sem alterar ações existentes que não possuam notação.
2. Adicionar controles apenas às ações com dados de rolagem válidos e manter fallback visual fora do Owlbear.
3. Implementar ou atualizar o adaptador equivalente no host `gm-vault`, instalando os listeners do SDK e validando mensagens.
4. Testar em uma sala Owlbear com Dice+ instalado, sem Dice+, com ficha fora do Owlbear e com múltiplas rolagens simultâneas.
5. Publicar o build Hugo e atualizar a extensão anfitriã de forma compatível com a versão da ponte.
6. Em rollback, remover a instalação da ponte ou desativar os controles; o conteúdo estático e as fichas continuarão sendo renderizados sem rolagens.

## Open Questions

- O valor `gm-vault` será aceito como identificador estável do campo `source` ou o Owlbear/Dice+ exigirá outro valor? O manifest atual não declara um `id`; validar a constante em uma sala real observando os canais `${source}/roll-result` e `${source}/roll-error`.
- O `rollTarget` padrão deve ser `everyone` ou ser configurável por campanha/personagem?
- O código da extensão anfitriã será incorporado a este repositório ou permanecerá em um repositório separado? 
