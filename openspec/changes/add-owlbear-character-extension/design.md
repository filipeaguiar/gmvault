## Context

O site Hugo publica fichas de personagem estáticas no GitHub Pages. Essas páginas são legíveis em navegador e em iframe, mas não possuem acesso confiável ao SDK do Owlbear quando carregadas por uma extensão de terceiros. O experimento anterior confirmou que uma ponte Dice+ funciona quando o código host roda no mesmo contexto da extensão que possui `OBR`, porém não pode ser instalado a partir de um iframe cross-origin.

A nova arquitetura coloca um shell controlado pelo projeto como filho direto do Owlbear. Esse shell carrega a ficha Hugo em um iframe interno e se torna responsável por seleção de personagem, SDK, comunicação Dice+ e validação de mensagens.

```text
Owlbear Rodeo
└── Extensão de Fichas (GitHub Pages)
    ├── @owlbear-rodeo/sdk
    ├── ponte Dice+
    └── iframe da ficha Hugo
```

O site e a extensão permanecerão estáticos, hospedados sob `https://filipeaguiar.github.io/gmvault/`, sem backend, autenticação ou framework JavaScript pesado.

## Goals / Non-Goals

**Goals:**

- Publicar um manifest Owlbear instalável junto ao site Hugo.
- Oferecer uma interface leve para selecionar e abrir personagens player-facing.
- Persistir a escolha por jogador e navegador sem serviço externo.
- Controlar o iframe da ficha e a ponte `postMessage` em uma origem conhecida.
- Integrar rolagens da ficha ao Dice+ usando o SDK oficial do Owlbear.
- Manter a ficha plenamente legível sem Owlbear, extensão ou Dice+.
- Tornar o próprio número ou fórmula clicável somente quando a integração estiver pronta.
- Preservar baixo peso, JavaScript vanilla e compatibilidade com máquinas modestas.

**Non-Goals:**

- Substituir Forge como ficha operacional completa ou rastreador de iniciativa.
- Persistir HP, recursos consumidos ou histórico de rolagens no servidor.
- Criar autenticação ou usar `visibility` como segurança real.
- Publicar conteúdo GM no catálogo da extensão.
- Implementar física de dados, parser próprio ou interface alternativa ao Dice+.
- Sincronizar automaticamente seleção de personagem entre dispositivos.

## Decisions

### 1. Hospedar a extensão no mesmo GitHub Pages

Os arquivos ficarão em `static/owlbear-character-sheet/`, produzindo URLs estáveis sob `/gmvault/owlbear-character-sheet/`. O manifest usará caminhos que incluem o prefixo de publicação `/gmvault/`, mas a identidade da extensão e seus canais não usarão `gm-vault`, evitando confusão com a extensão externa existente.

Essa escolha reutiliza o deploy atual, HTTPS e cache estático. Hospedagem separada em Netlify foi descartada porque recriaria dependência externa sem benefício necessário para o MVP.

### 2. Usar um shell de extensão em vez de um manifest por personagem

O manifest abrirá `owlbear-character-sheet/index.html`. O shell buscará um catálogo de personagens gerado pelo Hugo, exibirá a seleção e carregará a ficha escolhida em um iframe.

Um manifest por personagem seria mais simples inicialmente, mas exigiria instalar várias extensões e não escalaria para múltiplas campanhas e jogadores.

### 3. Gerar um catálogo JSON player-facing

O Hugo gerará um arquivo JSON dedicado com personagens construídos, não draft, e `visibility` igual a `players` ou `public`. Cada item terá título, URL canônica, campanha quando disponível, resumo e imagem opcional.

O filtro serve para navegação editorial, não autorização. URLs públicas continuam acessíveis diretamente.

### 4. Persistir a seleção localmente por jogador

Após `OBR.onReady`, o shell obterá `OBR.player.getId()` e usará uma chave de `localStorage` que inclua o ID do jogador. Sem SDK disponível, usará uma chave local genérica. A seleção poderá ser alterada por um controle visível.

`OBR.player.metadata` foi evitado no MVP porque sincronizaria estado na sala e aumentaria o acoplamento. A seleção não é dado de campanha nem exige compartilhamento.

### 5. Manter a ficha em iframe e usar uma ponte versionada

O shell e a ficha se comunicarão por `postMessage` com canal e versão explícitos. O shell validará `event.source`, origem, tipo e payload. Como ambos serão hospedados no mesmo domínio, a origem esperada poderá ser calculada diretamente; ainda assim, a implementação não acessará o DOM interno da ficha.

Isso mantém separação de responsabilidades e permite testar cliente e host isoladamente.

### 6. Integrar Dice+ no shell

O shell importará uma versão fixa do SDK Owlbear, aguardará `OBR.onReady` e implementará:

- readiness em `dice-plus/isReady`;
- requests em `dice-plus/roll-request`;
- resultados em `io.github.filipeaguiar.character-sheet/roll-result`;
- erros em `io.github.filipeaguiar.character-sheet/roll-error`.

Cada pedido terá `rollId`, identidade obtida por `OBR.player`, `rollTarget`, notação, `showResults`, timestamp e `source: "io.github.filipeaguiar.character-sheet"`. O mesmo namespace será usado no protocolo privado entre shell e ficha. Listeners serão únicos e correlacionados por `rollId`.

### 7. Aplicar aprimoramento progressivo aos números

O HTML Hugo exibirá bônus e fórmulas como texto normal com metadados `data-*`. O cliente da ficha só os transformará em controles de teclado/clique depois que o shell confirmar que Dice+ está disponível.

Fora da extensão, ou sem Dice+, os valores permanecerão texto de referência e não haverá botão textual separado. Essa abordagem evita controles quebrados e atende ao uso da ficha apenas para consulta.

### 8. Manter o SDK fora do build principal do Hugo

Somente o shell da extensão importará `@owlbear-rodeo/sdk`, por URL ESM com versão fixa ou arquivo vendorizado. As páginas comuns não dependerão do SDK. O código será vanilla JavaScript e não introduzirá npm ou bundler no MVP.

## Risks / Trade-offs

- **[Risco]** Mudanças no contrato do Dice+ podem quebrar a ponte. **Mitigação:** centralizar canais e tipos, validar readiness e manter testes com `OBR.broadcast` falso.
- **[Risco]** O CDN ESM do SDK pode ficar indisponível. **Mitigação:** fixar versão e permitir vendorização posterior do módulo.
- **[Risco]** `localStorage` pode ser particionado ou limpo pelo navegador. **Mitigação:** manter seletor acessível e tratar ausência da preferência sem erro.
- **[Risco]** O catálogo pode expor uma ficha marcada incorretamente como player-facing. **Mitigação:** filtrar estritamente `players/public` e documentar que visibilidade não é segurança.
- **[Risco]** Um iframe pode enviar notação arbitrária. **Mitigação:** validar origem, source window, tamanho, caracteres permitidos e destinos de rolagem no shell.
- **[Trade-off]** A seleção não acompanha o jogador em outro dispositivo. **Mitigação:** aceitar no MVP; sincronização por metadata pode ser proposta separadamente.
- **[Trade-off]** O popup nativo do Dice+ e o resultado resumido da ficha podem duplicar informação. **Mitigação:** manter `showResults` configurável e priorizar o popup no MVP.

## Migration Plan

1. Adicionar catálogo JSON de personagens e validar filtros de visibilidade.
2. Publicar shell e manifest sem rolagens, validando instalação e seleção no Owlbear.
3. Adicionar ponte versionada entre shell e ficha.
4. Adicionar integração Dice+ e aprimoramento progressivo dos valores.
5. Testar em navegador comum, Owlbear sem Dice+ e Owlbear com Dice+.
6. Instalar o manifest definitivo na sala e remover dependência operacional do `gm-vault` para fichas.
7. Em rollback, remover a extensão da sala; as URLs Hugo continuam funcionando normalmente.

## Open Questions

- O ícone definitivo da extensão será específico para fichas ou reutilizará o ícone atual do projeto?
- O `rollTarget` padrão será `everyone` ou `self`? O design recomenda `everyone` inicialmente para reproduzir o comportamento esperado na mesa.
- A primeira versão deve listar personagens de todas as campanhas ou permitir filtrar por campanha no catálogo?
