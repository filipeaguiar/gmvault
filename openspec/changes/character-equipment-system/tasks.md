## 1. Atualizações no Importador D&D Beyond

- [x] 1.1 Atualizar `import_dndbeyond.py` para obter e gravar propriedades detalhadas de itens (cost, weight, properties, range, damage, damage_type, modifiers) no compêndio global sob a chave `item_info` do frontmatter.
- [x] 1.2 Atualizar `import_dndbeyond.py` para exportar a lista de equipamentos do personagem sob `char_info.equipment` contendo apenas referências limpas (`name`, `ref`, `quantity`, `equipped`).
- [x] 1.3 Garantir que os atributos base (`char_info.stats`) e CA base (`char_info.ac`) gravados no topo do frontmatter do personagem não tenham os modificadores mágicos pré-aplicados.

## 2. Lógica de Cálculo Dinâmico no Template Hugo

- [x] 2.1 Inicializar os atributos base usando `newScratch` no topo de `layouts/partials/kinds/character.html`.
- [x] 2.2 Resolver cada equipamento do personagem através de `site.GetPage .ref`. Se estiver equipado (`equipped: true`), ler os modificadores do compêndio (`item_info.modifiers.stat_override` e `item_info.modifiers.stat_bonus`) e aplicar no scratch.
- [x] 2.3 Calcular os modificadores finais de atributos e extrair o delta em relação aos modificadores base originais do personagem.
- [x] 2.4 Somar o delta dos modificadores de atributos nos testes de resistência e perícias calculadas durante a renderização.
- [x] 2.5 Recalcular dinamicamente a CA da personagem buscando as propriedades da armadura equipada (tipo e AC), escudo equipado e somando os modificadores de `modifiers.ac_bonus` de todos os itens mágicos equipados ativos.

## 3. Interface Visual na Ficha

- [x] 3.1 Exibir na aba de Equipamentos os detalhes das armas (alcance, dano, propriedades) resolvidos dinamicamente da página do compêndio.
- [x] 3.2 Aplicar opacidade `0.5` e indicador visual "Não Equipado" para itens não ativos na aba de Equipamentos.

## 4. Validação e Compilação

- [ ] 4.1 Testar importação de personagem com itens mágicos (como luvas de força ou anel de proteção) e verificar se o frontmatter gerado está limpo e os compêndios estão ricos.
- [ ] 4.2 Executar build local `hugo --gc --minify` e verificar se a ficha renderiza os atributos calculados e a CA corretos.
