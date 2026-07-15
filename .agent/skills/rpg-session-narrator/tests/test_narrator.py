#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import json
import yaml

# Adiciona o diretório de scripts ao path para importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from process_transcript import (
    clean_transcript,
    parse_turns,
    normalize_text_lexicon,
    resolve_shared_microphone,
    segment_into_scenes,
    extract_structured_scene_data
)

class TestRPGSessionNarrator(unittest.TestCase):
    def setUp(self):
        # Memória fictícia para testes
        self.memory = {
            "version": 1,
            "user": {
                "name": "Filipe",
                "role": "game_master",
                "transcript_names": ["Filipe"],
                "notes": ""
            },
            "campaign": {
                "name": "Cidadela Radiante",
                "system": "D&D 5e",
                "root_directory": "/home/filipe/Documentos/Projetos/gmvault/content/campaigns/cidadela-radiante",
                "sessions_directory": "sessions",
                "narrative_style": "fantasia",
                "default_tense": "past",
                "default_point_of_view": "third_person"
            },
            "players": [
                {
                    "player_name": "João",
                    "transcript_names": ["Joao"],
                    "character_name": "Arannis",
                    "character_aliases": ["Aranis", "ladino"],
                    "pronouns": "ele",
                    "usually_remote": False
                },
                {
                    "player_name": "Maria",
                    "transcript_names": ["Maria"],
                    "character_name": "Brom",
                    "character_aliases": ["Brum"],
                    "pronouns": "ela",
                    "usually_remote": False
                },
                {
                    "player_name": "Carlos",
                    "transcript_names": ["Carlos"],
                    "character_name": "Elysia",
                    "character_aliases": [],
                    "pronouns": "ela",
                    "usually_remote": True
                }
            ],
            "npcs": [
                {
                    "canonical_name": "Siabsungkoh",
                    "aliases": ["Siabsunko"],
                    "common_transcription_errors": ["se abre um corpo", "se absconco"],
                    "description": "Uma cidade de feiras e comércio."
                },
                {
                    "canonical_name": "Yana",
                    "aliases": [],
                    "common_transcription_errors": ["iana", "yana"],
                    "description": "Guarda local."
                }
            ],
            "locations": [],
            "terms": [],
            "output": {
                "filename_pattern": "{date}-{session_number}-{slug}.md",
                "overwrite_existing": False
            }
        }
        
        # Configuração de sessão fictícia com participantes presenciais compartilhando o microfone do GM
        self.session_config = {
            "date": "2026-07-14",
            "session_number": 12,
            "session_title": "O Mercado Noturno",
            "players_present": ["João", "Maria", "Carlos"],
            "shared_microphone": {
                "transcript_label": "Filipe",
                "possible_speakers": [
                    {"type": "game_master", "name": "Filipe"},
                    {"type": "player", "name": "João", "character": "Arannis"},
                    {"type": "player", "name": "Maria", "character": "Brom"}
                ]
            }
        }
        
        # Transcrição fictícia cobrindo os requisitos
        # Mestre e jogador remoto com nomes próprios: Filipe e Carlos (remoto)
        # Dois presenciais (João e Maria) usando o microfone do mestre (Filipe na transcrição)
        # Contém:
        # - uma pergunta do mestre
        # - uma resposta de jogador presencial sob o nome do mestre
        # - um NPC com nome transcrito incorretamente ("se abre um corpo" em vez de Siabsungkoh)
        # - uma rolagem de dado ("tirei 17")
        # - uma discussão de regra ("o modificador é +3")
        # - uma ação bem-sucedida
        # - uma fala cuja autoria permaneça incerta
        self.raw_transcript = """
[10:00] Google Meet System: A gravação foi iniciada.
[10:01] Filipe: O que vocês fazem agora no mercado de se abre um corpo?
[10:02] Filipe: Eu vou tentar abrir a fechadura do portão com minhas ferramentas de ladino.
[10:03] Carlos: Eu dou cobertura e fico vigiando a rua.
[10:04] Filipe: Rola um teste de Prestidigitação. O modificador é +3 pelas regras.
[10:05] Filipe: Eu tirei 17 no dado, deu 20 no total.
[10:06] Filipe: Você consegue girar os pinos e o portão se abre suavemente. Ação bem sucedida.
[10:07] Filipe: Vamos ver se tem alguém lá dentro.
"""

    def test_clean_transcript(self):
        # Valida que removeu avisos automáticos
        cleaned = clean_transcript(self.raw_transcript)
        self.assertNotIn("A gravação foi iniciada", cleaned)
        self.assertIn("Filipe: O que vocês fazem", cleaned)

    def test_parse_turns(self):
        cleaned = clean_transcript(self.raw_transcript)
        turns = parse_turns(cleaned)
        
        self.assertEqual(len(turns), 7)
        self.assertEqual(turns[0]["speaker"], "Filipe")
        self.assertEqual(turns[0]["timestamp"], "10:01")
        self.assertEqual(turns[0]["content"], "O que vocês fazem agora no mercado de se abre um corpo?")
        
        self.assertEqual(turns[2]["speaker"], "Carlos")
        self.assertEqual(turns[2]["content"], "Eu dou cobertura e fico vigiando a rua.")

    def test_normalize_lexicon(self):
        text = "O que vocês fazem agora no mercado de se abre um corpo com iana?"
        normalized = normalize_text_lexicon(text, self.memory)
        # "se abre um corpo" deve virar Siabsungkoh
        self.assertIn("Siabsungkoh", normalized)
        self.assertNotIn("se abre um corpo", normalized)
        # "iana" deve virar Yana (canonical_name)
        # Peraí, "iana" está no "common_transcription_errors" de "Yana"
        # O script substitui "iana" por "Yana"
        self.assertIn("Yana", normalized)

    def test_resolve_shared_microphone(self):
        cleaned = clean_transcript(self.raw_transcript)
        turns = parse_turns(cleaned)
        
        # Aplica a normalização primeiro nas falas
        for t in turns:
            t["content"] = normalize_text_lexicon(t["content"], self.memory)
            
        resolved, uncertainties = resolve_shared_microphone(
            turns, 
            self.memory, 
            self.session_config["shared_microphone"]
        )
        
        # Turno 0: "Filipe: O que vocês fazem agora no mercado de Siabsungkoh?"
        # Deve ser atribuído ao Filipe (Mestre)
        self.assertEqual(resolved[0]["speaker"], "Filipe")
        
        # Turno 1: "Filipe: Eu vou tentar abrir a fechadura do portão com minhas ferramentas de ladino."
        # João é o ladino/Arannis. Tem verbos em primeira pessoa ("vou tentar", "minhas ferramentas").
        # Deve ser associado provisoriamente a João (como Arannis)
        self.assertIn("João", resolved[1]["speaker"])
        self.assertIn("Arannis", resolved[1]["speaker"])
        self.assertEqual(resolved[1]["confidence"], "medium")
        
        # Turno 3: "Filipe: Rola um teste de Prestidigitação. O modificador é +3 pelas regras."
        # Deve ser atribuído a Filipe (Mestre) pelas descrições de regras e comando de rolar teste
        self.assertEqual(resolved[3]["speaker"], "Filipe")
        
        # Turno 4: "Filipe: Eu tirei 17 no dado, deu 20 no total."
        # João acabou de rolar. Deve ser associado a João (Arannis)
        # (Nesse teste, a fala anterior foi o mestre mandando rolar, e agora é alguém falando que tirou 17)
        self.assertIn("João", resolved[4]["speaker"])
        
        # Turno 6: "Filipe: Vamos ver se tem alguém lá dentro."
        # Uma fala curta sem marcadores claros e sem contexto de ação direta do personagem
        # Deve constar como incerta/ambígua nas incertezas
        self.assertEqual(resolved[6]["confidence"], "uncertain")
        self.assertTrue(len(uncertainties) > 0)
        
    def test_segmenting_and_structuring(self):
        cleaned = clean_transcript(self.raw_transcript)
        turns = parse_turns(cleaned)
        
        # Normalização e resolução
        for t in turns:
            t["content"] = normalize_text_lexicon(t["content"], self.memory)
        resolved, uncertainties = resolve_shared_microphone(
            turns, 
            self.memory, 
            self.session_config["shared_microphone"]
        )
        
        scenes = segment_into_scenes(resolved, max_lines_per_scene=3)
        self.assertTrue(len(scenes) >= 2) # Dividido devido ao tamanho máximo
        
        scene_data = extract_structured_scene_data(1, scenes[0]["turns"], self.memory)
        self.assertIn("Carlos", scene_data["participants"])
        # Valida que detectou rolagens de dados se houver
        # (A rolagem está no turno 4, que pode cair na cena 2 dependendo da divisão)
        all_dice = []
        for s in scenes:
            s_data = extract_structured_scene_data(s["scene_id"], s["turns"], self.memory)
            all_dice.extend(s_data["dice_results"])
            
        self.assertTrue(any(d["result"] == 17 for d in all_dice))

if __name__ == "__main__":
    unittest.main()
