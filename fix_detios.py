import re

with open("content/campaigns/journeys-through-the-radiant-citadel/characters/detios-canto-baixo.md", "r") as f:
    content = f.read()

translations = {
    "name: Bardic Inspiration": "name: Inspiração de Bardo",
    "name: Spellcasting": "name: Conjuração",
    "name: Jack of All Trades": "name: Faz-Tudo",
    "name: Magical Inspiration": "name: Inspiração Mágica",
    "name: Song of Rest (d6)": "name: Canção de Descanso (d6)",
    "name: Expertise": "name: Especialização",
    "name: Psychic Blades": "name: Lâminas Psíquicas",
    "name: Words of Terror": "name: Palavras de Terror",
    "alignment: True Neutral": "alignment: Neutro Verdadeiro"
}

for eng, pt in translations.items():
    content = content.replace(eng, pt)

with open("content/campaigns/journeys-through-the-radiant-citadel/characters/detios-canto-baixo.md", "w") as f:
    f.write(content)
print("Detios sheet translated.")
