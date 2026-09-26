#!/bin/bash
REFS=(
  "/compendium/classes/barbarian/"
  "/compendium/feats/great-weapon-master/"
  "/compendium/feats/tough/"
  "/compendium/items/backpack/"
  "/compendium/items/bedroll/"
  "/compendium/items/greataxe/"
  "/compendium/items/handaxe/"
  "/compendium/items/hempen-rope-50-feet/"
  "/compendium/items/mess-kit/"
  "/compendium/items/rations-1-day/"
  "/compendium/items/tinderbox/"
  "/compendium/items/torch/"
  "/compendium/items/waterskin/"
  "/compendium/rules/action-attack/"
  "/compendium/rules/action-dash/"
  "/compendium/rules/action-disengage/"
  "/compendium/rules/action-dodge/"
  "/compendium/rules/action-help/"
  "/compendium/rules/action-hide/"
  "/compendium/rules/action-use-object/"
  "/compendium/rules/rage/"
  "/compendium/rules/unarmored-defense/"
  "/compendium/rules/weapon-mastery/"
  "/compendium/species/goliath/"
  "/compendium/rules/danger-sense/"
  "/compendium/rules/reckless-attack/"
  "/compendium/rules/primal-knowledge/"
  "/compendium/rules/primal-path/"
  "/compendium/rules/barbarian-subclass/"
  "/compendium/rules/path-of-the-berserker/"
  "/compendium/rules/frenzy/"
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
