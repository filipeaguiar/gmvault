## Why

As fichas Hugo são adequadas para consulta pelos jogadores, mas dependem hoje de uma extensão externa para serem abertas dentro do Owlbear Rodeo. Essa extensão não é controlada pelo projeto, o que impede integrar de forma confiável o SDK do Owlbear e o Dice+.

Uma extensão própria, estática e hospedada junto ao site Hugo permite controlar todo o fluxo da ficha, manter a seleção de personagem simples e oferecer rolagens Dice+ como aprimoramento progressivo sem backend ou framework pesado.

## What Changes

- Criar uma extensão própria para Owlbear Rodeo em `static/owlbear-character-sheet/`, publicada pelo mesmo GitHub Pages do site e identificada separadamente da extensão externa `gm-vault`.
- Adicionar um manifest instalável com `manifest_version: 1` e versão inicial `1.0.0`, abrindo uma interface leve de fichas em um popover do Owlbear.
- Gerar pelo Hugo um catálogo JSON contendo apenas personagens seguros para jogadores (`visibility: players` ou `public`).
- Permitir que cada jogador selecione sua ficha e persistir essa escolha localmente no navegador.
- Carregar a página Hugo selecionada em um iframe interno da extensão, preservando a ficha como fonte canônica de conteúdo.
- Integrar a extensão diretamente ao SDK do Owlbear Rodeo e aos canais documentados do Dice+.
- Reintroduzir rolagens na ficha por aprimoramento progressivo: bônus e fórmulas permanecem texto de referência fora da extensão e se tornam controles clicáveis somente após uma ponte Dice+ válida.
- Usar o próprio valor numérico ou fórmula como controle, sem botão textual separado de “Rolar”.
- Exibir estados acessíveis de disponibilidade, rolagem, resultado, erro e timeout sem bloquear a consulta da ficha.
- Continuar funcionando como site Hugo normal quando aberto fora do Owlbear ou sem Dice+.

## Capabilities

### New Capabilities

- `owlbear-character-extension`: Manifest, interface, catálogo de personagens, seleção persistente, iframe controlado e comunicação entre a extensão própria, fichas Hugo, SDK Owlbear e Dice+.

### Modified Capabilities

- `rpg-character-sheet`: A ficha passa a oferecer metadados estruturados de rolagem e aprimoramento progressivo dos valores numéricos quando executada dentro da extensão própria.

## Impact

- Novos arquivos estáticos em `static/owlbear-character-sheet/` para manifest, shell da extensão, JavaScript, CSS e ícone.
- Novo output JSON ou template Hugo para catálogo de personagens visíveis a jogadores.
- Alterações no layout de personagem para expor fórmulas estruturadas sem tornar a rolagem obrigatória.
- Integração com `@owlbear-rodeo/sdk`, preferencialmente como módulo ESM com versão fixa e sem framework de interface.
- Integração com os canais Dice+ `dice-plus/isReady`, `dice-plus/roll-request`, `{source}/roll-result` e `{source}/roll-error`.
- Persistência apenas local da ficha selecionada; nenhuma base de dados, autenticação ou backend será introduzido.
- O campo `visibility` continuará sendo metadado editorial e não será tratado como segurança real.
