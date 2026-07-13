## 1. Implementação de Layouts do Hugo

- [x] 1.1 Atualizar `layouts/partials/helpers/gmvault_adventure_category.html` para achatar a exportação JSON de Cenas
- [x] 1.2 Atualizar `layouts/partials/kinds/adventure.html` para renderizar a timeline com Cenas diretamente
- [x] 1.3 Ajustar as asserções em `tests/test_adventure_introduction_rendering.py` para as novas tags e itens da timeline

## 2. Ajustes no Importador Python

- [x] 2.1 Refatorar `import_campaign.py` em Modo 2 (Antologia) para remover a criação da sessão física `001-inicio`
- [x] 2.2 Corrigir o mapeamento de `scene_ref` em `import_campaign.py` para apontar diretamente sob o diretório da aventura

## 3. Migração de Conteúdo e Testes

- [x] 3.1 Mover fisicamente as cenas traduzidas de `welcome-to-the-radiant-citadel` e `salted-legacy` das subpastas `001-inicio` para a raiz correspondente
- [x] 3.2 Executar a suíte de testes unitários (`pytest`) e compilação do Hugo para atestar sucesso total
