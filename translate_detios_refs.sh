#!/bin/bash
REFS=(
  "/compendium/classes/bard/"
  "/compendium/classes/college-of-whispers/"
  "/compendium/feats/inspiring-leader/"
  "/compendium/feats/lucky/"
  "/compendium/items/backpack/"
  "/compendium/items/bedroll/"
  "/compendium/items/candle/"
  "/compendium/items/costume-clothes/"
  "/compendium/items/dagger/"
  "/compendium/items/disguise-kit/"
  "/compendium/items/entertainers-pack/"
  "/compendium/items/leather-armor/"
  "/compendium/items/rations-1-day/"
  "/compendium/items/waterskin/"
  "/compendium/rules/action-attack/"
  "/compendium/rules/action-dash/"
  "/compendium/rules/action-disengage/"
  "/compendium/rules/action-dodge/"
  "/compendium/rules/action-help/"
  "/compendium/rules/action-hide/"
  "/compendium/rules/action-use-object/"
  "/compendium/rules/bardic-inspiration/"
  "/compendium/rules/bard-subclass/"
  "/compendium/rules/college-of-whispers/"
  "/compendium/rules/spellcasting/"
  "/compendium/species/halfling/"
  "/compendium/spells/charm-person/"
  "/compendium/spells/detect-magic/"
  "/compendium/spells/detect-thoughts/"
  "/compendium/spells/dissonant-whispers/"
  "/compendium/spells/healing-word/"
  "/compendium/spells/invisibility/"
  "/compendium/spells/minor-illusion/"
  "/compendium/spells/prestidigitation/"
  "/compendium/spells/suggestion/"
  "/compendium/spells/vicious-mockery/"
  "/compendium/rules/jack-of-all-trades/"
  "/compendium/rules/magical-inspiration/"
  "/compendium/rules/song-of-rest-d6/"
  "/compendium/rules/words-of-terror/"
  "/compendium/rules/expertise/"
)

source .venv/bin/activate

for REF in "${REFS[@]}"; do
  # Remove leading slash and trailing slash
  REL_PATH="${REF#/}"
  REL_PATH="${REL_PATH%/}"
  
  FILE_PATH="content/${REL_PATH}.md"
  INDEX_PATH="content/${REL_PATH}/_index.md"
  
  TARGET=""
  if [ -f "$FILE_PATH" ]; then
    TARGET="$FILE_PATH"
  elif [ -f "$INDEX_PATH" ]; then
    TARGET="$INDEX_PATH"
  fi
  
  if [ -n "$TARGET" ]; then
    echo "Translating $TARGET"
    python3 translate_drafts.py --scope compendium --path "$TARGET" --translate-frontmatter --apply
  else
    echo "Not found: $REF"
  fi
done
