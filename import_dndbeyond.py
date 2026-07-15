#!/usr/bin/env python3
import urllib.request
import json
import os
import sys
import argparse
import yaml

from dnd_utils import (
    slugify,
    get_modifier,
    dump_yaml_indented,
    DATA_BASE_URL,
    clean_5etools_tags,
    parse_entries,
    fetch_from_5etools,
    fetch_class_json,
    publish_compendium_page,
    ensure_compendium_class_overview,
    STANDARD_ACTION_REFS,
)


def main():
    parser = argparse.ArgumentParser(description="Importa um personagem do D&D Beyond para a wiki estática Hugo.")
    parser.add_argument("char_id", type=str, nargs="?", help="O ID do personagem do D&D Beyond (ex: 168106464)")
    parser.add_argument("--campaign", type=str, default="cidadela-radiante", help="O slug da campanha de destino (padrão: cidadela-radiante)")
    parser.add_argument("--interactive", "--menu", action="store_true", help="Abre o menu interativo Rich.")
    
    args = parser.parse_args()

    if args.interactive:
        from interactive_cli import dndbeyond_menu

        values = dndbeyond_menu()
        if values is None:
            print("Operação cancelada.")
            return
        args.char_id = values["char_id"]
        args.campaign = values["campaign"]
    elif not args.char_id:
        parser.error("o argumento char_id é obrigatório, exceto com --interactive/--menu")
    
    url = f"https://character-service.dndbeyond.com/character/v5/character/{args.char_id}"
    print(f"Buscando dados da API do D&D Beyond para o personagem ID: {args.char_id}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            payload = json.loads(response.read().decode())
            
        char = payload.get("data")
        if not char:
            print("ERRO: Resposta inválida da API ou personagem não encontrado/privado.", file=sys.stderr)
            sys.exit(1)
            
        char_name = char.get("name")
        print(f"Personagem encontrado: {char_name}!")
        
        # 1. Atributos Base e cálculo final com modificadores
        stats_base = {s['id']: s['value'] for s in char.get('stats', [])}
        stat_names = {1: 'str', 2: 'dex', 3: 'con', 4: 'int', 5: 'wis', 6: 'cha'}
        stats_final = {stat_names[i]: stats_base[i] for i in stat_names}
        
        modifiers = char.get('modifiers', {})
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus':
                    subtype = item.get('subType', '')
                    val = item.get('value')
                    if val is not None:
                        for stat_id, sname in stat_names.items():
                            if sname in subtype:
                                stats_final[sname] += int(val)
                                
        # Modificadores finais calculados
        dex_mod = get_modifier(stats_final['dex'])
        wis_mod = get_modifier(stats_final['wis'])
        con_mod = get_modifier(stats_final['con'])
        
        # 2. Classes e Nível Total
        classes_list = []
        total_level = 0
        is_monk = False
        is_barbarian = False
        primary_class_slug = ""
        primary_class_name = ""
        
        for cls in char.get('classes', []):
            cls_def = cls.get('definition', {})
            cls_name = cls_def.get('name')
            cls_level = cls.get('level', 1)
            total_level += cls_level
            subcls_def = cls.get('subclassDefinition')
            if subcls_def:
                subcls_name = subcls_def.get('name')
                classes_list.append(f"{cls_name} {cls_level} ({subcls_name})")
            else:
                classes_list.append(f"{cls_name} {cls_level}")
            
            if cls_name == "Monk":
                is_monk = True
            elif cls_name == "Barbarian":
                is_barbarian = True
                
            if cls.get('isStartingClass'):
                primary_class_slug = slugify(cls_name)
                primary_class_name = cls_name
                
        class_str = " / ".join(classes_list)
        if not primary_class_slug and classes_list:
            primary_class_name = char.get('classes')[0].get('definition', {}).get('name')
            primary_class_slug = slugify(primary_class_name)
            
        # 3. Raça e Sub-raça
        race_data = char.get('race', {})
        race_fullname = race_data.get('fullName', "Desconhecida")
        race_basename = race_data.get('baseName', race_fullname)
        race_slug = slugify(race_basename)
        
        # Tamanho e Alinhamento
        SIZE_MAP = {
            1: "Tiny",
            2: "Tiny",
            3: "Small",
            4: "Medium",
            5: "Large",
            6: "Huge",
            7: "Gargantuan"
        }
        ALIGNMENT_MAP = {
            1: "Lawful Good",
            2: "Neutral Good",
            3: "Chaotic Good",
            4: "Lawful Neutral",
            5: "True Neutral",
            6: "Chaotic Neutral",
            7: "Lawful Evil",
            8: "Neutral Evil",
            9: "Chaotic Evil"
        }

        alignment_val = char.get('alignmentId')
        char_alignment = ALIGNMENT_MAP.get(alignment_val, "Neutral")

        size_val = race_data.get('sizeId') or char.get('sizeId')
        char_size = SIZE_MAP.get(size_val, "Medium")

        # Velocidades de movimento
        race_speeds = race_data.get('weightSpeeds', {}).get('normal', {})
        char_speeds = {
            "walk": race_speeds.get('walk', 30),
            "fly": race_speeds.get('fly', 0),
            "swim": race_speeds.get('swim', 0),
            "climb": race_speeds.get('climb', 0),
            "burrow": race_speeds.get('burrow', 0)
        }

        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus':
                    subtype = item.get('subType', '')
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        val = int(val)
                        if subtype == 'unarmored-movement' or subtype == 'speed' or subtype == 'speed-walk' or 'walk-speed' in subtype:
                            char_speeds['walk'] += val
                        elif 'fly-speed' in subtype or subtype == 'speed-fly':
                            char_speeds['fly'] += val
                        elif 'swim-speed' in subtype or subtype == 'speed-swim':
                            char_speeds['swim'] += val
                        elif 'climb-speed' in subtype or subtype == 'speed-climb':
                            char_speeds['climb'] += val
                        elif 'burrow-speed' in subtype or subtype == 'speed-burrow':
                            char_speeds['burrow'] += val

        custom_speeds = char.get('customSpeeds', [])
        if custom_speeds:
            speed_map = {1: "walk", 2: "fly", 3: "swim", 4: "climb", 5: "burrow"}
            for cs in custom_speeds:
                sid = cs.get('speedId')
                dist = cs.get('distance')
                if sid in speed_map and dist is not None:
                    char_speeds[speed_map[sid]] = int(dist)

        # Salvamentos (Saving Throws)
        prof_bonus = (total_level - 1) // 4 + 2
        stat_names_save = {
            'str': 'strength',
            'dex': 'dexterity',
            'con': 'constitution',
            'int': 'intelligence',
            'wis': 'wisdom',
            'cha': 'charisma'
        }

        char_saves = {s: get_modifier(stats_final[s]) for s in stat_names_save}
        proficient_saves = {s: False for s in stat_names_save}

        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'proficiency':
                    subtype = item.get('subType', '')
                    for s, full_name in stat_names_save.items():
                        if subtype == f"{full_name}-saving-throws":
                            proficient_saves[s] = True

        for s in char_saves:
            if proficient_saves[s]:
                char_saves[s] += prof_bonus

        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus':
                    subtype = item.get('subType', '')
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        val = int(val)
                        if subtype == 'saving-throws':
                            for s in char_saves:
                                char_saves[s] += val
                        else:
                            for s, full_name in stat_names_save.items():
                                if subtype == f"{full_name}-saving-throws":
                                    char_saves[s] += val

        saves_summary_list = []
        for s in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            if proficient_saves[s]:
                val = char_saves[s]
                sign = "+" if val >= 0 else ""
                saves_summary_list.append(f"{s.capitalize()} {sign}{val}")
        char_saves_summary = ", ".join(saves_summary_list)

        # Sentidos (Senses)
        darkvision = 0
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'set-base' and item.get('subType') == 'darkvision':
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        darkvision = max(darkvision, int(val))

        is_proficient_perception = False
        has_expertise_perception = False
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('subType') == 'perception':
                    if item.get('type') == 'proficiency':
                        is_proficient_perception = True
                    elif item.get('type') == 'expertise':
                        has_expertise_perception = True

        passive_perception_bonus = 0
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus' and item.get('subType') == 'passive-perception':
                    val = item.get('value') or item.get('fixedValue')
                    if val is not None:
                        passive_perception_bonus += int(val)

        passive_perception = 10 + wis_mod + passive_perception_bonus
        if has_expertise_perception:
            passive_perception += 2 * prof_bonus
        elif is_proficient_perception:
            passive_perception += prof_bonus

        senses_list = [f"Passive Perception {passive_perception}"]
        if darkvision > 0:
            senses_list.append(f"Darkvision {darkvision} ft.")
        char_senses = ", ".join(senses_list)

        # Idiomas (Languages)
        languages_list = []
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'language':
                    lang_name = item.get('friendlySubtypeName')
                    if lang_name and lang_name not in languages_list:
                        languages_list.append(lang_name)
        char_languages = ", ".join(sorted(languages_list))
        
        # 4. Cálculo do HP Máximo
        base_hp = char.get('baseHitPoints', 10)
        bonus_hp = char.get('bonusHitPoints') or 0
        final_hp = base_hp + (con_mod * total_level) + bonus_hp
        
        # 5. Cálculo da CA (Classe de Armadura)
        has_armor = False
        has_shield = False
        armor_ac = 10
        shield_ac = 0
        armor_type = None
        equipped_items_names = []
        
        for item in char.get('inventory', []):
            d = item.get('definition', {})
            if item.get('equipped'):
                equipped_items_names.append((d.get('name'), d.get('magic'), d.get('filterType')))
                
            if not item.get('equipped'):
                continue
            filter_type = d.get('filterType')
            if filter_type == 'Armor':
                ac_val = d.get('armorClass', 0)
                armor_type_id = d.get('armorTypeId', 0)
                if armor_type_id == 4: # Escudo
                    has_shield = True
                    shield_ac = ac_val
                else: # Armadura Leve, Média ou Pesada
                    has_armor = True
                    armor_ac = ac_val
                    armor_type = armor_type_id
                    
        # Algoritmo de CA
        if has_armor:
            if armor_type == 1: # Leve
                base_ac = armor_ac + dex_mod
            elif armor_type == 2: # Média
                base_ac = armor_ac + min(dex_mod, 2)
            else: # Pesada
                base_ac = armor_ac
        else:
            # Defesa Sem Armadura
            if is_monk and not has_shield:
                base_ac = 10 + dex_mod + wis_mod
            elif is_barbarian:
                base_ac = 10 + dex_mod + con_mod
            else:
                base_ac = 10 + dex_mod
                
        final_ac = base_ac + shield_ac
        
        # Bônus mágicos de CA do inventário
        for source, items in modifiers.items():
            if not items:
                continue
            for item in items:
                if item.get('type') == 'bonus' and item.get('subType') == 'armor-class':
                    val = item.get('value')
                    if val is not None:
                        final_ac += int(val)
                        
        # 6. Talentos
        feats_list = []
        for feat_item in char.get('feats', []):
            f_name = feat_item.get('definition', {}).get('name', '')
            if f_name not in ["Dark Bargain", "Character Threads", "Runestones"]:
                feats_list.append(f_name)
        feat_str = ", ".join(feats_list) if feats_list else "Nenhum"
        
        # 7. Magias Conhecidas e seus detalhes de uso
        spells_list = []
        spells_usage_map = {}
        
        def get_spell_usage_str(s):
            s_def = s.get('definition', {})
            level = s_def.get('level', 0)
            if level == 0:
                return "Truque"
                
            is_ritual = s_def.get('ritual', False)
            uses_slot = s.get('usesSpellSlot', True)
            
            # Checar limites de uso (feats / items)
            lim = s.get('limitedUse')
            if lim and isinstance(lim, dict) and lim.get('maxUses'):
                max_u = lim.get('maxUses')
                reset = lim.get('resetType')
                reset_str = "Descanso Longo" if reset == 2 else "Descanso Curto" if reset == 1 else "Dia"
                return f"{max_u}x/{reset_str}"
                
            if is_ritual:
                if uses_slot:
                    return "Slot / Ritual"
                else:
                    return "Ritual"
                    
            if uses_slot:
                return "Slot de Magia"
                
            return "Especial"

        for class_spell_obj in char.get('classSpells', []):
            if isinstance(class_spell_obj, dict):
                slist = class_spell_obj.get('spells', [])
                if slist:
                    for s in slist:
                        s_def = s.get('definition', {})
                        if s_def and s_def.get('name'):
                            name = s_def.get('name')
                            spells_list.append(name)
                            spells_usage_map[name] = get_spell_usage_str(s)
                            
        # Adicionar outras fontes de magias (race, class, feat, item, background)
        other_spells = char.get('spells', {})
        if isinstance(other_spells, dict):
            for source, slist in other_spells.items():
                if slist:
                    for s in slist:
                        s_def = s.get('definition', {})
                        if s_def and s_def.get('name'):
                            name = s_def.get('name')
                            spells_list.append(name)
                            spells_usage_map[name] = get_spell_usage_str(s)
                            
        # Remove duplicatas
        spells_list = sorted(list(set(spells_list)))
                
        # 8. Resolver Compêndio Refs
        compendium_refs = []
        
        # Entidades que precisamos garantir no Compêndio
        entities_to_check = []
        
        # Classe principal
        entities_to_check.append(("class", primary_class_name, f"/compendium/classes/{primary_class_slug}/"))
        # Espécie
        entities_to_check.append(("species", race_basename, f"/compendium/species/{race_slug}/"))
        # Subclasses
        for cls in char.get('classes', []):
            subcls_def = cls.get('subclassDefinition')
            if subcls_def:
                subcls_name = subcls_def.get('name')
                entities_to_check.append(("subclass", subcls_name, f"/compendium/classes/{slugify(subcls_name)}/"))
        # Talentos
        for feat in feats_list:
            entities_to_check.append(("feat", feat, f"/compendium/feats/{slugify(feat)}/"))
        # Itens Equipados
        item_aliases = {
            "leather": "leather armor",
            "studded leather": "studded leather armor",
            "scale mail": "scale mail armor",
            "ring mail": "ring mail armor",
            "plate": "plate armor",
            "hide": "hide armor",
            "padded": "padded armor",
            "chain mail": "chain mail armor",
            "splint": "splint armor"
        }
        inventory_entities = []
        for inventory_item in char.get('inventory', []):
            definition = inventory_item.get('definition', {}) or {}
            inventory_name = definition.get('name')
            inventory_filter = definition.get('filterType')
            if inventory_name and inventory_filter in ['Weapon', 'Armor', 'Wondrous item', 'Ring', 'Potion', 'Scroll', 'Other Gear']:
                inventory_entities.append((inventory_name, bool(definition.get('magic')), inventory_filter))

        for item_name, is_magic, filter_type in inventory_entities:
            kind = "magic_item" if is_magic else "item"
            slug_prefix = "magic-items" if is_magic else "items"
            check_name = item_aliases.get(item_name.lower(), item_name)
            entities_to_check.append((kind, item_name, f"/compendium/{slug_prefix}/{slugify(check_name)}/"))
        # Magias
        for spell_name in spells_list:
            entities_to_check.append(("spell", spell_name, f"/compendium/spells/{slugify(spell_name)}/"))
            
        # Checar se existem localmente, senão baixar do 5e.tools
        for kind, eng_name, ref in entities_to_check:
            content_path = "content" + ref.rstrip('/') + ".md"
            folder_path = "content" + ref + "_index.md"
            
            if os.path.exists(content_path) or os.path.exists(folder_path):
                compendium_refs.append(ref)
            else:
                # O item não existe localmente! Tenta buscar e criar do 5e.tools
                new_ref = fetch_from_5etools(kind, eng_name)
                if new_ref:
                    compendium_refs.append(new_ref)
                    
        # Remove duplicatas nas referências
        compendium_refs = sorted(list(set(compendium_refs)))
        
        # Preparar spells_usage para o front matter
        yaml_spells_usage = []
        for name in sorted(spells_usage_map.keys()):
            yaml_spells_usage.append({
                "name": name,
                "usage": spells_usage_map[name]
            })
            
        # Função para garantir a criação da regra no compêndio
        def ensure_compendium_rule(name, description):
            # Limpar indentações no início de cada linha que geram blocos de código em markdown
            cleaned_lines = []
            for line in description.split('\n'):
                stripped = line.strip()
                if stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('+') or stripped.startswith('o'):
                    cleaned_lines.append(stripped)
                else:
                    cleaned_lines.append(line.lstrip(' \t'))
            description = '\n'.join(cleaned_lines)
            
            slug = slugify(name)
            ref_path = f"/compendium/rules/{slug}/"
            dest_path = f"content/compendium/rules/{slug}.md"
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            if os.path.exists(dest_path):
                try:
                    with open(dest_path, "r", encoding="utf-8") as f:
                        existing = f.read()
                    existing_body = existing.split("---", 2)[-1].strip() if existing.startswith("---") else existing.strip()
                    if existing_body:
                        print(f"  [Compêndio] Preservando nota existente: {dest_path}")
                        return ref_path
                except OSError:
                    pass

            markdown = f"""---
title: "{name}"
params:
  kind: "rule"
draft: true
status: "draft"
summary: "Habilidade de classe."
---

{description}
"""
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"  [Compêndio] Habilidade de classe criada: {dest_path}")
            return ref_path

        # 10. Coletar e criar opções customizadas de classe (Pactos e Invocações) no Compêndio
        class_opts = char.get('options', {}).get('class', [])
        if isinstance(class_opts, list):
            for opt in class_opts:
                if isinstance(opt, dict):
                    opt_def = opt.get('definition', {})
                    if opt_def:
                        opt_name = opt_def.get('name')
                        opt_snippet = opt_def.get('snippet', '') or opt_def.get('description', '')
                        if opt_name and opt_snippet:
                            clean_snippet = clean_5etools_tags(opt_snippet.replace('<em>', '').replace('</em>', '').replace('<p>', '').replace('</p>', '\n').replace('<br>', '\n'))
                            ref = ensure_compendium_rule(opt_name, clean_snippet.strip())
                            compendium_refs.append(ref)
            
        # 11. Coletar e criar habilidades de classe e subclasse a partir do 5e.tools no Compêndio
        feature_blacklist = [
            "core bard traits", "core warlock traits", "core fighter traits", 
            "core rogue traits", "core barbarian traits", "core monk traits",
            "core sorcerer traits", "core wizard traits", "core cleric traits",
            "core druid traits", "core paladin traits", "core ranger traits",
            "ability score improvement", "ability score increase", "bard subclass",
            "warlock subclass", "subclass options", "bonus proficiency",
            "roguish archetype", "subclass feature", "roguish archetype feature",
            "sorcerous origin", "monastic tradition", "primal path", "bard college",
            "cleric domain", "druid circle", "martial archetype", "sacred oath",
            "ranger archetype", "arcane tradition", "subclass", "rogue subclass",
            "sorcerer subclass", "barbarian subclass", "fighter subclass",
            "monk subclass", "warlock subclass", "wizard subclass", "cleric subclass",
            "druid subclass", "paladin subclass", "ranger subclass"
        ]

        for cl in char.get('classes', []):
            cls_def = cl.get('definition', {})
            class_name = cls_def.get('name')
            class_level = cl.get('level', 1)
            subcls_def = cl.get('subclassDefinition')
            subclass_name = subcls_def.get('name') if subcls_def else None
            
            class_data = fetch_class_json(class_name)
            if not class_data:
                continue
                
            raw_features = []
            # Coletar classFeature
            for f in class_data.get('classFeature', []):
                if f.get('className', '').lower() == class_name.lower() and f.get('level', 1) <= class_level:
                    raw_features.append(f)
                    
            # Coletar subclassFeature se houver subclasse
            if subclass_name:
                for sf in class_data.get('subclassFeature', []):
                    if sf.get('className', '').lower() == class_name.lower() and sf.get('level', 1) <= class_level:
                        sf_sc_name = sf.get('subclassShortName', '')
                        if sf_sc_name.lower() == subclass_name.lower() or subclass_name.lower() in sf.get('subclassShortName', '').lower() or sf_sc_name.lower() in subclass_name.lower():
                            raw_features.append(sf)
            
            # Ordenar por prioridade de fonte (XPHB > PHB > outras) para sobrescrever com versões mais novas
            def get_source_priority(item):
                source = item.get("source", "")
                if source == "XPHB":
                    return 2
                if source == "PHB":
                    return 1
                return 0
                
            raw_features.sort(key=get_source_priority)
            
            # Filtrar duplicados pelo nome (mantendo o de maior prioridade de fonte)
            features_dict = {}
            for f in raw_features:
                name = f.get('name')
                if name:
                    features_dict[name.lower()] = f
                    
            # Criar as regras
            for name_lower, f in features_dict.items():
                name = f.get('name')
                if name.lower() in feature_blacklist:
                    continue
                    
                entries = f.get('entries', [])
                if not entries:
                    continue
                    
                description = parse_entries(entries)
                if not description or not description.strip():
                    continue
                    
                ref = ensure_compendium_rule(name, description.strip())
                compendium_refs.append(ref)

            ensure_compendium_class_overview(class_name, class_data)
            if subclass_name:
                ensure_compendium_class_overview(class_name, class_data, subclass_name)

        # Remove duplicatas nas referências
        compendium_refs = sorted(list(set(compendium_refs)))

        # === NOVOS METADADOS DA FICHA DE RPG ===
        # 1. Avatar: usar a imagem do handout local quando a API não fornecer avatar.
        avatar_url = char.get('avatarUrl') or ""
        avatar_slug = slugify(char_name)
        avatar_slug = {"perwinkle-pinky-pirata": "pinky", "nyx-": "nyxclair"}.get(avatar_slug, avatar_slug)
        avatar_aliases = {"detios-cantobaixo": "detios", "nyxclair": "nyx"}
        avatar_candidates = [avatar_slug, avatar_aliases.get(avatar_slug, "")]
        if not avatar_url:
            for candidate in avatar_candidates:
                if not candidate:
                    continue
                fallback_avatar = f"/images/campaigns/{args.campaign}/handouts/{candidate}.png"
                if os.path.exists(f"static{fallback_avatar}"):
                    avatar_url = fallback_avatar
                    break

        # 2. Moedas
        currencies = char.get('currencies', {}) or {}
        
        # 3. Habilidade de conjuração, DC de magia e Bônus de ataque
        casting_stat_id = None
        for cl in char.get('classes', []):
            cls_def = cl.get('definition', {})
            ability_id = cls_def.get('spellCastingAbilityId')
            if ability_id:
                casting_stat_id = ability_id
                break
                
        spell_dc = 0
        spell_attack_bonus = 0
        if casting_stat_id in stat_names:
            casting_stat_name = stat_names[casting_stat_id]
            stat_mod = get_modifier(stats_final[casting_stat_name])
            spell_dc = 8 + prof_bonus + stat_mod
            spell_attack_bonus = prof_bonus + stat_mod

        # 4. Cálculo e mapeamento das 18 Perícias (Skills)
        SKILL_MAP = {
            "acrobatics": "dex",
            "animal-handling": "wis",
            "arcana": "int",
            "athletics": "str",
            "deception": "cha",
            "history": "int",
            "insight": "wis",
            "intimidation": "cha",
            "investigation": "int",
            "medicine": "wis",
            "nature": "int",
            "perception": "wis",
            "performance": "cha",
            "persuasion": "cha",
            "religion": "int",
            "sleight-of-hand": "dex",
            "stealth": "dex",
            "survival": "wis"
        }
        
        skills_data = {}
        for skill_name, stat_key in SKILL_MAP.items():
            is_prof = False
            is_exp = False
            bonus = 0
            for source, items in modifiers.items():
                if not items:
                    continue
                for item in items:
                    if item.get('subType') == skill_name:
                        if item.get('type') == 'proficiency':
                            is_prof = True
                        elif item.get('type') == 'expertise':
                            is_exp = True
                        elif item.get('type') == 'bonus':
                            val = item.get('value') or item.get('fixedValue')
                            if val is not None:
                                bonus += int(val)
            stat_mod = get_modifier(stats_final[stat_key])
            total_bonus = stat_mod + bonus
            if is_exp:
                total_bonus += 2 * prof_bonus
            elif is_prof:
                total_bonus += prof_bonus
                
            skills_data[skill_name] = {
                "bonus": total_bonus,
                "proficient": is_prof or is_exp,
                "expertise": is_exp,
                "stat": stat_key
            }

        # 5. Sentidos Passivos calculados
        passive_senses = {
            "perception": 10 + skills_data["perception"]["bonus"],
            "investigation": 10 + skills_data["investigation"]["bonus"],
            "insight": 10 + skills_data["insight"]["bonus"]
        }

        # 6. Ações (Ações padrão + Ações de classe/raça/talento)
        actions_data = []
        standard_actions = [
            {"name": name, "ref": ref, "max_uses": 0, "reset": ""}
            for name, ref in STANDARD_ACTION_REFS.items()
        ]
        actions_data.extend(standard_actions)
        compendium_refs.extend(action["ref"] for action in standard_actions)
        for action in standard_actions:
            publish_compendium_page(action["ref"])

        # Adicionar ações específicas
        for source_key in ['class', 'race', 'feat']:
            actions_list = char.get('actions', {}).get(source_key, []) or []
            for act in actions_list:
                act_name = act.get('name')
                act_desc = act.get('snippet') or act.get('description', '')
                if not act_name:
                    continue
                lim = act.get('limitedUse') or {}
                max_uses = lim.get('maxUses', 0)
                reset = lim.get('resetType')
                reset_str = "Descanso Longo" if reset == 2 else "Descanso Curto" if reset == 1 else "Dia" if reset else ""
                
                clean_desc = clean_5etools_tags(act_desc.replace('<p>', '').replace('</p>', '\n').replace('<br>', '\n')).strip()
                action_ref = f"/compendium/rules/{slugify(act_name)}/"
                action_path = f"content{action_ref.rstrip('/')}.md"
                if not os.path.exists(action_path) and clean_desc:
                    action_ref = ensure_compendium_rule(act_name, clean_desc)

                action_entry = {
                    "name": act_name,
                    "max_uses": max_uses,
                    "reset": reset_str,
                    "source": source_key
                }
                if action_ref:
                    publish_compendium_page(action_ref)
                    action_entry["ref"] = action_ref
                    compendium_refs.append(action_ref)
                actions_data.append(action_entry)

        compendium_refs = sorted(list(set(compendium_refs)))

        # 7. Equipamentos detalhados (Armas, Armaduras, Consumíveis e Outros)
        equipment_list = []
        for item in char.get('inventory', []):
            d = item.get('definition', {})
            item_name = d.get('name')
            filter_type = d.get('filterType')
            is_equipped = item.get('equipped', False)
            qty = item.get('quantity', 1)
            
            atk_formula = ""
            dmg_formula = ""
            if filter_type == 'Weapon':
                is_finesse = any(p.get('name') == 'Finesse' for p in d.get('properties', []))
                stat_key = 'dex' if is_finesse and stats_final['dex'] > stats_final['str'] else 'str'
                stat_mod = get_modifier(stats_final[stat_key])
                prof = prof_bonus if is_equipped else 0
                atk_bonus = stat_mod + prof
                atk_formula = f"1d20 + {atk_bonus}"
                
                dice = d.get('damage', {}).get('diceString', '1d4')
                dmg_bonus = stat_mod
                dmg_formula = f"{dice} + {dmg_bonus}"
                
            item_ref = f"/compendium/{'magic-items' if d.get('magic') else 'items'}/{slugify(item_aliases.get((item_name or '').lower(), item_name or ''))}/"
            equipment_entry = {
                "name": item_name,
                "quantity": qty,
                "equipped": is_equipped,
                "filter_type": filter_type,
                "attack_formula": atk_formula,
                "damage_formula": dmg_formula,
            }
            item_path = f"content{item_ref.rstrip('/')}.md"
            if os.path.exists(item_path):
                equipment_entry["ref"] = item_ref
            else:
                print(f"  [Compêndio] Item sem nota local, mantendo sem ref: {item_name}")
            equipment_list.append(equipment_entry)

        # 8. Grimório Estruturado
        structured_spells = []
        for class_spell_obj in char.get('classSpells', []):
            if isinstance(class_spell_obj, dict):
                slist = class_spell_obj.get('spells', [])
                if slist:
                    for s in slist:
                        s_def = s.get('definition', {})
                        if s_def and s_def.get('name'):
                            name = s_def.get('name')
                            spell_ref = f"/compendium/spells/{slugify(name)}/"
                            spell_entry = {
                                "name": name,
                                "level": s_def.get('level', 0),
                                "prepared": s.get('prepared', False),
                                "usage": get_spell_usage_str(s)
                            }
                            if os.path.exists(f"content{spell_ref.rstrip('/')}.md"):
                                spell_entry["ref"] = spell_ref
                            structured_spells.append(spell_entry)
        other_spells = char.get('spells', {})
        if isinstance(other_spells, dict):
            for source, slist in other_spells.items():
                if slist:
                    for s in slist:
                        s_def = s.get('definition', {})
                        if s_def and s_def.get('name'):
                            name = s_def.get('name')
                            spell_ref = f"/compendium/spells/{slugify(name)}/"
                            spell_entry = {
                                "name": name,
                                "level": s_def.get('level', 0),
                                "prepared": s.get('prepared', False) or (source in ['race', 'background', 'feat']),
                                "usage": get_spell_usage_str(s)
                            }
                            if os.path.exists(f"content{spell_ref.rstrip('/')}.md"):
                                spell_entry["ref"] = spell_ref
                            structured_spells.append(spell_entry)
        structured_spells = sorted(structured_spells, key=lambda k: (k['level'], k['name']))

        # 9. Classes e Progressão por Nível
        classes_data = []
        for cl in char.get('classes', []):
            cls_def = cl.get('definition', {})
            subcls_def = cl.get('subclassDefinition') or {}
            classes_data.append({
                "name": cls_def.get('name'),
                "level": cl.get('level'),
                "subclass": subcls_def.get('name', "")
            })
            
        # 10. Montar conteúdo Markdown
        slug = slugify(char_name)
        slug_map = {
            "perwinkle-pinky-pirata": "pinky",
            "nyx-": "nyxclair"
        }
        title_map = {
            "pinky": "Pinky",
            "nyxclair": "Nyx'Clair"
        }
        if slug in slug_map:
            slug = slug_map[slug]
        
        display_title = char_name
        if slug in title_map:
            display_title = title_map[slug]
            
        file_path = f"content/campaigns/{args.campaign}/characters/{slug}.md"
        
        markdown = f"""---
title: {json.dumps(display_title)}
date: 2026-07-09T19:00:00Z
params:
  kind: "character"
draft: false
weight: 10
summary: "{race_fullname} {class_str} importado do D&D Beyond."
tags:
  - jogador
  - {race_basename.lower()}
  - {primary_class_slug}
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "{class_str}"
  level: {total_level}
  species: "{race_fullname}"
  ac: "{final_ac}"
  hp: "{final_hp}"
  hp_max: "{final_hp}"
  hp_current: "{final_hp}"
  feat: "{feat_str}"
  size: "{char_size}"
  alignment: "{char_alignment}"
  dndbeyond_id: "{args.char_id}"
  proficiency_bonus: {prof_bonus}
  spell_dc: {spell_dc}
  spell_attack_bonus: {spell_attack_bonus}
  avatar: "{avatar_url}"
  speed:
    walk: {char_speeds['walk']}
    fly: {char_speeds['fly']}
    swim: {char_speeds['swim']}
    climb: {char_speeds['climb']}
    burrow: {char_speeds['burrow']}
  senses: "{char_senses}"
  passive_senses:
    perception: {passive_senses['perception']}
    investigation: {passive_senses['investigation']}
    insight: {passive_senses['insight']}
  languages: "{char_languages}"
  saves:
    str: {char_saves['str']}
    dex: {char_saves['dex']}
    con: {char_saves['con']}
    int: {char_saves['int']}
    wis: {char_saves['wis']}
    cha: {char_saves['cha']}
  saves_proficient:
    str: {str(proficient_saves['str']).lower()}
    dex: {str(proficient_saves['dex']).lower()}
    con: {str(proficient_saves['con']).lower()}
    int: {str(proficient_saves['int']).lower()}
    wis: {str(proficient_saves['wis']).lower()}
    cha: {str(proficient_saves['cha']).lower()}
  saves_summary: "{char_saves_summary}"
  mods:
    str: {get_modifier(stats_final['str'])}
    dex: {get_modifier(stats_final['dex'])}
    con: {get_modifier(stats_final['con'])}
    int: {get_modifier(stats_final['int'])}
    wis: {get_modifier(stats_final['wis'])}
    cha: {get_modifier(stats_final['cha'])}
  stats:
    str: {stats_final['str']}
    dex: {stats_final['dex']}
    con: {stats_final['con']}
    int: {stats_final['int']}
    wis: {stats_final['wis']}
    cha: {stats_final['cha']}
  currencies:
    cp: {currencies.get('cp', 0) or 0}
    sp: {currencies.get('sp', 0) or 0}
    gp: {currencies.get('gp', 0) or 0}
    ep: {currencies.get('ep', 0) or 0}
    pp: {currencies.get('pp', 0) or 0}
  skills:{dump_yaml_indented(skills_data, 4)}
  actions:{dump_yaml_indented(actions_data, 4)}
  equipment:{dump_yaml_indented(equipment_list, 4)}
  spells:{dump_yaml_indented(structured_spells, 4)}
  classes_progression:{dump_yaml_indented(classes_data, 4)}

# Relacionamentos
locations: []
factions: []
compendium_refs:{dump_yaml_indented(compendium_refs, 0)}
spells_usage:{dump_yaml_indented(yaml_spells_usage, 0)}
---

### Biografia
Este personagem foi importado automaticamente do D&D Beyond. 

### Equipamentos e Recursos
Acesse a ficha completa original no D&D Beyond para acompanhar o inventário de itens e slots de magia em tempo real.
"""
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)
            
        print(f"SUCESSO: Ficha do personagem criada com sucesso em: {file_path}")
        
    except Exception as e:
        print(f"ERRO: Falha ao processar ou importar o personagem. Detalhes: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
