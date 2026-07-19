## Context

As fichas guardam nível, atributos, ações, recursos, magias e referências do compêndio em `char_info`. O compêndio local agora inclui classes, subclasses e features XPHB, mas a operação de edição ainda exige que o mestre aplique manualmente os ganhos de nível. A solução deve permanecer local, sem banco de dados, e preservar fichas legadas e edições editoriais.

## Goals / Non-Goals

**Goals:**
- Aplicar de modo interativo ganhos determinísticos de uma classe/subclasse XPHB ao elevar um nível.
- Sincronizar referências de features, ações e conteúdo compartilhado usando os resolvedores existentes.
- Recalcular valores derivados seguros e solicitar escolhas que não podem ser inferidas.
- Exibir uma prévia e gravar somente após confirmação.

**Non-Goals:**
- Implementar multiclasse, reespecificação, progressão de espécies/backgrounds ou todas as regras opcionais.
- Inferir escolhas de talentos, magias, invocações, manobras ou opções similares.
- Interpretar livremente prosa de regras para calcular usos de recursos nesta mudança.

## Decisions

### Fonte de verdade: dados 5e.tools XPHB e compêndio local
O resolvedor usará os dados de classe/subclasse selecionados com prioridade XPHB, restringindo features ao nível novo e à subclasse registrada. As páginas locais de rules permanecem a fonte de descrição e URLs; os JSONs fornecem nível e identidade da feature.

Alternativa descartada: extrair a progressão do Markdown renderizado. O Markdown é editorial, traduzível e não oferece estrutura estável para cálculos.

### Operação planejada antes da gravação
A subida construirá um plano contendo mudanças automáticas, escolhas pendentes e referências a sincronizar. O editor exibirá o plano e só persistirá após confirmação. Isso evita arquivos parcialmente atualizados se uma escolha for cancelada.

### Estado operacional mínimo
A operação atualizará nível da classe e nível total, bônus de proficiência, pontos de vida conforme a opção selecionada e espaços de magia derivados. Features recebidas serão adicionadas como ações/referências sem duplicação. Dados não reconhecidos e campos manuais existentes serão preservados.

### Escolhas explícitas
Quando o nível concede escolha (talento, magia, invocação, opções de feature ou aumento de atributo), o fluxo apresentará uma etapa específica ou registrará pendência; nunca escolherá automaticamente por texto de regra.

## Risks / Trade-offs

- [Dados XPHB com feature repetida ou slug compartilhado] → Deduplicar por referência canônica e manter o nome/origem da feature na ficha.
- [Feature com efeitos mecânicos não estruturados] → Adicionar a referência e informar que ajustes operacionais exigem escolha/edição explícita.
- [Fichas legadas incompletas] → Validar classe, nível e subclasse antes de planejar; abortar sem gravar quando faltarem dados essenciais.
- [Divergência entre nível total e nível de classe] → Suportar apenas aumento da classe principal nesta primeira versão e validar a consistência.

## Migration Plan

1. Introduzir helpers puros para construir e validar o plano de subida.
2. Integrar a operação ao editor sem alterar fichas até confirmação.
3. Adicionar fixtures XPHB para classes, subclasses e escolhas.
4. Manter o caminho de edição manual como fallback.
5. Rollback: remover a ação do editor; fichas atualizadas continuam válidas porque usam campos e URLs existentes.

## Open Questions

- Definir a UX exata para Aumento de Valor de Atributo e talentos no primeiro corte.
- Definir quais recursos com usos escalonáveis receberão cálculo estruturado nesta mudança ou em uma extensão posterior.
