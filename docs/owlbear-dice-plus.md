# Integração com Dice+

A ficha de personagem é carregada em um iframe. O JavaScript da ficha não importa o SDK do Owlbear; ele envia mensagens versionadas ao documento pai. O documento pai da extensão `gm-vault` é responsável por chamar `OBR.broadcast`.

## Identificador da extensão

O manifest publicado em `https://owlbear-gm-vault.netlify.app/manifest.json` não possui um campo `id`. O adaptador usa inicialmente o identificador estável `gm-vault`:

```js
const GM_VAULT_EXTENSION_ID = "gm-vault";
```

Esse valor é usado pelo Dice+ para os canais:

```text
gm-vault/roll-result
gm-vault/roll-error
```

## Cliente da ficha

O asset `assets/js/dice-plus-bridge.js` expõe `window.GMVaultDice`. O asset `assets/js/dice-roll-controls.js` localiza elementos com `data-dice-roll`, envia a notação estruturada e mostra os estados da rolagem.

A ficha pode configurar a origem do pai antes do carregamento dos módulos:

```html
<script>
  window.GMVaultDiceConfig = {
    targetOrigin: "https://owlbear-gm-vault.netlify.app"
  };
</script>
```

Quando a configuração não existe, o cliente usa a origem do `document.referrer`. Ele nunca usa `*` como destino.

## Adaptador do host

`assets/js/dice-plus-host.js` é um módulo sem dependência fixa de npm. O host fornece a instância já inicializada do SDK e a janela do iframe:

```js
import { createDicePlusHost } from "./dice-plus-host.js";

const iframe = document.querySelector("#character-frame");
const iframeOrigin = new URL(iframe.src, window.location.href).origin;

const diceBridge = createDicePlusHost({
  OBR,
  iframeWindow: iframe.contentWindow,
  iframeOrigin,
  extensionId: "gm-vault"
});

diceBridge.start();

// Ao fechar ou recarregar a superfície:
diceBridge.destroy();
```

O host deve criar o adaptador depois de `OBR.onReady` e depois de o iframe existir. No código atual publicado, esse ciclo começa em `js/main.js`, no callback de `OBR.onReady`, que inicializa o `ExtensionController`.

## Mensagens e segurança

O host aceita apenas mensagens com:

- canal `gm-vault/dice`;
- versão `1`;
- tipo conhecido;
- origem exata da ficha;
- `event.source` igual à janela do iframe;
- notação compatível com o Dice+;
- destino entre `everyone`, `self`, `dm` e `gm_only`.

O `playerId` e o `playerName` são obtidos pelo host usando `OBR.player`. A ficha não pode fornecer esses valores.

## Limitações atuais

O repositório deste site não contém o código-fonte da extensão pai publicada no Netlify. A integração do adaptador em `js/main.js` precisa ser feita no repositório da `gm-vault` ou carregando este módulo pelo host. O site Hugo continua funcionando sem a extensão e sem o Dice+.
