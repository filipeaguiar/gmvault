## Context

A página de classe usa `layouts/partials/kinds/class.html`. O template apresenta o título, metadados, uma ficha compacta e o conteúdo Markdown em `.class-body`; progressões importadas normalmente são listas com entradas como `Nível 1: [Rage](...)`. A seção de subclasses ainda usa estilos inline e links sem um componente visual próprio.

O projeto já possui variáveis CSS, cards, badges e a biblioteca de ícones RuneScape usada em outros layouts. A solução deve ser estática, leve, acessível e compatível com conteúdo Markdown já existente.

## Goals / Non-Goals

**Goals:**

- Dar hierarquia visual clara ao título da classe, metadados, progressão e subclasses.
- Transformar níveis e entradas de progressão em elementos escaneáveis com cards/linhas, cores e ícones.
- Estilizar links internos do compêndio sem depender do estilo padrão do navegador.
- Usar ícones por classes CSS existentes, sem caracteres Unicode decorativos ou emojis.
- Preservar o conteúdo e os links Markdown existentes.
- Manter layout responsivo em telas estreitas e iframes.

**Non-Goals:**

- Não alterar regras, traduções, slugs ou URLs do compêndio.
- Não reescrever o Markdown das classes importadas.
- Não adicionar JavaScript ou bibliotecas externas.
- Não criar um sistema visual diferente para cada classe.

## Decisions

### 1. Estrutura semântica no partial de classe

O partial receberá classes CSS específicas para o cabeçalho da classe, o bloco de informações, o corpo da progressão e a lista de subclasses. A estrutura continuará usando `.Content` para o Markdown, evitando duplicação de regras.

Alternativa descartada: transformar cada entrada Markdown no template com parsing textual, pois isso seria frágil para conteúdo legado e traduções diferentes.

### 2. Gerar e estilizar agrupamentos por nível

As páginas de classe manterão a lista de características, mas o gerador de progressão e a migração do conteúdo existente inserirão headings `Nível X` quando o nível mudar. O CSS de `.class-body` tratará esses headings como divisores de grupo com linhas horizontais; as entradas serão listas simples com espaçamento, sem transformar cada item em um card. O mesmo HTML será reutilizado quando a página de classe for exibida dentro da ficha do personagem.

Cada característica disponível deverá apontar para uma página de regra do compêndio com o texto correspondente. Quando a página não existir, o gerador deverá criar um stub com as entradas da característica antes de inserir o link.

Alternativa descartada: inferir e agrupar níveis somente no CSS, pois CSS não consegue transformar de forma confiável o prefixo textual `Nível X` em grupos sem alterar a estrutura HTML.

Alternativa descartada: substituir listas por HTML gerado no importador, pois exigiria alterar conteúdo existente e aumentaria o acoplamento entre importação e apresentação.

### 3. Links internos com componente visual consistente

Links dentro da progressão e subclasses usarão cor de destaque, peso tipográfico, estados hover/focus e ícone RuneScape inserido no HTML do template quando necessário. O render hook de links deverá prefixar o caminho configurado em `site.BaseURL` para destinos internos absolutos, como `/compendium/rules/...`. Nenhum símbolo Unicode será usado como decoração.

Alternativa descartada: usar `::before` com caracteres Unicode, pois há uma exigência explícita de evitar Unicode e isso pode variar entre fontes.

### 4. Responsividade por CSS

A progressão usará largura fluida, `min-width: 0`, quebra de texto e uma coluna em telas estreitas. A página não terá overflow horizontal causado por títulos ou links longos.

## Risks / Trade-offs

- **[Risco]** Estruturas Markdown incomuns podem não receber o mesmo tratamento visual. → **Mitigação:** manter seletores limitados ao bloco `.class-body` e preservar a renderização padrão como fallback.
- **[Risco]** Links longos podem aumentar a altura dos cards. → **Mitigação:** aplicar `overflow-wrap: anywhere` e layout fluido.
- **[Risco]** Cores podem perder contraste em modo escuro. → **Mitigação:** usar variáveis existentes e validar build/renderização nos temas disponíveis.
- **[Risco]** Ícones RuneScape podem não estar disponíveis em uma instalação externa. → **Mitigação:** manter o texto do título/link sempre visível e tratar o ícone como complemento visual.

## Migration Plan

1. Atualizar o partial de classe com classes semânticas e ícones existentes.
2. Atualizar o gerador de progressão e o conteúdo de classes existente para inserir headings por nível e gerar stubs das características ausentes.
3. Adicionar o render hook de links internos para respeitar o `baseURL`.
4. Adicionar CSS da progressão, links e subclasses.
3. Renderizar uma classe com progressão longa e uma subclasse para verificar a hierarquia.
4. Executar build Hugo e revisar que os links continuam apontando para `/compendium/rules/.../`.
5. Reverter removendo as classes e regras CSS novas, sem alterar o conteúdo Markdown.

## Open Questions

Nenhuma. A mudança deve usar as classes de ícones já presentes no projeto e não usar Unicode.
