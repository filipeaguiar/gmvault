## 1. Atualizações no Importador D&D Beyond

- [ ] 1.1 Atualizar `import_dndbeyond.py` para extrair metadados avançados de armas do inventário (propriedades, alcance, tipo de dano, categoria) e gravá-los na lista de equipamentos.
- [ ] 1.2 Atualizar `import_dndbeyond.py` para mapear modificadores mágicos (sobreposição de atributos, bônus de atributos, bônus de CA e testes de resistência) de itens ativos no inventário para o objeto `modifiers` de cada item.
- [ ] 1.3 Garantir que os valores base de atributos (`char_info.stats`) e CA base (`char_info.ac`) sejam gravados no frontmatter sem acumular previamente os modificadores mágicos individuais dos equipamentos, evitando contagem dupla.

## 2. Lógica de Cálculo Dinâmico no Template Hugo

- [ ] 2.1 Inicializar os atributos dinâmicos usando `newScratch` no topo de `layouts/partials/kinds/character.html` a partir dos dados do frontmatter.
- [ ] 2.2 Iterar sobre os itens equipados (`equipped: true`) para aplicar modificações de atributos (`stat_override` e `stat_bonus`), obtendo os valores finais de Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma.
- [ ] 2.3 Calcular os modificadores finais de atributos usando a fórmula matemática correta e extrair o delta em relação aos modificadores base originais.
- [ ] 2.4 Aplicar o delta dos modificadores de atributos nos testes de resistência e nas perícias calculadas durante a renderização das respectivas abas.
- [ ] 2.5 Recalcular dinamicamente a CA da personagem somando a base da armadura equipada, o modificador de Destreza (aplicando regras de limite de armadura leve/média/pesada), escudos e os bônus mágicos de CA (`modifiers.ac_bonus`) dos itens equipados.

## 3. Interface Visual na Ficha

- [ ] 3.1 Exibir alcance, tipo de dano e propriedades de armas de forma organizada na aba de Equipamentos.
- [ ] 3.2 Adicionar estilo visual diferenciador para itens equipados e não equipados (ex: opacidade 0.5 e badge visual para itens inativos) no CSS e no template.

## 4. Validação e Compilação

- [ ] 4.1 Executar importação de teste de personagem contendo itens mágicos (como luvas de força ou anel de proteção) para verificar a geração correta do frontmatter.
- [ ] 4.2 Compilar o site com `hugo --gc --minify` e testar a renderização da ficha para garantir que os cálculos batem com o esperado.
