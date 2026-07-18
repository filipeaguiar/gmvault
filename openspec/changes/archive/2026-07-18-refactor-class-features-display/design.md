## Context

A seção de características de classe atualmente usa:
```html
<article class="class-feature-card">
  <div class="class-feature-card-title">
    <i class="ra ra-lightning-bolt"></i>
    <strong>Feature Name</strong>
  </div>
  <!-- compendium content -->
</article>
```

Enquanto equipamentos usam:
```html
<article class="equipment-card weapon-card">
  <header class="equipment-card-header">
    <span class="equipment-card-icon"><i class="ra ra-broadsword"></i></span>
    <div class="equipment-card-heading">
      <strong class="equipment-card-name">Weapon Name</strong>
      <div class="equipment-badges">
        <span class="equipment-badge">Corpo a corpo</span>
      </div>
    </div>
  </header>
  <!-- stats grid, properties, content -->
</article>
```

## Goals / Non-Goals

**Goals:**
- Padronizar visual das features de classe com equipamentos
- Adicionar badges informativos (nível, fonte)
- Manter ícone contextual por tipo de feature

**Non-Goals:**
- Mudar dados do front matter
- Afetar outras seções da ficha

## Decisions

**Reusar classes CSS existentes**
- Usar `equipment-card`, `equipment-card-header`, `equipment-card-icon`, `equipment-card-heading`, `equipment-badges`
- Adicionar nova variação `feature-card` para cor da borda esquerda

**Mapeamento de ícones**
- `ra-lightning-bolt` para ações/habilidades
- `ra-star` para características passivas
- `ra-diamond` para talentos

**Badges**
- Nível: quando disponível nos dados
- Fonte: "Classe" ou "Subclasse"

## Risks / Trade-offs

- **Features sem dados de nível** → Badge de nível será omitido
- **CSS pode conflitar** → Usar namespace `feature-card` para isolar
