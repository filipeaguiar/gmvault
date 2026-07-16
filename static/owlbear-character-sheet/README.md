# Extensão de Fichas para Owlbear Rodeo

Extensão própria para abrir fichas de personagem do GMVault dentro do Owlbear Rodeo, com integração opcional ao Dice+.

## Instalação

1. No Owlbear Rodeo, acesse **Configurações > Extensões**.
2. Cole a URL do manifest:
   ```
   https://filipeaguiar.github.io/gmvault/owlbear-character-sheet/manifest.json
   ```
3. Clique em **Adicionar**. A extensão aparecerá como "Fichas de Personagem" no painel lateral.

## Uso

### Seleção de personagem

- Ao abrir a extensão, o catálogo de personagens visíveis a jogadores é carregado automaticamente.
- Clique no personagem desejado para abrir a ficha.
- A seleção é salva localmente no navegador por jogador. Na próxima vez que abrir a extensão, a ficha será carregada automaticamente.
- Para trocar de personagem, clique no botão **⟵ Trocar** no canto superior.

### Catálogo

O catálogo inclui apenas personagens com:
- `visibility: "players"` ou `visibility: "public"`
- Não marcados como `draft: true` no build de produção

Personagens GM, arquivados ou sem visibilidade definida não aparecem.

> **Nota:** `visibility` é um metadado editorial, não uma medida de segurança. URLs públicas continuam acessíveis diretamente.

## Integração com Dice+

### Dependência opcional

A extensão funciona sem o Dice+ instalado. Nesse caso:
- Fichas são exibidas normalmente como referência.
- Valores numéricos (bônus, fórmulas) permanecem como texto estático.

Com o Dice+ instalado e ativo:
- Os valores de salvaguardas, perícias e fórmulas de ataque/dano recebem uma pequena borda quadrada e se tornam clicáveis.
- Clicar em um valor envia uma rolagem pelo Dice+.
- O resultado permanece no popup e no histórico do Dice+, sem ser inserido na ficha.

### Fluxo de rolagem

1. A extensão verifica se o Dice+ está pronto ao carregar.
2. Se disponível, os valores numéricos na ficha recebem uma pequena borda quadrada.
3. Ao clicar ou pressionar Enter/Espaço em um valor, a rolagem é enviada.
4. Durante a rolagem, a borda fica tracejada e o valor perde opacidade temporariamente.
5. Ao receber resultado, erro ou timeout, o valor retorna ao estado pronto.
6. O Dice+ exibe o resultado e mantém seu histórico; a ficha não duplica essas informações.

### Canais Dice+ utilizados

| Canal | Uso |
|---|---|
| `dice-plus/isReady` | Verificação de disponibilidade |
| `dice-plus/roll-request` | Envio de rolagem |
| `io.github.filipeaguiar.character-sheet/roll-result` | Recebimento de resultado |
| `io.github.filipeaguiar.character-sheet/roll-error` | Recebimento de erro |

## Diagnóstico

### A extensão mostra "Modo local (sem Owlbear)"

A extensão foi aberta fora do Owlbear Rodeo (diretamente no navegador). Isso é normal para testes. A seleção de personagem e a ficha funcionam, mas não há integração Dice+.

### A extensão mostra "Conectado: [nome]" sem "Dice+ ativo"

O Owlbear está conectado, mas o Dice+ não está instalado ou não respondeu. A ficha funciona como referência. Instale o Dice+ na sala para habilitar rolagens.

### "Erro ao carregar catálogo"

O arquivo `character-catalog.json` não foi encontrado. Verifique se o site Hugo foi publicado corretamente com `hugo --gc --minify`.

### Valores não são clicáveis

1. Verifique se o Dice+ está instalado e ativo na sala.
2. Reabra a extensão (feche e abra o popover).
3. Verifique se a barra de status mostra "Dice+ ativo".

## Arquitetura

```
Owlbear Rodeo
└── Extensão (index.html)
    ├── @owlbear-rodeo/sdk (ESM CDN)
    ├── bridge.js (ponte Dice+)
    ├── protocol.js (constantes do protocolo)
    └── iframe → ficha Hugo
        └── sheet-client.js (cliente postMessage)
```

- O shell da extensão (`index.html` + `main.js`) importa o SDK Owlbear e gerencia seleção, iframe e ponte Dice+.
- A ficha Hugo é carregada em iframe e se comunica via `postMessage` versionado.
- O `sheet-client.js` roda dentro da ficha e faz aprimoramento progressivo dos valores.
- Páginas Hugo comuns **não** carregam o SDK Owlbear.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `manifest.json` | Manifest Owlbear para instalação |
| `icon.svg` | Ícone da extensão |
| `index.html` | Shell HTML da extensão |
| `style.css` | Estilos do shell |
| `main.js` | Lógica principal do shell |
| `bridge.js` | Ponte postMessage + Dice+ |
| `protocol.js` | Constantes do protocolo |
| `sheet-client.js` | Cliente da ficha (aprimoramento progressivo) |
