## 1. Levantamento e modelagem
- [ ] 1.1 Consolidar o contrato de dados de conjuração na ficha.
- [ ] 1.2 Mapear quais classes do projeto entram em prepared, known, pact, hybrid e feature-granted.
- [ ] 1.3 Definir compatibilidade com `char_info.spells`, `char_info.class_spells` e `spell_slots` existentes.

## 2. Layout e componentes
- [ ] 2.1 Quebrar a aba atual em partials menores e reutilizáveis.
- [ ] 2.2 Criar bloco de counters no topo.
- [ ] 2.3 Criar barra de busca e filtros por nível.
- [ ] 2.4 Criar linha/card de spell com badges, metadados e ação contextual.
- [ ] 2.5 Introduzir estados vazios e mensagens específicas por tipo de conjurador.

## 3. Interação
- [ ] 3.1 Atualizar o JS para filtrar por nome e nível sem depender de uma única classe.
- [ ] 3.2 Implementar ações Prepare/Unprepare apenas quando o perfil permitir.
- [ ] 3.3 Garantir clonagem/atualização segura dos cards entre listas.
- [ ] 3.4 Preservar o comportamento progressivo quando não houver bridge Dice+.

## 4. Backend / importadores
- [ ] 4.1 Atualizar `create_character.py` e `edit_character.py` para gerar o novo contrato de spellcasting.
- [ ] 4.2 Ajustar `import_dndbeyond.py` para distinguir magias preparadas, conhecidas, sempre-preparadas e por origem.
- [ ] 4.3 Revisar `dnd_utils.py` para suportar a classificação por perfil e não apenas por classe.
- [ ] 4.4 Atualizar `archetypes/character.md` e documentação de dados.

## 5. Validação
- [ ] 5.1 Criar testes para prepared caster, known caster, pact magic e híbrido.
- [ ] 5.2 Validar a renderização com personagem sem magia.
- [ ] 5.3 Validar que a aba continua funcional com dados legados.
- [ ] 5.4 Validar build Hugo e regressão visual da aba.

## 6. Encerramento
- [ ] 6.1 Revisar a spec/ossatura criada e registrar decisões finais.
- [ ] 6.2 Se necessário, dividir a implementação em uma fase 1 (layout + dados) e fase 2 (interações + persistência).
