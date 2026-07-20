## Why

As páginas de classe mostram apenas links para características por nível, obrigando o jogador a abrir diversas páginas para entender suas opções. Subclasses têm o mesmo problema, o que dificulta comparação e escolha.

## What Changes

- Renderizar o texto descritivo de cada característica de classe diretamente na página da classe, agrupado por nível.
- Renderizar o texto descritivo das características de subclasse diretamente na página de cada subclasse.
- Manter um link discreto para a página canônica da característica quando ela existir.
- Usar fallback seguro para referências ausentes ou conteúdo sem descrição.
- Preservar visibilidade: páginas player-facing não devem expor navegação ou conteúdo GM.

## Capabilities

### New Capabilities
- `inline-class-feature-descriptions`: Exibe descrições das características referenciadas nas páginas de classe e subclasse, no contexto de sua progressão.

### Modified Capabilities
- `index-layout`: Os layouts de classe e subclasse passam a resolver e apresentar conteúdo de características relacionadas.

## Impact

- Layouts de classe, subclasse e partials de relações em `layouts/`.
- CSS do compêndio para hierarquia, densidade e leitura em telas pequenas.
- Nenhuma alteração em URLs, importadores ou modelo de dados de conteúdo.
