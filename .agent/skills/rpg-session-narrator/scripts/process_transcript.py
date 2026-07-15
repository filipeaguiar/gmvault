#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import yaml
from pathlib import Path

def load_memory(memory_path):
    if not os.path.exists(memory_path):
        return None
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Erro ao carregar a memória: {e}", file=sys.stderr)
        return None

def save_memory(memory, memory_path):
    try:
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        with open(memory_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(memory, f, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar a memória: {e}", file=sys.stderr)
        return False

def clean_transcript(text):
    # Remove avisos comuns do Google Meet e ruídos de conexão
    lines = text.split('\n')
    cleaned_lines = []
    
    noise_patterns = [
        r"entrou na chamada",
        r"saiu da chamada",
        r"gravação foi iniciada",
        r"gravação foi encerrada",
        r"Você está gravando",
        r"Google Meet System",
        r"Som de teste",
        r"Alô, som, testando",
        r"Estão me ouvindo"
    ]
    
    compiled_noises = [re.compile(p, re.IGNORECASE) for p in noise_patterns]
    
    for line in lines:
        is_noise = False
        for pattern in compiled_noises:
            if pattern.search(line.strip()):
                is_noise = True
                break
        if not is_noise:
            cleaned_lines.append(line)
            
    return '\n'.join(cleaned_lines)

def parse_turns(text):
    # Detecta falantes no formato "[HH:MM] Nome: Fala" ou "Nome: Fala" ou "Nome [HH:MM]: Fala"
    lines = text.split('\n')
    turns = []
    current_speaker = None
    current_timestamp = None
    current_content = []
    
    # Padroes comuns de transcrição
    # Exemplo: "Filipe 10:15: Olá pessoal" ou "[10:15] Filipe: Olá pessoal" ou "Filipe: Olá pessoal"
    pattern1 = re.compile(r"^\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s+([^:]+):\s*(.*)$")
    pattern2 = re.compile(r"^([^:]+?)\s+\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?:\s*(.*)$")
    pattern3 = re.compile(r"^([^:]+):\s*(.*)$")
    
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
            
        m1 = pattern1.match(line_strip)
        m2 = pattern2.match(line_strip)
        m3 = pattern3.match(line_strip)
        
        if m1:
            if current_speaker:
                turns.append({
                    "speaker": current_speaker,
                    "timestamp": current_timestamp,
                    "content": "\n".join(current_content).strip()
                })
            current_timestamp = m1.group(1)
            current_speaker = m1.group(2).strip()
            current_content = [m1.group(3)]
        elif m2:
            if current_speaker:
                turns.append({
                    "speaker": current_speaker,
                    "timestamp": current_timestamp,
                    "content": "\n".join(current_content).strip()
                })
            current_speaker = m2.group(1).strip()
            current_timestamp = m2.group(2).strip()
            current_content = [m2.group(3)]
        elif m3:
            # Evita casar coisas que parecem URLs
            if not m3.group(1).startswith("http") and len(m3.group(1)) < 50:
                if current_speaker:
                    turns.append({
                        "speaker": current_speaker,
                        "timestamp": current_timestamp,
                        "content": "\n".join(current_content).strip()
                    })
                current_speaker = m3.group(1).strip()
                current_timestamp = None
                current_content = [m3.group(2)]
            else:
                if current_speaker:
                    current_content.append(line)
        else:
            if current_speaker:
                current_content.append(line)
            else:
                # Linha inicial sem falante conhecido
                pass
                
    if current_speaker:
        turns.append({
            "speaker": current_speaker,
            "timestamp": current_timestamp,
            "content": "\n".join(current_content).strip()
        })
        
    return turns

def normalize_text_lexicon(text, memory):
    # Substitui aliases e erros comuns por termos canônicos
    normalized = text
    
    # Agrupa todos os mapeamentos
    replacements = []
    
    # NPCs
    for npc in memory.get("npcs", []):
        canonical = npc.get("canonical_name", "")
        aliases = npc.get("aliases", []) or []
        errors = npc.get("common_transcription_errors", []) or []
        for term in list(aliases) + list(errors):
            if term:
                replacements.append((term, canonical))
                
    # Locais
    for loc in memory.get("locations", []):
        canonical = loc.get("canonical_name", "")
        aliases = loc.get("aliases", []) or []
        errors = loc.get("common_transcription_errors", []) or []
        for term in list(aliases) + list(errors):
            if term:
                replacements.append((term, canonical))
                
    # Termos gerais
    for term_item in memory.get("terms", []):
        canonical = term_item.get("canonical_form", "")
        variants = term_item.get("variants", []) or []
        for term in list(variants):
            if term:
                replacements.append((term, canonical))
                
    # Jogadores e Personagens
    for player in memory.get("players", []):
        p_name = player.get("player_name", "")
        char_name = player.get("character_name", "")
        p_aliases = player.get("transcript_names", []) or []
        char_aliases = player.get("character_aliases", []) or []
        
        # Mapeia nomes do jogador e aliases para o nome do jogador
        for pa in list(p_aliases):
            if pa:
                replacements.append((pa, p_name))
        # Mapeia aliases do personagem para o personagem canonical
        for ca in list(char_aliases):
            if ca:
                replacements.append((ca, char_name))

    # Ordena substituições pelo tamanho do termo de forma decrescente
    # para evitar substituir substrings incorretamente antes de strings maiores
    replacements.sort(key=lambda x: len(x[0]), reverse=True)
    
    # Aplica as substituições respeitando bordas de palavra para termos comuns
    for orig, dest in replacements:
        # Se for um erro comum composto ou palavra que exija bordas
        # Usamos regex de borda de palavra \b
        # Para lidar com português e caracteres acentuados, fazemos uma regex adaptada
        escaped_orig = re.escape(orig)
        # Se contiver apenas caracteres alfanuméricos e acentuados, exige bordas
        if re.match(r'^[\w\sáéíóúâêôãõçÀÉÍÓÚÂÊÔÃÕÇ]+$', orig):
            # Regex que aceita bordas de palavras em português
            pattern = re.compile(r'(?<!\w)' + escaped_orig + r'(?!\w)', re.IGNORECASE)
        else:
            pattern = re.compile(escaped_orig, re.IGNORECASE)
            
        normalized = pattern.sub(dest, normalized)
        
    return normalized

def resolve_shared_microphone(turns, memory, session_shared_config):
    # Se não houver configuração de microfone compartilhado na sessão, pula
    if not session_shared_config or not session_shared_config.get("possible_speakers"):
        return turns, []
        
    label = session_shared_config.get("transcript_label", "")
    possible_speakers = session_shared_config.get("possible_speakers", [])
    
    # Mapeia os possíveis falantes
    gm_name = None
    players = []
    
    for ps in possible_speakers:
        if ps.get("type") == "game_master":
            gm_name = ps.get("name")
        elif ps.get("type") == "player":
            players.append(ps)
            
    resolved_turns = []
    uncertainties = []
    
    for idx, turn in enumerate(turns):
        speaker = turn["speaker"]
        content = turn["content"]
        timestamp = turn["timestamp"]
        
        if speaker.lower() == label.lower():
            # Heurísticas de atribuição
            assigned_speaker = None
            confidence = "low"
            reason = ""
            
            # 1. Verifica se a fala anterior é o GM perguntando especificamente para um jogador presencial
            # Ex: "Mestre: Maria, o que o Brom faz?" -> próxima fala é o mestre de novo: "Eu vou atacar" -> Provavelmente é Maria/Brom
            if idx > 0:
                prev_turn = turns[idx - 1]
                prev_content = prev_turn["content"]
                
                # Se a fala anterior já foi resolvida ou veio de outro jogador, ou se foi o mestre
                for p in players:
                    p_name = p.get("name", "")
                    c_name = p.get("character", "")
                    # Busca pelo nome do jogador ou do personagem na pergunta anterior
                    if re.search(r'\b' + re.escape(p_name) + r'\b', prev_content, re.IGNORECASE) or \
                       re.search(r'\b' + re.escape(c_name) + r'\b', prev_content, re.IGNORECASE):
                        # E se a fala atual contiver verbos de ação ou primeira pessoa
                        if re.search(r'\b(vou|faço|uso|ataco|tento|pego|olho|rodo|quero)\b', content, re.IGNORECASE):
                            assigned_speaker = f"{p_name} (como {c_name})"
                            confidence = "medium"
                            reason = f"Fala anterior faz referência a {p_name}/{c_name} e esta possui verbos em primeira pessoa."
                            break
                            
            # 2. Verifica se a fala cita o próprio personagem do jogador em primeira pessoa
            # Ex: "Eu como Brom vou abrir a porta"
            if not assigned_speaker:
                for p in players:
                    c_name = p.get("character", "")
                    p_name = p.get("name", "")
                    if re.search(r'\bcomo\s+' + re.escape(c_name) + r'\b', content, re.IGNORECASE) or \
                       re.search(r'\bmeu\s+personagem\s+' + re.escape(c_name) + r'\b', content, re.IGNORECASE):
                        assigned_speaker = f"{p_name} (como {c_name})"
                        confidence = "high"
                        reason = f"Citação direta ao personagem {c_name} em primeira pessoa."
                        break
            
            # 3. Identifica declarações de rolagens de dados ou mecânicas específicas de um personagem
            # ou referências a aliases do personagem/jogador em primeira pessoa
            if not assigned_speaker:
                for p in players:
                    c_name = p.get("character", "")
                    p_name = p.get("name", "")
                    # Busca aliases reais na memória geral
                    aliases = [c_name, p_name]
                    for m_player in memory.get("players", []):
                        if m_player.get("player_name").lower() == p_name.lower():
                            aliases.extend(m_player.get("transcript_names", []) or [])
                            aliases.extend(m_player.get("character_aliases", []) or [])
                            break
                    # Remove duplicados e vazios
                    aliases = list(set([a for a in aliases if a]))
                    
                    # Se contiver verbos em primeira pessoa ou mecânicas
                    has_first_person = re.search(r'\b(vou|meu|minha|faço|ataco|usei|tento|pego|olho|rodo|tirei|ferramentas)\b', content, re.IGNORECASE)
                    if has_first_person:
                        # E se contiver algum alias
                        for alias in aliases:
                            if re.search(r'\b' + re.escape(alias) + r'\b', content, re.IGNORECASE):
                                assigned_speaker = f"{p_name} (como {c_name})"
                                confidence = "medium"
                                reason = f"Fala em primeira pessoa associada ao alias '{alias}' de {p_name}."
                                break
                    if assigned_speaker:
                        break
            
            # 3.1 Continuidade de rolagem de dados
            if not assigned_speaker:
                is_dice_roll = re.search(r'\b(tirei|rolei|deu|rolagem|resultado)\s+(\d{1,2})\b', content, re.IGNORECASE)
                if is_dice_roll:
                    # Busca o último jogador presencial ativo nos turnos anteriores
                    for prev_turn in reversed(resolved_turns):
                        prev_sp = prev_turn["speaker"]
                        if "(" in prev_sp and "como" in prev_sp:
                            assigned_speaker = prev_sp
                            confidence = "medium"
                            reason = "Continuidade de rolagem de dados associada ao último jogador ativo."
                            break
            
            # 4. Caso o mestre esteja narrando (falas tipicamente narrativas, descrições de cenários, falas de NPCs)
            # Geralmente usa terceira pessoa, descreve o ambiente, ou usa verbos de fala "o guarda diz"
            # Se não bateu nas anteriores e tem cara de descrição do mestre:
            if not assigned_speaker:
                # Ex: "Vocês chegam na praça", "O monstro avança", "Yana fala: ..."
                if re.search(r'\b(vocês|chegam|vêem|olham|encontram|diz|fala|pergunta|rola|iniciativa)\b', content, re.IGNORECASE) or \
                   not re.search(r'\b(vou|meu|minha|faço|ataco|usei|tirei|rolei|tento|pego|vamos|nós|nossos|iremos|olhamos|fizemos|decidimos|tentamos)\b', content, re.IGNORECASE):
                    assigned_speaker = gm_name or "Mestre"
                    confidence = "medium"
                    reason = "Padrão de descrição narrativa ou segunda/terceira pessoa."
                    
            if not assigned_speaker:
                # Permanece como incerteza
                assigned_speaker = label
                confidence = "uncertain"
                reason = "Impossível diferenciar mestre de jogadores presenciais automaticamente."
                uncertainties.append({
                    "turn_index": idx,
                    "timestamp": timestamp,
                    "content": content,
                    "probable_speaker": gm_name or "Mestre",
                    "options": [gm_name or "Mestre"] + [f"{p.get('name')} ({p.get('character')})" for p in players]
                })
                
            resolved_turns.append({
                "speaker": assigned_speaker,
                "timestamp": timestamp,
                "content": content,
                "confidence": confidence,
                "reason": reason
            })
        else:
            resolved_turns.append({
                "speaker": speaker,
                "timestamp": timestamp,
                "content": content,
                "confidence": "high",
                "reason": "Falante remoto com label único na transcrição."
            })
            
    return resolved_turns, uncertainties

def segment_into_scenes(turns, max_lines_per_scene=150):
    # Divide os turnos em cenas com base em menções a novas localidades, timestamps espaçados ou pausas
    scenes = []
    current_scene_turns = []
    scene_count = 1
    
    # Palavras-chave de transição
    scene_transition_patterns = [
        r"\b(vamos\s+para\s+o|chegamos\s+em|indo\s+para|dentro\s+de|na\s+taverna|no\s+mercado|transição|nova\s+cena)\b",
        r"\b(corta\s+para|enquanto\s+isso|horas\s+depois|no\s+dia\s+seguinte)\b"
    ]
    compiled_transitions = [re.compile(p, re.IGNORECASE) for p in scene_transition_patterns]
    
    for turn in turns:
        content = turn["content"]
        is_transition = False
        
        # Se a cena atual já tem um tamanho razoável, permitimos quebrar em transições
        if len(current_scene_turns) >= 30:
            for pattern in compiled_transitions:
                if pattern.search(content):
                    is_transition = True
                    break
                    
        # Se ultrapassar muito o tamanho máximo, força quebra
        if len(current_scene_turns) >= max_lines_per_scene:
            is_transition = True
            
        if is_transition and current_scene_turns:
            scenes.append({
                "scene_id": scene_count,
                "turns": current_scene_turns
            })
            scene_count += 1
            current_scene_turns = []
            
        current_scene_turns.append(turn)
        
    if current_scene_turns:
        scenes.append({
            "scene_id": scene_count,
            "turns": current_scene_turns
        })
        
    return scenes

def extract_structured_scene_data(scene_id, scene_turns, memory):
    # Analisa os turnos de fala da cena e extrai participantes, eventos, rolagens de dados
    participants = set()
    events = []
    dice_results = []
    location = "Desconhecido"
    
    # Mapeamentos de personagens e NPCs para detecção
    char_names = [p.get("character_name") for p in memory.get("players", []) if p.get("character_name")]
    npc_names = [n.get("canonical_name") for n in memory.get("npcs", []) if n.get("canonical_name")]
    loc_names = [l.get("canonical_name") for l in memory.get("locations", []) if l.get("canonical_name")]
    
    # Tenta inferir localização
    for turn in scene_turns:
        content = turn["content"]
        for loc in loc_names:
            if re.search(r'\b' + re.escape(loc) + r'\b', content, re.IGNORECASE):
                location = loc
                break
                
    # Extrai dados e eventos
    order = 1
    for turn in scene_turns:
        speaker = turn["speaker"]
        content = turn["content"]
        
        # Adiciona falante aos participantes
        # Se for no formato "Nome (como Char)", extrai o personagem
        match_char = re.match(r"^(.+?)\s+\(como\s+(.+?)\)$", speaker)
        if match_char:
            participants.add(match_char.group(2))
        else:
            participants.add(speaker)
            
        # Detecta dados
        # Ex: "18 de Furtividade", "tirei 17 no ataque", "dado deu 12"
        dice_pattern = re.compile(r"\b(?:tirei|deu|rolou|resultado|dado|teste|rolagem)\s+(\d{1,2})\b", re.IGNORECASE)
        dice_matches = dice_pattern.findall(content)
        for val in dice_matches:
            # Tenta achar o tipo do teste
            check_type = "Geral"
            check_words = ["percepção", "furtividade", "atletismo", "história", "arcanismo", "investigação", "medicina", "natureza", "religião", "intuição", "sobrevivência", "ataque", "dano", "iniciativa"]
            for cw in check_words:
                if re.search(r'\b' + cw + r'\b', content, re.IGNORECASE):
                    check_type = cw.capitalize()
                    break
            
            actor = match_char.group(2) if match_char else speaker
            dice_results.append({
                "actor": actor,
                "check": check_type,
                "result": int(val)
            })
            
        # Classifica eventos importantes
        # Se contiver ações verbais marcantes
        event_type = "dialogue"
        if re.search(r'\b(ataco|golpeio|lanço|uso|corro|abro|escondo|procuro|investigo)\b', content, re.IGNORECASE):
            event_type = "action"
            
        actor = match_char.group(2) if match_char else speaker
        events.append({
            "order": order,
            "type": event_type,
            "actor": actor,
            "content": content[:200] + ("..." if len(content) > 200 else "")
        })
        order += 1
        
    return {
        "scene_id": scene_id,
        "location": location,
        "participants": sorted(list(participants)),
        "events": events,
        "dice_results": dice_results
    }

def interactive_setup(memory_path):
    print("=== Configuração Inicial do RPG Session Narrator ===")
    
    memory = load_memory(memory_path) or {
        "version": 1,
        "user": {"name": "", "role": "game_master", "transcript_names": [], "notes": ""},
        "campaign": {"name": "", "system": "", "root_directory": "", "sessions_directory": "", "narrative_style": "", "default_tense": "past", "default_point_of_view": "third_person"},
        "players": [],
        "npcs": [],
        "locations": [],
        "terms": [],
        "output": {"filename_pattern": "{date}-{session_number}-{slug}.md", "overwrite_existing": False}
    }
    
    # 1. Dados do Usuário
    u_name = input(f"1. Qual é o nome do usuário/mestre? [{memory['user']['name']}]: ").strip()
    if u_name: memory['user']['name'] = u_name
    
    u_trans = input(f"2. Nome que aparece na transcrição para o usuário? (separado por vírgula) [{','.join(memory['user']['transcript_names'])}]: ").strip()
    if u_trans:
        memory['user']['transcript_names'] = [n.strip() for n in u_trans.split(',') if n.strip()]
        
    u_role = input("3. O usuário é o mestre da sessão? (s/n) [s]: ").strip().lower()
    memory['user']['role'] = "game_master" if u_role != 'n' else "player"
    
    # 2. Dados da Campanha
    c_name = input(f"4. Qual é o nome da campanha? [{memory['campaign']['name']}]: ").strip()
    if c_name: memory['campaign']['name'] = c_name
    
    c_sys = input(f"5. Qual é o sistema de RPG utilizado? [{memory['campaign']['system']}]: ").strip()
    if c_sys: memory['campaign']['system'] = c_sys
    
    c_root = input(f"6. Qual é o diretório raiz da campanha? [{memory['campaign']['root_directory']}]: ").strip()
    if c_root: memory['campaign']['root_directory'] = c_root
    
    c_sess = input(f"7. Em qual pasta devem ser salvas as narrativas das sessões? [{memory['campaign']['sessions_directory']}]: ").strip()
    if c_sess: memory['campaign']['sessions_directory'] = c_sess
    
    c_style = input(f"8. Qual estilo de narrativa prefere? (Ex: fantasia épica, dark fantasy) [{memory['campaign']['narrative_style']}]: ").strip()
    if c_style: memory['campaign']['narrative_style'] = c_style
    
    c_pov = input("9. Primeira ou Terceira pessoa? (first/third) [third]: ").strip().lower()
    memory['campaign']['default_point_of_view'] = "first_person" if c_pov == "first" else "third_person"
    
    c_tense = input("10. Passado ou Presente? (past/present) [past]: ").strip().lower()
    memory['campaign']['default_tense'] = "present" if c_tense == "present" else "past"
    
    # 3. Adicionar Jogadores (Loop Simples)
    print("\n--- Jogadores ---")
    add_p = input("Deseja cadastrar jogadores agora? (s/n) [n]: ").strip().lower()
    if add_p == 's':
        while True:
            p_name = input("Nome do jogador (ou vazio para encerrar): ").strip()
            if not p_name:
                break
            char_name = input(f"Nome do personagem de {p_name}: ").strip()
            p_aliases = input(f"Aliases de transcrição de {p_name} (separado por vírgulas): ").strip()
            char_aliases = input(f"Variantes/aliases do personagem {char_name}: ").strip()
            pronouns = input("Pronomes (ele/ela/eles): ").strip()
            usually_remote = input("Costuma jogar remoto? (s/n) [s]: ").strip().lower() != 'n'
            
            memory['players'].append({
                "player_name": p_name,
                "transcript_names": [n.strip() for n in p_aliases.split(',') if n.strip()],
                "character_name": char_name,
                "character_aliases": [n.strip() for n in char_aliases.split(',') if n.strip()],
                "pronouns": pronouns,
                "usually_remote": usually_remote,
                "notes": ""
            })
            
    # 4. Adicionar NPCs (Loop Simples)
    print("\n--- NPCs ---")
    add_n = input("Deseja cadastrar NPCs agora? (s/n) [n]: ").strip().lower()
    if add_n == 's':
        while True:
            npc_name = input("Nome canônico do NPC (ou vazio para encerrar): ").strip()
            if not npc_name:
                break
            npc_aliases = input(f"Aliases/Variantes de {npc_name}: ").strip()
            npc_errors = input(f"Erros de transcrição comuns de {npc_name}: ").strip()
            desc = input("Breve descrição do NPC: ").strip()
            
            memory['npcs'].append({
                "canonical_name": npc_name,
                "aliases": [n.strip() for n in npc_aliases.split(',') if n.strip()],
                "common_transcription_errors": [n.strip() for n in npc_errors.split(',') if n.strip()],
                "description": desc,
                "role": "npc",
                "notes": ""
            })
            
    # 5. Adicionar Termos
    print("\n--- Termos de fantasia ou locais ---")
    add_t = input("Deseja cadastrar termos de fantasia/locais agora? (s/n) [n]: ").strip().lower()
    if add_t == 's':
        while True:
            term = input("Termo canônico (ou vazio para encerrar): ").strip()
            if not term:
                break
            variants = input(f"Variantes/erros comuns de transcrição do termo '{term}': ").strip()
            cat = input("Categoria (local, facção, item): ").strip()
            
            memory['terms'].append({
                "canonical_form": term,
                "variants": [v.strip() for v in variants.split(',') if v.strip()],
                "category": cat,
                "notes": ""
            })

    save_memory(memory, memory_path)
    print(f"\nConfiguração salva com sucesso em {memory_path}!")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Script auxiliar do RPG Session Narrator")
    parser.add_argument("--memory", default=".agent/skills/rpg-session-narrator/memory.yaml", help="Caminho do arquivo memory.yaml")
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # setup
    subparsers.add_parser("setup", help="Roda a configuração interativa")
    
    # review
    subparsers.add_parser("review", help="Mostra a memória atualizada")
    
    # process
    process_p = subparsers.add_parser("process", help="Processa uma transcrição")
    process_p.add_argument("--transcript", required=True, help="Caminho da transcrição (.txt, .md)")
    process_p.add_argument("--session-config", required=True, help="Caminho do JSON contendo os parâmetros específicos da sessão")
    process_p.add_argument("--output-json", required=True, help="Caminho do JSON intermediário a ser gerado")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        interactive_setup(args.memory)
        return
        
    elif args.command == "review":
        memory = load_memory(args.memory)
        if not memory:
            print("Memória vazia ou inexistente. Execute o setup.")
        else:
            print(yaml.dump(memory, allow_unicode=True, default_flow_style=False))
        return
        
    elif args.command == "process":
        memory = load_memory(args.memory)
        if not memory:
            print(f"Erro: Arquivo de memória {args.memory} não encontrado. Roda o comando setup.", file=sys.stderr)
            sys.exit(1)
            
        if not os.path.exists(args.transcript):
            print(f"Erro: Transcrição {args.transcript} não encontrada.", file=sys.stderr)
            sys.exit(1)
            
        if not os.path.exists(args.session_config):
            print(f"Erro: Configurações da sessão {args.session_config} não encontradas.", file=sys.stderr)
            sys.exit(1)
            
        with open(args.session_config, 'r', encoding='utf-8') as f:
            session_config = json.load(f)
            
        # 1. Carrega e limpa a transcrição
        with open(args.transcript, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
        cleaned_text = clean_transcript(raw_text)
        
        # 2. Faz parse das falas (turnos)
        turns = parse_turns(cleaned_text)
        
        # 3. Normaliza nomes próprios e termos com base na memória
        for t in turns:
            t["content"] = normalize_text_lexicon(t["content"], memory)
            
        # 4. Resolve microfone compartilhado do GM
        shared_mic_config = session_config.get("shared_microphone", {})
        resolved_turns, uncertainties = resolve_shared_microphone(turns, memory, shared_mic_config)
        
        # 5. Segmenta em cenas
        scenes = segment_into_scenes(resolved_turns)
        
        # 6. Extrai metadados estruturados de cada cena
        structured_scenes = []
        for scene in scenes:
            s_data = extract_structured_scene_data(scene["scene_id"], scene["turns"], memory)
            # Adiciona os turnos reais normalizados à cena para a IA poder ler e narrar
            s_data["turns"] = scene["turns"]
            structured_scenes.append(s_data)
            
        # 7. Salva a representação intermediária em JSON
        intermediate_data = {
            "session_metadata": session_config,
            "scenes": structured_scenes,
            "uncertainties": uncertainties
        }
        
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(intermediate_data, f, ensure_ascii=False, indent=2)
            
        print(f"Sucesso: Dados intermediários salvos em {args.output_json}")
        print(f"Cenas identificadas: {len(structured_scenes)}")
        print(f"Ambigüidades detectadas: {len(uncertainties)}")
        return
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
