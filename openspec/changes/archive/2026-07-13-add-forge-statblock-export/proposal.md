## Why

Os personagens e monstros do vault já possuem dados estruturados em Markdown, mas não há uma exportação compatível com a extensão Forge! do Owlbear Rodeo. Isso obriga a recriar statblocks manualmente e dificulta manter o material do compêndio e da campanha sincronizado com a mesa.

## What Changes

- Criar uma exportação JSON global compatível com o formato de statblocks do Forge!, gerada automaticamente em cada build do Hugo.
- Incluir todos os personagens de jogadores e todos os monstros do compêndio no export, com IDs determinísticos e metadados Forge mapeados a partir dos dados estruturados disponíveis.
- Preservar uma ordem determinística dos registros, colocando personagens antes dos monstros e ordenando cada grupo por peso e nome.
- Gerar o arquivo em uma URL estável para importação no Owlbear Rodeo, sem depender de backend ou etapa manual.
- Exibir no índice do Compêndio um link copiável para o JSON do Forge!.
- Exibir na página de cada campanha um link copiável para o JSON `gm-vault.json` correspondente.
- Manter os exports existentes do GM Vault sem alteração de formato.

## Capabilities

### New Capabilities

- `forge-statblock-export`: exportação Hugo de personagens e monstros para o JSON compatível com Forge!.

### Modified Capabilities

- `content-model`: páginas de campanha e do Compêndio devem expor links copiáveis para os exports JSON relevantes.

## Impact

- `hugo.yaml` e um novo template JSON de output do Hugo para o Forge!.
- Novos helpers/layouts para converter `char_info` e `stats` em metadados Forge.
- Layout da página de campanha e índice do Compêndio.
- Possível novo `content/compendium/_index.md` para fornecer uma página estável ao índice do Compêndio.
- Novo arquivo gerado em `public/exports/forge/statblocks.json` durante o build; não será versionado como artefato manual.
- Consumidores externos: extensão Forge! do Owlbear Rodeo e ferramenta GM Vault.
