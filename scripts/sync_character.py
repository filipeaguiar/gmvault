#!/usr/bin/env python3
"""
sync_character.py — Sincroniza a ficha de personagem com o compêndio local.

Dado um arquivo Markdown de personagem, este script:
  1. Varre spells, equipment, race, classes, feats → baixa stubs ausentes do 5e.tools
  2. Recalcula mods (modificadores de atributo) a partir de char_info.stats
  3. Atualiza compendium_refs, removendo refs stale de raça/classe e adicionando novas
  4. Preserva integralmente o corpo (biografia/prosa) sem formatação indesejada

Uso:
    python3 scripts/sync_character.py <caminho_para_ficha.md>
"""

import os
import sys
import argparse
import re
import math
import yaml

# Adiciona o diretório raiz ao path para usar o resolvedor compartilhado.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from dnd_utils import fetch_from_5etools, slugify
except ImportError as e:
    print(f"Erro ao importar resolvedor do compêndio: {e}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_modifier(score: int) -> int:
    """Calcula o modificador de atributo a partir do score (D&D 5e)."""
    return math.floor((int(score) - 10) / 2)


# Regras compartilhadas com nomes traduzidos ou variantes de importação.
ACTION_REF_ALIASES = {
    "ataque": "/compendium/rules/action-attack/",
    "esconder": "/compendium/rules/action-hide/",
    "esconder-se": "/compendium/rules/action-hide/",
    "desengajar": "/compendium/rules/action-disengage/",
    "disparar": "/compendium/rules/action-dash/",
    "disparada": "/compendium/rules/action-dash/",
    "ajudar": "/compendium/rules/action-help/",
    "esquivar": "/compendium/rules/action-dodge/",
    "usar objeto": "/compendium/rules/action-use-object/",
    "usar um objeto": "/compendium/rules/action-use-object/",
    "vex (pistol)": "/compendium/rules/vex-pistol/",
    "slow (musket)": "/compendium/rules/slow-musket/",
    "healing hands": "/compendium/rules/healing-hands/",
    "firearm specialist": "/compendium/rules/firearm-specialist/",
}


def normalize_action_name(name: str) -> str:
    return " ".join(str(name).strip().lower().split())


def local_page_for_ref(ref: str):
    """Retorna o arquivo local de uma ref do compêndio, se for seguro e existir."""
    if not isinstance(ref, str) or not ref.startswith("/compendium/"):
        return None
    relative = ref.rstrip("/").removeprefix("/compendium/")
    if not relative or "/" in relative and relative.endswith("/"):
        pass
    candidate = os.path.join("content", "compendium", f"{relative}.md")
    if os.path.isfile(candidate):
        return candidate
    index_candidate = os.path.join("content", "compendium", relative, "_index.md")
    if os.path.isfile(index_candidate):
        return index_candidate
    return None


def ref_has_content(ref: str) -> bool:
    """Verifica se uma nota local tem corpo Markdown não vazio."""
    path = local_page_for_ref(ref)
    if not path:
        return False
    try:
        _, body = parse_markdown_file(path)
    except (OSError, ValueError, yaml.YAMLError):
        return False
    return bool(body.strip())


def resolve_action_ref(name: str):
    """Resolve somente correspondências locais inequívocas; não inventa refs."""
    normalized = normalize_action_name(name)
    alias = ACTION_REF_ALIASES.get(normalized)
    if alias:
        return alias

    candidate = f"/compendium/rules/{slugify(name)}/"
    if local_page_for_ref(candidate):
        return candidate
    return None


def parse_markdown_file(file_path: str):
    """
    Lê o arquivo Markdown e divide cirurgicamente o YAML frontmatter
    do corpo de texto (biografia/prosa), preservando o corpo exatamente.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
    match = pattern.match(content)

    if not match:
        raise ValueError("O arquivo não possui um YAML frontmatter válido delimitado por '---'.")

    yaml_str = match.group(1)
    body_str = match.group(2)

    try:
        frontmatter = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Erro ao processar o YAML do frontmatter: {e}")

    return frontmatter, body_str


def save_markdown_file(file_path: str, frontmatter: dict, body_str: str):
    """
    Grava de volta o Markdown juntando o frontmatter YAML atualizado
    e o corpo original, sem danificar comentários ou biografia.
    """
    yaml_str = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{yaml_str}---\n{body_str}"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def fetch_and_collect(entity_type: str, name: str, existing_refs: set, new_refs: list,
                      stale_refs: set = None, stale_prefixes: list = None):
    """
    Baixa um stub do 5e.tools se ausente no compêndio.
    Remove refs stale (de entidades antigas) se `stale_prefixes` for fornecido.
    Retorna a ref nova se foi criada, ou None.
    """
    slug = slugify(name)
    prefix_map = {
        "spell":      ("/compendium/spells/", "content/compendium/spells/"),
        "item":       ("/compendium/items/", "content/compendium/items/"),
        "magic_item": ("/compendium/magic-items/", "content/compendium/magic-items/"),
        "race":       ("/compendium/species/", "content/compendium/species/"),
        "class":      ("/compendium/classes/", "content/compendium/classes/"),
        "subclass":   ("/compendium/classes/", "content/compendium/classes/"),
        "feat":       ("/compendium/feats/", "content/compendium/feats/"),
    }
    ref_prefix, file_prefix = prefix_map.get(entity_type, ("/compendium/", "content/compendium/"))
    expected_ref = f"{ref_prefix}{slug}/"
    expected_file = f"{file_prefix}{slug}.md"

    # Remover refs stale do mesmo prefixo (ex: raça antiga)
    if stale_refs is not None and stale_prefixes:
        for prefix in stale_prefixes:
            for ref in list(stale_refs):
                if ref.startswith(prefix) and ref != expected_ref:
                    stale_refs.add(ref)

    if expected_ref in existing_refs and os.path.exists(expected_file):
        return None  # Já existe, nada a fazer

    print(f"  Stub ausente ou ref faltando: '{name}' ({entity_type})")
    ref = fetch_from_5etools(entity_type, name)
    if ref:
        new_refs.append(ref)
        return ref
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza e atualiza o compêndio local a partir de adições manuais na ficha de personagem."
    )
    parser.add_argument(
        "character_file",
        type=str,
        help="Caminho para o arquivo Markdown do personagem (ex: content/campaigns/.../characters/pinky.md)"
    )
    args = parser.parse_args()

    file_path = args.character_file
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)

    print(f"Lendo a ficha de personagem: {file_path}...")
    try:
        frontmatter, body_str = parse_markdown_file(file_path)
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        sys.exit(1)

    char_info = frontmatter.get("char_info", {})
    compendium_refs: list = frontmatter.get("compendium_refs", []) or []
    existing_refs: set = set(compendium_refs)
    new_refs: list = []
    refs_to_remove: set = set()
    dirty = False  # Rastreia se algo mudou além de compendium_refs

    # -----------------------------------------------------------------------
    # 1. Recalcular mods a partir de stats (se stats existir)
    # -----------------------------------------------------------------------
    stats = char_info.get("stats", {})
    if stats:
        attr_keys = ["str", "dex", "con", "int", "wis", "cha"]
        new_mods = {k: get_modifier(stats[k]) for k in attr_keys if k in stats}
        current_mods = char_info.get("mods", {})
        if new_mods != current_mods:
            print(f"  Recalculando modificadores de atributo...")
            char_info["mods"] = new_mods
            dirty = True
            for k, v in new_mods.items():
                sign = "+" if v >= 0 else ""
                print(f"    {k.upper()}: {sign}{v}")

    # -----------------------------------------------------------------------
    # 2. Processar Raça (race) — detecta troca e remove ref stale
    # -----------------------------------------------------------------------
    race_name = char_info.get("race", "")
    if race_name:
        slug = slugify(race_name)
        expected_ref = f"/compendium/species/{slug}/"
        expected_file = f"content/compendium/species/{slug}.md"

        # Detectar refs stale de raça, incluindo o caminho legado /races/
        for ref in list(existing_refs):
            if any(ref.startswith(prefix) for prefix in ("/compendium/species/", "/compendium/races/")) and ref != expected_ref:
                refs_to_remove.add(ref)
                print(f"  Removendo ref de raça desatualizada: {ref}")

        if expected_ref not in existing_refs or not os.path.exists(expected_file):
            print(f"  Raça '{race_name}' ausente no compêndio, buscando...")
            ref = fetch_from_5etools("race", race_name)
            if ref:
                new_refs.append(ref)

    # -----------------------------------------------------------------------
    # 3. Processar Magias (spells)
    # -----------------------------------------------------------------------
    spells = char_info.get("spells", []) or []
    for spell in spells:
        spell_name = spell.get("name") if isinstance(spell, dict) else spell
        if not spell_name:
            continue
        slug = slugify(spell_name)
        expected_ref = f"/compendium/spells/{slug}/"
        expected_file = f"content/compendium/spells/{slug}.md"
        if expected_ref not in existing_refs or not os.path.exists(expected_file):
            print(f"  Magia ausente: '{spell_name}'")
            ref = fetch_from_5etools("spell", spell_name)
            if ref:
                new_refs.append(ref)
                if isinstance(spell, dict):
                    spell["ref"] = ref

    # -----------------------------------------------------------------------
    # 4. Processar Equipamentos (equipment)
    # -----------------------------------------------------------------------
    equipment = char_info.get("equipment", []) or []
    for item in equipment:
        item_name = item.get("name") if isinstance(item, dict) else item
        if not item_name:
            continue
        slug = slugify(item_name)
        ref_item = f"/compendium/items/{slug}/"
        ref_magic = f"/compendium/magic-items/{slug}/"
        file_item = f"content/compendium/items/{slug}.md"
        file_magic = f"content/compendium/magic-items/{slug}.md"

        ref_exists = ref_item in existing_refs or ref_magic in existing_refs
        file_exists = os.path.exists(file_item) or os.path.exists(file_magic)

        if not ref_exists or not file_exists:
            print(f"  Item ausente: '{item_name}'")
            ref = fetch_from_5etools("magic_item", item_name)
            if not ref:
                ref = fetch_from_5etools("item", item_name)
            if ref:
                new_refs.append(ref)
                if isinstance(item, dict):
                    item["ref"] = ref

    # -----------------------------------------------------------------------
    # 4.5 Processar Propriedades de Maestria de Arma (D&D 2024 / XPHB)
    # Armas podem ter `mastery: ['Slow|XPHB']` nos dados do 5e.tools.
    # Garantimos stubs das propriedades no compêndio.
    # -----------------------------------------------------------------------
    for item in equipment:
        if not isinstance(item, dict):
            continue
        item_mastery_list = item.get("mastery") or []
        if isinstance(item_mastery_list, str):
            item_mastery_list = [item_mastery_list]
        for mastery_entry in item_mastery_list:
            mastery_name = mastery_entry.split("|")[0].strip()
            mastery_slug = "weapon-mastery-" + slugify(mastery_name)
            expected_ref = f"/compendium/rules/{mastery_slug}/"
            expected_file = f"content/compendium/rules/{mastery_slug}.md"
            if expected_ref not in existing_refs or not os.path.exists(expected_file):
                print(f"  Propriedade de maestria ausente: '{mastery_name}'")
                ref = fetch_from_5etools("item_mastery", mastery_name)
                if ref:
                    new_refs.append(ref)

    # -----------------------------------------------------------------------
    # 5. Processar Classes e Subclasses (classes_progression)
    # -----------------------------------------------------------------------
    classes_prog = char_info.get("classes_progression", []) or []
    for cl in classes_prog:
        cls_name = cl.get("name") if isinstance(cl, dict) else cl
        subcls_name = cl.get("subclass") if isinstance(cl, dict) else None

        if cls_name:
            slug = slugify(cls_name)
            expected_ref = f"/compendium/classes/{slug}/"
            expected_file = f"content/compendium/classes/{slug}.md"
            if expected_ref not in existing_refs or not os.path.exists(expected_file):
                print(f"  Classe ausente: '{cls_name}'")
                ref = fetch_from_5etools("class", cls_name)
                if ref:
                    new_refs.append(ref)

        if subcls_name:
            slug_sub = slugify(subcls_name)
            expected_ref_sub = f"/compendium/classes/{slug_sub}/"
            expected_file_sub = f"content/compendium/classes/{slug_sub}.md"
            if expected_ref_sub not in existing_refs or not os.path.exists(expected_file_sub):
                print(f"  Subclasse ausente: '{subcls_name}'")
                ref = fetch_from_5etools("subclass", subcls_name)
                if ref:
                    new_refs.append(ref)

    # -----------------------------------------------------------------------
    # 6. Processar Talentos (feats / feat string)
    # -----------------------------------------------------------------------
    feats = char_info.get("feats", []) or []
    if not feats:
        feat_str = char_info.get("feat", "")
        if feat_str:
            feats = [f.strip() for f in feat_str.split(",") if f.strip()]

    # Nota: alias de feats são tratados internamente em fetch_from_5etools
    for feat in feats:
        feat_name = feat.get("name") if isinstance(feat, dict) else feat
        if not feat_name:
            continue
        slug = slugify(feat_name)
        expected_ref = f"/compendium/feats/{slug}/"
        expected_file = f"content/compendium/feats/{slug}.md"
        if expected_ref not in existing_refs or not os.path.exists(expected_file):
            print(f"  Talento ausente: '{feat_name}'")
            ref = fetch_from_5etools("feat", feat_name)
            if ref:
                new_refs.append(ref)

    # -----------------------------------------------------------------------
    # 6.5 Processar ações e características compartilhadas
    # -----------------------------------------------------------------------
    shared_entries = []
    shared_entries.extend(char_info.get("actions", []) or [])
    shared_entries.extend(char_info.get("features", []) or [])
    for entry in shared_entries:
        if not isinstance(entry, dict):
            continue
        entry_name = entry.get("name")
        if not entry_name:
            continue

        ref = entry.get("ref")
        if ref and ref_has_content(ref):
            if ref not in existing_refs:
                new_refs.append(ref)
            # A descrição deixa de ser duplicada somente após validar a nota.
            if entry.get("description"):
                del entry["description"]
                dirty = True
            continue

        resolved_ref = resolve_action_ref(entry_name)
        if resolved_ref and ref_has_content(resolved_ref):
            entry["ref"] = resolved_ref
            if resolved_ref not in existing_refs:
                new_refs.append(resolved_ref)
            if entry.get("description"):
                del entry["description"]
            dirty = True
            print(f"  Conteúdo compartilhado resolvido: '{entry_name}' -> {resolved_ref}")
        else:
            print(f"  Pendente: nenhuma nota local inequívoca para '{entry_name}'")

    # -----------------------------------------------------------------------
    # 7. Consolidar e gravar
    # -----------------------------------------------------------------------
    # Remover refs stale e adicionar novas
    updated_refs = set(compendium_refs) - refs_to_remove
    added_refs = [r for r in new_refs if r and r not in updated_refs]
    updated_refs.update(added_refs)

    refs_changed = refs_to_remove or added_refs
    if refs_changed:
        frontmatter["compendium_refs"] = sorted(list(updated_refs))
        if refs_to_remove:
            print(f"  {len(refs_to_remove)} ref(s) stale removida(s).")
        if added_refs:
            print(f"  {len(added_refs)} nova(s) referência(s) adicionada(s).")

    if refs_changed or dirty:
        if dirty:
            frontmatter["char_info"] = char_info
        save_markdown_file(file_path, frontmatter, body_str)
        print("Ficha do personagem salva com sucesso.")
    else:
        print("Tudo sincronizado! Nenhuma atualização necessária.")


if __name__ == "__main__":
    main()
