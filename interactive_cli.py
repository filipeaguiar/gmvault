#!/usr/bin/env python3
"""Launcher e menus Rich reutilizáveis para os scripts do projeto."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

console = Console()
PROJECT_ROOT = Path(__file__).resolve().parent

OPERATIONS = {
    "1": ("Importar campanha do 5e.tools", "import_campaign.py"),
    "2": ("Importar personagem do D&D Beyond", "import_dndbeyond.py"),
    "3": ("Criar personagem manualmente", "create_character.py"),
    "4": ("Editar personagem", "edit_character.py"),
    "5": ("Traduzir drafts", "translate_drafts.py"),
}


def _numbered_choice(title: str, options: list[tuple[str, Any]], default: int = 1) -> Any:
    """Mostra todas as opções numeradas e devolve o valor escolhido."""
    console.print(f"\n[bold]{title}[/]")
    for index, (label, _) in enumerate(options, start=1):
        console.print(f"  [bold cyan]{index}[/]  {label}")
    choice = IntPrompt.ask(
        "Escolha uma opção",
        choices=[str(index) for index in range(1, len(options) + 1)],
        default=default,
    )
    return options[choice - 1][1]


def _summary(title: str, values: dict[str, Any]) -> bool:
    table = Table(show_header=False, box=None)
    for label, value in values.items():
        table.add_row(label, str(value if value not in (None, "") else "—"))
    console.print(Panel(table, title=title, border_style="cyan"))
    return _numbered_choice(
        "Confirmação",
        [("Continuar", True), ("Cancelar", False)],
    )


def campaign_menu() -> dict[str, Any] | None:
    console.print(Panel("Importar campanha do 5e.tools", style="bold blue"))
    values = {"slug": Prompt.ask("Slug da aventura", default="jttrc").strip()}
    return values if _summary("Resumo da importação", values) else None


def dndbeyond_menu() -> dict[str, Any] | None:
    console.print(Panel("Importar personagem do D&D Beyond", style="bold blue"))

    campaign_options: list[tuple[str, str]] = []
    campaigns_dir = PROJECT_ROOT / "content" / "campaigns"
    if campaigns_dir.is_dir():
        for campaign in sorted(path for path in campaigns_dir.iterdir() if path.is_dir()):
            campaign_options.append((campaign.name, campaign.name))

    values: dict[str, Any] = {"char_id": Prompt.ask("ID do personagem").strip()}

    if campaign_options:
        selected = _numbered_choice("Campanha do personagem", campaign_options)
        values["campaign"] = selected
    else:
        console.print("[yellow]Nenhuma campanha encontrada. Usando slug manual.[/]")
        values["campaign"] = Prompt.ask("Slug da campanha", default="cidadela-radiante").strip()

    return values if _summary("Resumo da importação", values) else None


def create_character_menu() -> dict[str, Any] | None:
    console.print(Panel("Criar personagem manualmente", style="bold blue"))

    campaign_options: list[tuple[str, str]] = []
    campaigns_dir = PROJECT_ROOT / "content" / "campaigns"
    if campaigns_dir.is_dir():
        for campaign in sorted(path for path in campaigns_dir.iterdir() if path.is_dir()):
            campaign_options.append((campaign.name, campaign.name))

    values: dict[str, Any] = {}

    if campaign_options:
        selected = _numbered_choice("Campanha do personagem", campaign_options)
        values["campaign"] = selected
    else:
        console.print("[yellow]Nenhuma campanha encontrada. Usando slug manual.[/]")
        values["campaign"] = Prompt.ask("Slug da campanha", default="cidadela-radiante").strip()

    return values if _summary("Resumo", values) else None


def _translation_targets() -> list[tuple[str, dict[str, Any]]]:
    targets: list[tuple[str, dict[str, Any]]] = []
    compendium = PROJECT_ROOT / "content" / "compendium"
    if compendium.is_dir():
        targets.append(("Compêndio", {"scope": "compendium", "campaign": None}))

    campaigns = PROJECT_ROOT / "content" / "campaigns"
    if campaigns.is_dir():
        for campaign in sorted(path for path in campaigns.iterdir() if path.is_dir()):
            targets.append(
                (
                    f"Campanha: {campaign.name}",
                    {"scope": "campaign", "campaign": campaign.name},
                )
            )
    return targets


def translation_menu() -> dict[str, Any] | None:
    console.print(Panel("Traduzir conteúdo já baixado", style="bold blue"))
    targets = _translation_targets()
    if not targets:
        console.print("[yellow]Nenhum conteúdo baixado foi encontrado em content/.[/]")
        return None

    target = _numbered_choice("Conteúdo para traduzir", targets)
    jobs = _numbered_choice(
        "Número de workers",
        [("1 worker", 1), ("2 workers", 2), ("4 workers", 4), ("8 workers", 8)],
        default=1,
    )
    apply = _numbered_choice(
        "Modo de execução",
        [("Somente simular (dry-run)", False), ("Gravar traduções", True)],
    )
    include_non_draft = _numbered_choice(
        "Arquivos considerados",
        [("Somente drafts", False), ("Todos os arquivos", True)],
    )
    translate_frontmatter = _numbered_choice(
        "Front matter",
        [("Traduzir campos textuais", True), ("Não traduzir campos textuais", False)],
    )
    values = {
        **target,
        "path": None,
        "apply": apply,
        "include_non_draft": include_non_draft,
        "translate_frontmatter": translate_frontmatter,
        "jobs": jobs,
        "glossary": "translation_glossary.json",
        "source": "en",
        "target": "pb",
    }
    return values if _summary("Resumo da tradução", values) else None


def main() -> int:
    """Delega operações e retorna ao menu até o usuário escolher sair."""
    while True:
        console.print(Panel("GM Vault — ferramentas interativas", style="bold magenta"))
        for key, (label, _) in OPERATIONS.items():
            console.print(f"  [bold cyan]{key}[/]  {label}")
        console.print("  [bold cyan]0[/]  Sair")

        choice = Prompt.ask(
            "Escolha uma operação", choices=["0", *OPERATIONS], default="0"
        )
        if choice == "0":
            console.print("Sessão encerrada.")
            return 0

        _, script_name = OPERATIONS[choice]
        script = Path(__file__).resolve().with_name(script_name)
        completed = subprocess.run(
            [sys.executable, str(script), "--menu"], check=False
        )
        if completed.returncode:
            console.print(
                f"[yellow]A operação terminou com código {completed.returncode}.[/]"
            )
        console.print("\n[cyan]Retornando ao menu inicial…[/]\n")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        console.print("\nOperação cancelada.")
        raise SystemExit(130)
