## 1. Contrato de dados e compatibilidade
- [x] 1.1 Definir o contrato persistido da lista de magias do personagem, incluindo referência, origem e estado básico.
- [x] 1.2 Definir como `char_info.spells`, `char_info.class_spells` e `spell_slots` antigos serão lidos como fallback.
- [x] 1.3 Mapear os perfis de conjuração necessários para os personagens do vault com base no 5e.tools.

## 2. Layout da aba de magias
- [x] 2.1 Quebrar a aba atual em partials menores e reutilizáveis.
- [x] 2.2 Criar o cabeçalho com contadores e resumo da lista de magias.
- [x] 2.3 Criar barra de busca e filtros por nível.
- [x] 2.4 Criar linha/card de spell com badges, metadados e separação visual por estado.
- [x] 2.5 Introduzir estados vazios e mensagens específicas quando o personagem não tiver magia ou não houver preparo.

## 3. Interação e estado local
- [x] 3.1 Atualizar o JS para filtrar por nome e nível sem depender de uma única classe.
- [x] 3.2 Persistir em `localStorage` o estado operacional da aba.
- [x] 3.3 Carregar o estado salvo ao abrir a ficha e aplicar a separação visual correta.
- [x] 3.4 Manter ações de preparo/despreparo somente quando o perfil permitir.
- [x] 3.5 Preservar o comportamento progressivo quando não houver bridge Dice+.

## 4. Scripts e importadores
- [x] 4.1 Atualizar `create_character.py` e `edit_character.py` para gerar a lista persistida de magias.
- [x] 4.2 Ajustar `import_dndbeyond.py` para distinguir magias preparadas, conhecidas, sempre-preparadas e por origem.
- [x] 4.3 Revisar `dnd_utils.py` para classificar magias e perfis de conjuração com dados do 5e.tools.
- [x] 4.4 Atualizar `archetypes/character.md` e documentação de dados para o novo contrato.

## 5. Validação
- [x] 5.1 Criar testes para personagem preparado, conhecido, pact magic e híbrido.
- [x] 5.2 Validar a renderização com personagem sem magia.
- [x] 5.3 Validar que a aba continua funcional com dados legados.
- [x] 5.4 Validar build Hugo e regressão visual da aba.

## 6. Encerramento
- [x] 6.1 Revisar a spec/ossatura criada e registrar decisões finais.
- [x] 6.2 Se necessário, dividir a implementação em fase de dados, fase de UI e fase de persistência local.
