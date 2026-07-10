## Context

O projeto já possui importadores que criam muitos arquivos Markdown como `draft: true`, frequentemente em inglês. Esses arquivos são úteis estruturalmente, mas ainda exigem preparação editorial antes de uso em mesa.

A nova etapa deve operar como pós-processamento local e opcional:

```text
import_campaign.py / import_dndbeyond.py
        ↓
Markdown draft em inglês
        ↓
translate_drafts.py
        ↓
Markdown draft em português, ainda marcado para revisão
```

Argos Translate é adequado porque permite tradução local sem depender de API externa paga. O ponto crítico é preservar termos de D&D e estruturas Markdown/YAML, pois tradução automática pura tende a corromper nomes de regras, magias, atributos, links e blocos técnicos.

## Goals / Non-Goals

**Goals:**
- Criar script local para traduzir páginas Markdown com `draft: true`.
- Usar Argos Translate para tradução inglês → português.
- Preservar front matter YAML e estruturas Markdown sensíveis.
- Tokenizar termos de D&D antes da tradução e substituir tokens por traduções controladas depois.
- Manter glossário versionado e editável manualmente.
- Oferecer execução segura com dry-run, escopo por `compendium` ou `campaign`, e limitação opcional por caminho.
- Marcar arquivos traduzidos para revisão humana.

**Non-Goals:**
- Garantir tradução perfeita ou publicação automática sem revisão.
- Traduzir conteúdo que não esteja em draft por padrão.
- Implementar interface web ou integração dinâmica no Hugo.
- Resolver direitos autorais de conteúdo importado de fontes externas.
- Substituir revisão editorial/manual do mestre.

## Decisions

### 1. Script separado em vez de acoplar aos importadores
Criar `translate_drafts.py` como etapa independente.

Racional: importação e tradução têm ritmos diferentes. O usuário pode importar várias fontes, revisar diffs e traduzir apenas subconjuntos.

Alternativa considerada: adicionar tradução diretamente aos importadores. Isso tornaria importações mais lentas, mais frágeis e menos previsíveis.

### 2. Processar apenas arquivos Markdown com `draft: true` por padrão
O script deve ler front matter YAML e selecionar apenas páginas draft, salvo opção explícita.

O escopo primário deve ser informado por parâmetro:

```text
--scope compendium
  → traduz drafts em content/compendium/

--scope campaign --campaign <campaign-slug>
  → traduz drafts em content/campaigns/<campaign-slug>/
```

Uma opção `--path` pode restringir ainda mais o escopo, mas não deve permitir escapar do escopo selecionado.

Racional: reduz risco de sobrescrever conteúdo já revisado ou publicado e separa claramente tradução de compêndio global e tradução de campanha específica.

Alternativa considerada: traduzir tudo sob `content/`. Isso é perigoso para conteúdo pronto, conteúdo de jogadores e páginas já revisadas.

### 3. Preservar front matter estrutural
O front matter deve ser parseado e reemitido com alterações mínimas. Campos estruturais como `kind`, `visibility`, `status`, `related`, `npcs`, `locations`, `compendium_refs`, `stats`, `char_info`, `spell_info`, `item_info`, `weight`, `draft` e URLs internas não devem ser traduzidos automaticamente.

Campos textuais seguros, como `title` e `summary`, podem ser traduzidos se a opção do script permitir. O corpo Markdown deve ser o alvo principal.

### 4. Tokenização antes da tradução
Antes de chamar Argos, o script deve substituir termos controlados por tokens estáveis:

```text
Armor Class → __GMV_TOKEN_0001__
Hit Points  → __GMV_TOKEN_0002__
Saving Throw → __GMV_TOKEN_0003__
```

Depois da tradução automática, os tokens devem ser substituídos pelas traduções do glossário:

```text
__GMV_TOKEN_0001__ → Classe de Armadura
__GMV_TOKEN_0002__ → Pontos de Vida
__GMV_TOKEN_0003__ → Salvaguarda
```

Racional: evita que a tradução estatística ou literal varie entre páginas.

### 5. Glossário versionado e explícito
Criar arquivo de glossário editável, preferencialmente JSON por simplicidade em Python sem dependência extra:

```text
translation_glossary.json
```

Formato sugerido:

```json
{
  "Armor Class": "Classe de Armadura",
  "Hit Points": "Pontos de Vida"
}
```

O glossário deve conter termos de regras, atributos, condições, ações, escolas de magia, tipos de criatura e expressões recorrentes. A implementação deve começar com um glossário mínimo e permitir expansão manual.

### 6. Proteger blocos Markdown sensíveis
O script deve proteger antes da tradução:

- fenced code blocks;
- inline code;
- URLs e destinos de links;
- imagens Markdown;
- shortcodes Hugo, se existirem;
- dados de dice notation `[[...]]`;
- paths internos como `/campaigns/.../` e `/compendium/.../`;
- front matter YAML estrutural.

Racional: tradução automática pode quebrar sintaxe e referências.

### 7. Metadados pós-tradução
Após traduzir, o script deve adicionar ou atualizar metadados indicando que a tradução foi automática e precisa de revisão. Exemplo:

```yaml
translation:
  source_language: "en"
  target_language: "pt-BR"
  engine: "argos"
  status: "machine_translated"
```

O `draft` deve permanecer `true` por padrão. O script não deve promover conteúdo para `ready` automaticamente.

### 8. Segurança operacional
A execução padrão deve ser conservadora:

```bash
python3 translate_drafts.py --scope compendium --dry-run
python3 translate_drafts.py --scope compendium --path content/compendium/spells --apply
python3 translate_drafts.py --scope campaign --campaign cidadela-radiante --dry-run
python3 translate_drafts.py --scope campaign --campaign cidadela-radiante --apply
```

O script deve mostrar quais arquivos seriam alterados e só escrever quando `--apply` for fornecido.

## Risks / Trade-offs

- Tradução automática pode gerar termos inadequados → Mitigar com glossário, tokens e revisão humana obrigatória.
- Glossário chamado de “oficial” pode implicar completude ou direitos sobre texto publicado → Mitigar documentando que o glossário é controlado pelo projeto e contém termos de tradução padronizados, não reprodução de regras.
- Argos pode não estar instalado ou não ter modelo en→pt → Mitigar com erro claro e instrução de instalação/modelo.
- Reemitir YAML pode mudar formatação → Mitigar com alteração mínima e preservação de campos estruturais.
- Tokenização pode substituir texto dentro de URLs ou código → Mitigar protegendo blocos sensíveis antes dos termos do glossário.
- Tradução de arquivos grandes pode ser lenta → Mitigar com processamento por arquivo, escopo por `--path` e feedback de progresso.
