## 1. Funções auxiliares em dnd_utils.py

- [x] 1.1 Criar `get_class_features_at_level(class_data, class_name, subclass_short, level)` que retorna lista de características novas da classe e subclasse para um nível específico
- [x] 1.2 Criar `get_asi_levels(class_name)` que retorna os níveis em que a classe ganha ASI/Talento (geralmente 4, 8, 12, 16, 19)

## 2. Função principal de level up em edit_character.py

- [x] 2.1 Criar `level_up_character(post, path)` que orquestra todo o fluxo de subida de nível
- [x] 2.2 Implementar passo 1: Ler ficha, incrementar level/class_level, recalcular prof_bonus
- [x] 2.3 Implementar passo 2: Recalcular HP com 3 opções: Média (automática), Rolagem (usuário digita o resultado do dado), Fixo (usuário digita valor)
- [x] 2.4 Implementar passo 3: Buscar e exibir novas características de classe/subclasse
- [x] 2.5 Implementar passo 4: Oferecer Talentos/ASI se nível aplicável
- [x] 2.6 Implementar passo 5: Recalcular slots de magia, saves, skills, e salvar

## 3. Integração no menu

- [x] 3.1 Adicionar opção "Subir de nível" no menu de edição do personagem
- [x] 3.2 Chamar `level_up_character()` quando a opção é selecionada

## 4. Validação

- [x] 4.1 Testar level up de um personagem nível 1→2 e verificar HP, prof_bonus, features
- [x] 4.2 Testar level up para nível 4 e verificar oferta de Talento/ASI
- [x] 4.3 Verificar que equipment, spells e skills existentes são preservados
- [x] 4.4 Executar `hugo -D --gc --minify` para garantir que fichas atualizadas renderizam
