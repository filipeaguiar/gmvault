#!/usr/bin/env python3
"""Edita equipamentos de personagens locais por uma CLI interativa."""

from __future__ import annotations

import glob
import re
from pathlib import Path

import frontmatter

import dnd_utils
from create_character import ask, ask_choice, ask_int


CHARACTER_GLOB = "content/campaigns/*/characters/*.md"
EQUIPPABLE_ITEM_TYPES = {
    "Weapon",
    "Light Armor",
    "Medium Armor",
    "Heavy Armor",
    "Shield",
    "Ring",
    "Wondrous item",
    "Wand",
    "Rod",
    "Staff",
}
FRONT_MATTER_PATTERN = re.compile(
    rb"\A---[ \t]*(?:\r\n|\n).*?^(?:---|\.\.\.)[ \t]*(?P<body>(?:\r\n|\n)?.*)\Z",
    re.DOTALL | re.MULTILINE,
)


def find_characters(pattern: str = CHARACTER_GLOB) -> list[tuple[str, Path]]:
    """Localiza fichas de personagem e devolve opções para ``ask_choice``."""
    characters: list[tuple[str, Path]] = []
    for raw_path in sorted(glob.glob(pattern)):
        path = Path(raw_path)
        if path.name == "_index.md":
            continue
        try:
            post = frontmatter.load(path)
        except (OSError, TypeError, ValueError):
            continue
        char_info = post.get("char_info")
        kind = post.get("kind") or (post.get("params") or {}).get("kind")
        if kind != "character" and not isinstance(char_info, dict):
            continue
        title = str(post.get("title") or path.stem)
        campaign = path.parents[1].name
        characters.append((f"{title} ({campaign})", path))
    return characters


def choose_character(characters: list[tuple[str, Path]]) -> Path:
    """Solicita a escolha de uma das fichas encontradas."""
    selected = ask_choice("Qual personagem deseja editar?", characters)
    return selected[1]


def choose_equipment() -> list[dict[str, object]]:
    """Busca, desambigua e coleta quantidades dos itens escolhidos."""
    selected_items: list[dict[str, object]] = []
    while True:
        query = ask("Nome do item a adicionar (vazio para finalizar)").strip()
        if not query:
            break
        matches = dnd_utils.search_item_by_name(query)
        if not matches:
            print("Nenhum item encontrado com esse nome.")
            continue
        selected = matches[0] if len(matches) == 1 else ask_choice(
            "Múltiplos itens encontrados. Qual deseja adicionar?", matches
        )
        quantity = ask_int(f"Quantidade de {selected}", 1)
        if quantity < 1:
            print("A quantidade deve ser maior que zero.")
            continue
        selected_items.append({"name": selected, "quantity": quantity})
    return selected_items


def choose_spells() -> list[dict[str, object]]:
    """Busca e coleta magias a adicionar."""
    selected_spells: list[dict[str, object]] = []
    spell_data = dnd_utils.load_spell_data()
    while True:
        query = ask("Nome da magia a adicionar (vazio para finalizar)").strip()
        if not query:
            break
        matches = dnd_utils.search_spell_by_name(query, spell_data)
        if not matches:
            print("Nenhuma magia encontrada com esse nome.")
            continue
        selected = matches[0] if len(matches) == 1 else ask_choice(
            "Múltiplos resultados. Qual deseja adicionar?", matches
        )

        spell_lvl = 0
        for spell in spell_data.get("spell", []):
            if spell.get("name") == selected:
                spell_lvl = spell.get("level", 0)
                break

        selected_spells.append({"name": selected, "level": spell_lvl})
    return selected_spells


def add_spells(
    post: frontmatter.Post, selected_spells: list[dict[str, object]]
) -> int:
    """Adiciona magias, calcula slots e registra referências."""
    char_info = post.get("char_info")
    if not isinstance(char_info, dict):
        char_info = {}
        post["char_info"] = char_info

    spells = char_info.get("spells")
    if not isinstance(spells, list):
        spells = []
    spells = dnd_utils.normalize_character_spell_entries(spells)
    char_info["spells"] = spells

    references = post.get("compendium_refs")
    if not isinstance(references, list):
        references = []
        post["compendium_refs"] = references

    class_name = char_info.get("class", "")
    level = int(char_info.get("level") or char_info.get("class_level") or 1)

    # Calculate slots if not already present
    if "spell_slots" not in char_info or not char_info["spell_slots"]:
        slots = dnd_utils.calculate_spell_slots(class_name, level)
        if slots:
            char_info["spell_slots"] = slots

    # Auto import class list if prepared caster
    prepared_caster_classes = {
        "cleric",
        "paladin",
        "druid",
        "artificer",
        "clérigo",
        "paladino",
        "druida",
        "artífice",
    }
    is_prepared_caster = class_name.lower() in prepared_caster_classes
    if is_prepared_caster:
        class_spells = char_info.get("class_spells")
        if not isinstance(class_spells, list) or len(class_spells) == 0:
            print(f"Baixando automaticamente todas as magias de {class_name}...")
            class_spell_refs = list(dict.fromkeys(
                ref for ref in dnd_utils.import_all_class_spells(class_name)
                if dnd_utils.canonical_spell_ref(ref)
            ))
            char_info["class_spells"] = class_spell_refs
            for r in class_spell_refs:
                if r not in references:
                    references.append(r)

    profile_kind = dnd_utils.infer_spellcasting_profile(class_name, level)["kind"]
    is_prepared = profile_kind == "prepared"
    added = 0
    existing_refs = {
        entry.get("ref") for entry in spells
        if isinstance(entry, dict) and entry.get("ref")
    }
    for selected in selected_spells:
        name = str(selected["name"])
        entry = dnd_utils.materialize_spell_entry(
            name,
            prepared=True if is_prepared else None,
            availability="prepared" if is_prepared else "known",
            source="class",
            usage="1 action",
            can_prepare=is_prepared,
        )
        if not entry:
            print(
                f"Não foi possível adicionar {name}: "
                "magia não resolvida no compêndio."
            )
            continue

        if entry["ref"] not in existing_refs:
            spells.append(entry)
            existing_refs.add(entry["ref"])
            added += 1
        if entry["ref"] not in references:
            references.append(entry["ref"])

    canonical = dnd_utils.deduplicate_spell_entries(
        entry for entry in spells if isinstance(entry, dict) and entry.get("ref")
    )
    unresolved = [
        entry for entry in spells
        if isinstance(entry, dict) and not entry.get("ref")
    ]
    char_info["spells"] = canonical + unresolved
    class_spells = char_info.get("class_spells")
    if isinstance(class_spells, list):
        char_info["class_spells"] = list(dict.fromkeys(
            ref for ref in class_spells if dnd_utils.canonical_spell_ref(ref)
        ))
    else:
        char_info["class_spells"] = []
    char_info["spellcasting"] = dnd_utils.infer_spellcasting_profile(
        class_name,
        level,
        spell_slots=char_info.get("spell_slots") or {},
        spells=char_info["spells"],
        class_spells=char_info["class_spells"],
    )
    post["compendium_refs"] = list(dict.fromkeys(references))
    return added


def add_equipment(post: frontmatter.Post, selected_items: list[dict[str, object]]) -> int:
    """Adiciona os itens resolvidos e suas referências ao front matter."""
    char_info = post.get("char_info")
    if not isinstance(char_info, dict):
        char_info = {}
        post["char_info"] = char_info
    equipment = char_info.get("equipment")
    if not isinstance(equipment, list):
        equipment = []
        char_info["equipment"] = equipment
    references = post.get("compendium_refs")
    if not isinstance(references, list):
        references = []
        post["compendium_refs"] = references

    added = 0
    for selected in selected_items:
        name = str(selected["name"])
        item_ref = dnd_utils.fetch_from_5etools("item", name)
        if not item_ref:
            print(f"Não foi possível adicionar {name}: item não resolvido no compêndio.")
            continue
        equipment.append(
            {
                "name": name,
                "ref": item_ref,
                "quantity": int(selected["quantity"]),
                "equipped": bool(selected.get("equipped", False)),
            }
        )
        if item_ref not in references:
            references.append(item_ref)
        added += 1
    return added


def resolve_compendium_item(item: dict[str, object]) -> frontmatter.Post | None:
    """Resolve uma referência de item para sua página Markdown local."""
    ref = item.get("ref")
    if not isinstance(ref, str) or not ref.startswith("/"):
        return None
    relative = ref.strip("/")
    candidates = [
        Path("content") / f"{relative}.md",
        Path("content") / relative / "_index.md",
    ]
    for candidate in candidates:
        if candidate.is_file():
            try:
                return frontmatter.load(candidate)
            except (OSError, TypeError, ValueError):
                return None
    return None


def is_equippable_item(item: dict[str, object]) -> bool:
    """Identifica itens vestíveis, armas e armaduras usando o compêndio."""
    page = resolve_compendium_item(item)
    if page is None:
        return bool(item.get("equipped"))
    item_info = page.get("item_info")
    if not isinstance(item_info, dict):
        return bool(item.get("equipped"))
    item_type = item_info.get("type")
    if item_type in EQUIPPABLE_ITEM_TYPES:
        return True
    if any(
        key in item_info
        for key in ("damage", "armor_class", "modifiers", "attunement")
    ):
        return True
    # Notas antigas de armas podem ter sido importadas sem tipo nem descrição.
    if item_type == "Adventuring Gear" and not page.content.strip():
        return True
    return False


def choose_equipped_items(post: frontmatter.Post) -> bool:
    """Aplica uma seleção numérica final aos itens equipáveis da ficha."""
    char_info = post.get("char_info")
    if not isinstance(char_info, dict):
        return False
    equipment = char_info.get("equipment")
    if not isinstance(equipment, list):
        return False

    candidates = [
        item
        for item in equipment
        if isinstance(item, dict) and is_equippable_item(item)
    ]
    if not candidates:
        print("Nenhum item equipável encontrado.")
        return False

    print("\nItens equipáveis:")
    for number, item in enumerate(candidates, start=1):
        marker = " [equipado]" if item.get("equipped") else ""
        quantity = int(item.get("quantity", 1) or 1)
        print(f"  {number}. {item.get('name', 'Item')} (x{quantity}){marker}")

    while True:
        raw = ask(
            "Itens a equipar, separados por vírgula "
            "(99 equipa todos; 0 desequipa todos; vazio mantém o estado atual)"
        ).strip()
        if not raw:
            return False
        if raw == "99":
            selected_numbers: set[int] = set(range(1, len(candidates) + 1))
        elif raw == "0":
            selected_numbers = set()
        else:
            parts = [part.strip() for part in raw.split(",")]
            try:
                selected_numbers = {int(part) for part in parts if part}
            except ValueError:
                print("Informe somente números separados por vírgula.")
                continue
            if not selected_numbers or any(
                number < 1 or number > len(candidates)
                for number in selected_numbers
            ):
                print(
                    f"Escolha números entre 1 e {len(candidates)}, 99 para todos, ou 0."
                )
                continue

        changed = False
        for number, item in enumerate(candidates, start=1):
            equipped = number in selected_numbers
            if bool(item.get("equipped")) != equipped:
                item["equipped"] = equipped
                changed = True
        return changed


def read_body_bytes(path: Path) -> bytes:
    """Captura os bytes após o delimitador YAML para preservação exata."""
    match = FRONT_MATTER_PATTERN.match(path.read_bytes())
    if not match:
        raise ValueError(f"Front matter YAML inválido ou ausente: {path}")
    return match.group("body")


def save_character(path: Path, post: frontmatter.Post, body: bytes) -> None:
    """Regrava o YAML alterado e mantém o corpo Markdown byte a byte."""
    metadata_only = frontmatter.Post("", **post.metadata)
    serialized = frontmatter.dumps(metadata_only).encode("utf-8")
    match = FRONT_MATTER_PATTERN.match(serialized)
    if not match:
        raise ValueError("Não foi possível serializar o front matter do personagem.")
    header = serialized[: match.start("body")]
    path.write_bytes(header + body)


def edit_selected_character(path: Path) -> str:
    """Mantém o usuário no menu do personagem até uma navegação explícita."""
    original_body = read_body_bytes(path)
    post = frontmatter.load(path)
    title = post.get("title") or path.stem
    print(f"\nPersonagem selecionado: {title}")

    while True:
        action = ask_choice(
            f"Editar {title}",
            [
                "Adicionar equipamentos",
                "Adicionar magias",
                "Escolher outro personagem",
                "Voltar ao menu principal",
            ],
        )
        if action == "Voltar ao menu principal":
            return "main_menu"
        if action == "Escolher outro personagem":
            return "character_list"

        changed = False
        if action == "Adicionar equipamentos":
            selected_items = choose_equipment()
            added = add_equipment(post, selected_items)
            equipment_changed = choose_equipped_items(post)
            changed = (added > 0) or equipment_changed
        elif action == "Adicionar magias":
            selected_spells = choose_spells()
            added = add_spells(post, selected_spells)
            changed = added > 0

        if changed:
            save_character(path, post, original_body)
            print(f"Ficha atualizada: {path}")
        else:
            print("Nenhuma alteração realizada.")


def main() -> int:
    """Seleciona personagens até o usuário voltar ao menu principal."""
    while True:
        characters = find_characters()
        if not characters:
            print("Nenhum personagem encontrado.")
            return 1
        path = choose_character(characters)
        destination = edit_selected_character(path)
        if destination == "main_menu":
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
