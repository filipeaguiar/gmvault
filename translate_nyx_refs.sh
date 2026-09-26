#!/bin/bash
REFS=(
  "/compendium/classes/warlock/"
  "/compendium/classes/great-old-one-patron/"
  "/compendium/feats/magic-initiate/"
  "/compendium/items/backpack/"
  "/compendium/items/book/"
  "/compendium/items/ink-1-ounce-bottle/"
  "/compendium/items/ink-pen/"
  "/compendium/items/leather-armor/"
  "/compendium/items/parchment-one-sheet/"
  "/compendium/items/quarterstaff/"
  "/compendium/items/sickle/"
  "/compendium/rules/action-attack/"
  "/compendium/rules/action-dash/"
  "/compendium/rules/action-disengage/"
  "/compendium/rules/action-dodge/"
  "/compendium/rules/action-help/"
  "/compendium/rules/action-hide/"
  "/compendium/rules/action-use-object/"
  "/compendium/rules/agonizing-blast/"
  "/compendium/rules/repelling-blast/"
  "/compendium/species/elf/"
  "/compendium/spells/charm-person/"
  "/compendium/spells/eldritch-blast/"
  "/compendium/spells/find-familiar/"
  "/compendium/spells/guidance/"
  "/compendium/spells/gust/"
  "/compendium/spells/mage-hand/"
  "/compendium/spells/message/"
  "/compendium/spells/misty-step/"
  "/compendium/spells/ray-of-frost/"
  "/compendium/spells/speak-with-animals/"
  "/compendium/spells/unseen-servant/"
  "/compendium/rules/eldritch-invocations/"
  "/compendium/rules/magical-cunning/"
  "/compendium/rules/warlock-subclass/"
  "/compendium/rules/awakened-mind/"
  "/compendium/rules/great-old-one-spells/"
  "/compendium/rules/pact-magic/"
  "/compendium/rules/psychic-spells/"
  "/compendium/spells/dissonant-whispers/"
  "/compendium/spells/tashas-hideous-laughter/"
  "/compendium/spells/detect-thoughts/"
  "/compendium/spells/phantasmal-force/"
)
source .venv/bin/activate
for REF in "${REFS[@]}"; do
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
