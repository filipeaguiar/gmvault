#!/usr/bin/env python3
"""Translate draft Markdown content with Argos Translate and a controlled RPG glossary.

This script is intentionally independent from Hugo. Hugo builds must not require
Argos Translate; only this optional post-import workflow does.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:  # pragma: no cover - exercised in environments without PyYAML
    yaml = None

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_GLOSSARY = PROJECT_ROOT / "translation_glossary.json"
DEFAULT_OPENAI_COMPATIBLE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_OPENAI_COMPATIBLE_MODEL = "google/gemma-4-e4b"
DEFAULT_OPENAI_COMPATIBLE_TIMEOUT = 300.0
DEFAULT_LMSTUDIO_URL = DEFAULT_OPENAI_COMPATIBLE_URL
DEFAULT_LMSTUDIO_MODEL = DEFAULT_OPENAI_COMPATIBLE_MODEL
DEFAULT_LMSTUDIO_TIMEOUT = DEFAULT_OPENAI_COMPATIBLE_TIMEOUT
PROTECTED_PREFIX = "ZXQPROTECTED"
GLOSSARY_PREFIX = "ZXQGLOSSARY"

STRUCTURAL_FRONT_MATTER_KEYS = {
    "kind",
    "params",
    "draft",
    "date",
    "lastmod",
    "weight",
    "visibility",
    "status",
    "tags",
    "related",
    "characters",
    "npcs",
    "locations",
    "factions",
    "handouts",
    "compendium_refs",
    "stats",
    "stats_meta",
    "char_info",
    "spell_info",
    "item_info",
    "feat_info",
    "race_info",
    "class_info",
    "spells_usage",
    "aliases",
    "url",
    "slug",
    "layout",
    "type",
    "outputs",
    "translation",
}

TEXTUAL_FRONT_MATTER_KEYS = {"summary", "description"}


@dataclass
class MarkdownDocument:
    path: Path
    front_matter_raw: str
    front_matter: dict[str, Any]
    body: str


@dataclass
class ProcessResult:
    path: Path
    changed: bool
    skipped_reason: str | None = None


@dataclass
class ProcessFailure:
    path: Path
    error_type: str
    message: str
    elapsed_seconds: float


class TranslationError(RuntimeError):
    """Raised when translation cannot be performed safely."""


class Protector:
    def __init__(self) -> None:
        self._items: list[str] = []

    def protect(self, text: str) -> str:
        patterns = [
            r"```[\s\S]*?```",  # fenced code blocks
            r"~~~[\s\S]*?~~~",  # alternate fenced code blocks
            r"\{\{[\s\S]*?\}\}",  # Hugo shortcodes/templates
            r"\[\[[^\]]+\]\]",  # dice notation
            r"`[^`\n]+`",  # inline code
        ]
        for pattern in patterns:
            text = re.sub(pattern, self._store_match, text)

        # Protect link destinations but leave labels translatable.
        text = re.sub(r"(\[[^\]]+\]\()([^\)]+)(\))", self._protect_link_destination, text)
        text = re.sub(
            r"((?:href|src)\s*=\s*[\"'])([^\"']+)([\"'])",
            self._protect_html_attribute_destination,
            text,
            flags=re.IGNORECASE,
        )

        # Protect bare URLs and internal Hugo paths.
        text = re.sub(r"https?://[^\s\)\]\}\>]+", self._store_match, text)
        text = re.sub(r"(?<![\w])/(campaigns|compendium|images|static)/[^\s\)\]\}\<\"']*", self._store_match, text)
        return text

    def restore(self, text: str) -> str:
        for index, original in enumerate(self._items):
            text = text.replace(self._token(index), original)
        return text

    def _token(self, index: int) -> str:
        return f"{PROTECTED_PREFIX}{index:05d}ZXQ"

    def _store(self, value: str) -> str:
        self._items.append(value)
        return self._token(len(self._items) - 1)

    def _store_match(self, match: re.Match[str]) -> str:
        return self._store(match.group(0))

    def _protect_link_destination(self, match: re.Match[str]) -> str:
        return f"{match.group(1)}{self._store(match.group(2))}{match.group(3)}"

    def _protect_html_attribute_destination(self, match: re.Match[str]) -> str:
        return f"{match.group(1)}{self._store(match.group(2))}{match.group(3)}"


def normalize_engine(engine: str) -> str:
    return "openai-compatible" if engine == "lmstudio" else engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Traduz arquivos Markdown em draft usando Argos Translate e glossário controlado.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemplos:
  # Traduzir toda a campanha, incluindo corpo, summary/description e título em titulo_pt_br
  source .venv/bin/activate
  python3 translate_drafts.py --scope campaign --campaign journeys-through-the-radiant-citadel --translate-frontmatter --apply

  # Traduzir campanha e compêndio em paralelo, com 4 workers
  python3 translate_drafts.py --scope campaign --campaign journeys-through-the-radiant-citadel --translate-frontmatter --jobs 4 --apply
  python3 translate_drafts.py --scope compendium --translate-frontmatter --jobs 4 --apply

Observações:
  - title é preservado; a tradução do título é gravada em titulo_pt_br.
  - --jobs pode acelerar em máquinas com CPU disponível, mas use valores moderados (2-4) para evitar excesso de memória.
""",
    )
    parser.add_argument("--scope", choices=["compendium", "campaign"], help="Escopo de tradução.")
    parser.add_argument("--campaign", help="Slug da campanha. Obrigatório com --scope campaign.")
    parser.add_argument("--path", help="Subcaminho opcional dentro do escopo selecionado.")
    parser.add_argument("--apply", action="store_true", help="Grava alterações. Sem esta flag, executa dry-run.")
    parser.add_argument(
        "--include-non-draft",
        action="store_true",
        help="Inclui arquivos sem draft: true. Use apenas para manutenção controlada.",
    )
    parser.add_argument(
        "--include-image-only-handouts",
        action="store_true",
        help="Inclui handouts cujo corpo contém somente uma imagem. Por padrão, eles não usam o motor de tradução.",
    )
    parser.add_argument(
        "--translate-frontmatter",
        action="store_true",
        help="Também traduz campos textuais seguros do front matter. title é preservado e sua tradução vai para titulo_pt_br.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Número de arquivos traduzidos em paralelo. Padrão: 1. Use 2-4 para tentar acelerar.",
    )
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY), help="Caminho do glossário JSON.")
    parser.add_argument(
        "--engine",
        choices=["openai-compatible", "lmstudio", "argos"],
        default="openai-compatible",
        help="Motor de tradução. 'lmstudio' é alias retrocompatível de 'openai-compatible'.",
    )
    parser.add_argument("--base-url", default=DEFAULT_OPENAI_COMPATIBLE_URL, help="URL base do endpoint OpenAI-compatible.")
    parser.add_argument("--model", default=DEFAULT_OPENAI_COMPATIBLE_MODEL, help="Modelo textual do endpoint OpenAI-compatible.")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_OPENAI_COMPATIBLE_TIMEOUT,
        help=f"Timeout por requisição, em segundos. Padrão: {DEFAULT_OPENAI_COMPATIBLE_TIMEOUT:g}.",
    )
    parser.add_argument("--retries", type=int, default=3, help="Tentativas por bloco.")
    parser.add_argument("--force-retranslate", action="store_true", help="Permite retraduzir conteúdo já pt-BR.")
    parser.add_argument("--source", default="en", help="Código do idioma de origem Argos. Padrão: en.")
    parser.add_argument("--target", default="pb", help="Código do idioma de destino Argos. Padrão: pb (português do Brasil).")
    parser.add_argument("--interactive", "--menu", action="store_true", help="Abre o menu interativo Rich.")
    parser.add_argument("--profile", help="Nome do perfil de tradução a ser carregado de translation_config.json.")
    parser.add_argument("--config", default="translation_config.json", help="Caminho para o arquivo JSON de configuração.")
    args = parser.parse_args()
    if args.interactive:
        from interactive_cli import translation_menu

        values = translation_menu()
        if values is None:
            raise TranslationError("Operação cancelada.")
        for key, value in values.items():
            setattr(args, key, value)
    elif not args.scope:
        parser.error("--scope é obrigatório, exceto com --interactive/--menu")

    # 1. Carrega o arquivo .env se existir na raiz do projeto
    load_env(PROJECT_ROOT / ".env")

    # 2. Carrega as configurações do JSON
    config_path = PROJECT_ROOT / args.config
    config_data = load_translation_config(config_path)

    # 3. Inicializa atributos adicionais padrão
    args.strategy = "split_blocks"
    args.api_key = None

    # 4. Determina o perfil a carregar
    profile_name = args.profile or config_data.get("active_profile")
    if profile_name and "profiles" in config_data:
        profiles = config_data["profiles"]
        if profile_name in profiles:
            profile = profiles[profile_name]
            if "engine" in profile:
                args.engine = profile["engine"]
            if "model" in profile:
                args.model = profile["model"]
            if "base_url" in profile:
                args.base_url = profile["base_url"]
            if "timeout" in profile:
                args.timeout = float(profile["timeout"])
            if "strategy" in profile:
                args.strategy = profile["strategy"]
            
            env_var_name = profile.get("api_key_env_var")
            if env_var_name:
                import os
                args.api_key = os.getenv(env_var_name)

    if not args.api_key:
        import os
        args.api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")

    args.engine = normalize_engine(args.engine)
    return args


def resolve_scope(args: argparse.Namespace) -> Path:
    if args.scope == "compendium":
        base = PROJECT_ROOT / "content" / "compendium"
    else:
        if not args.campaign:
            raise TranslationError("--campaign <slug> é obrigatório quando --scope campaign é usado.")
        base = PROJECT_ROOT / "content" / "campaigns" / args.campaign

    if not base.exists():
        raise TranslationError(f"Escopo não encontrado: {base}")

    if not args.path:
        return base

    requested = Path(args.path)
    if not requested.is_absolute():
        requested = PROJECT_ROOT / requested
    requested = requested.resolve()
    base_resolved = base.resolve()

    if requested != base_resolved and base_resolved not in requested.parents:
        raise TranslationError(f"O caminho informado escapa do escopo selecionado: {requested}")
    if not requested.exists():
        raise TranslationError(f"Caminho não encontrado: {requested}")
    return requested


def discover_markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix == ".md" else []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def filter_image_only_handouts(files: list[Path], include: bool = False) -> tuple[list[Path], list[Path]]:
    """Exclude image-only handout pages that would waste a translation request."""
    if include:
        return list(files), []

    selected: list[Path] = []
    skipped: list[Path] = []
    image_only_pattern = re.compile(r"^\s*!\[[^\]]*\]\([^\)]+\)\s*$", re.DOTALL)
    for path in files:
        if "handouts" not in path.parts:
            selected.append(path)
            continue
        document = parse_markdown(path)
        if document is not None and image_only_pattern.fullmatch(document.body):
            skipped.append(path)
        else:
            selected.append(path)
    return selected, skipped


def parse_markdown(path: Path) -> MarkdownDocument | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    try:
        _, front_matter_raw, body = text.split("---", 2)
    except ValueError:
        return None
    if yaml is None:
        raise TranslationError("PyYAML não está instalado. Ative .venv e instale as dependências do script.")
    data = yaml.safe_load(front_matter_raw) or {}
    if not isinstance(data, dict):
        return None
    return MarkdownDocument(path=path, front_matter_raw=front_matter_raw, front_matter=data, body=body.lstrip("\n"))

def load_env(path: Path) -> None:
    """Carrega variáveis de ambiente de um arquivo .env para o os.environ."""
    if not path.exists():
        return
    import os
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            os.environ[key] = val


def load_translation_config(path: Path) -> dict[str, Any]:
    """Carrega o arquivo de configuração translation_config.json."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise TranslationError("O arquivo de configuração de tradução deve ser um objeto JSON.")
        return data
    except json.JSONDecodeError as exc:
        raise TranslationError(f"Erro ao decodificar translation_config.json: {exc}") from exc


def load_glossary(path: Path) -> dict[str, str]:
    if not path.exists():
        raise TranslationError(f"Glossário não encontrado: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TranslationError("Glossário deve ser um objeto JSON.")

    # Schema v1: mapa plano, mantido para compatibilidade com glossários externos.
    if "required_translations" not in data:
        return {
            source: target
            for source, target in data.items()
            if isinstance(source, str)
            and isinstance(target, str)
            and source.strip()
            and target.strip()
        }

    categories = data["required_translations"]
    if not isinstance(categories, dict):
        raise TranslationError("required_translations deve ser um objeto de categorias.")

    glossary: dict[str, str] = {}
    for category, terms in categories.items():
        if not isinstance(terms, dict):
            raise TranslationError(f"Categoria de glossário inválida: {category}")
        for source, target in terms.items():
            if not isinstance(source, str) or not isinstance(target, str) or not source.strip() or not target.strip():
                raise TranslationError(f"Termo inválido na categoria {category}: {source!r}")
            if source in glossary:
                raise TranslationError(f"Termo duplicado no glossário: {source}")
            glossary[source] = target
    return glossary


def load_glossary_config(path: Path) -> dict[str, Any]:
    """Load and validate the complete versioned glossary configuration."""
    if not path.exists():
        raise TranslationError(f"Glossário não encontrado: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TranslationError(f"Glossário JSON inválido: {exc}") from exc
    if not isinstance(data, dict):
        raise TranslationError("Glossário deve ser um objeto JSON.")
    load_glossary(path)
    for key, expected in (("protected_terms", list), ("contextual_terms", dict), ("forbidden_outputs", list)):
        if not isinstance(data.get(key, expected()), expected):
            raise TranslationError(f"{key} possui formato inválido.")
    return data


def _contains_glossary_term(text: str, term: str) -> bool:
    """Match a glossary term case-insensitively without matching inside words."""
    if not term.strip():
        return False
    pattern = re.compile(rf"(?<![\w]){re.escape(term)}(?![\w])", re.IGNORECASE)
    return pattern.search(text) is not None


def select_glossary_config(config: dict[str, Any], document_text: str) -> dict[str, Any]:
    """Return only glossary entries referenced by one complete source document.

    Forbidden outputs remain global validation rules; required translations,
    protected names and contextual rules are selected from the front matter and
    body before any translation request is made.
    """
    selected = {
        key: value
        for key, value in config.items()
        if key not in {"required_translations", "protected_terms", "contextual_terms"}
    }

    required: dict[str, dict[str, str]] = {}
    for category, terms in config.get("required_translations", {}).items():
        if not isinstance(terms, dict):
            continue
        matches = {
            source: target
            for source, target in terms.items()
            if _contains_glossary_term(document_text, source)
        }
        if matches:
            required[category] = matches
    selected["required_translations"] = required
    selected["protected_terms"] = [
        term
        for term in config.get("protected_terms", [])
        if isinstance(term, str) and _contains_glossary_term(document_text, term)
    ]
    selected["contextual_terms"] = {
        term: rule
        for term, rule in config.get("contextual_terms", {}).items()
        if _contains_glossary_term(document_text, term)
    }
    selected.setdefault("forbidden_outputs", [])
    return selected


def build_translation_prompt(config: dict[str, Any]) -> str:
    """Build the pt-BR editorial prompt from every glossary section."""
    required: list[str] = []
    for terms in config.get("required_translations", {}).values():
        if isinstance(terms, dict):
            required.extend(f"{source} => {target}" for source, target in terms.items())
    contextual = []
    for term, rule in config.get("contextual_terms", {}).items():
        note = rule.get("note", "") if isinstance(rule, dict) else str(rule)
        contextual.append(f"{term}: {note}")
    return "\n".join([
        "Você é um tradutor editorial de D&D 5e para português do Brasil.",
        "Traduza somente o texto recebido. Não explique, não resuma e retorne apenas a tradução final.",
        "Preserve rigorosamente Markdown, HTML, YAML, URLs, shortcodes, tabelas, números, dados e tokens ZXQ.",
        "Mantenha nomes próprios protegidos e aplique a terminologia obrigatória exatamente.",
        "Não produza nenhuma saída proibida.",
        "\nTRADUÇÕES OBRIGATÓRIAS:\n" + "\n".join(required),
        "\nTERMOS PROTEGIDOS:\n" + "\n".join(map(str, config.get("protected_terms", []))),
        "\nREGRAS CONTEXTUAIS:\n" + "\n".join(contextual),
        "\nSAÍDAS PROIBIDAS:\n" + "\n".join(map(str, config.get("forbidden_outputs", []))),
    ])


def get_openai_compatible_translation(
    base_url: str,
    model: str,
    system_prompt: str,
    *,
    api_key: str | None = None,
    timeout: float = DEFAULT_OPENAI_COMPATIBLE_TIMEOUT,
    retries: int = 3,
) -> Callable[[str], str]:
    """Create a translator backed by an OpenAI-compatible chat endpoint."""
    endpoint = base_url.rstrip("/") + "/chat/completions"
    attempts = max(1, retries)

    def translate(text: str) -> str:
        last_error = "resposta inválida"
        for attempt in range(attempts):
            payload = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                "temperature": 0.1,
                "max_tokens": 8192,
                "stream": False,
            }).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            request = Request(endpoint, data=payload, headers=headers, method="POST")
            try:
                with urlopen(request, timeout=timeout) as response:
                    result = json.loads(response.read().decode("utf-8"))
                choices = result.get("choices") or []
                if not choices:
                    raise ValueError("resposta sem choices")
                choice = choices[0]
                finish_reason = choice.get("finish_reason")
                content = (choice.get("message") or {}).get("content")
                if finish_reason not in {None, "stop"}:
                    raise ValueError(f"resposta truncada ({finish_reason})")
                if not isinstance(content, str) or not content.strip():
                    raise ValueError("resposta vazia")
                return content.strip()
            except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                last_error = str(exc)
                if attempt + 1 < attempts:
                    time.sleep(min(0.25 * (2**attempt), 1.0))
        raise TranslationError(f"Endpoint OpenAI-compatible falhou após {attempts} tentativa(s): {last_error}")

    return translate


def get_lmstudio_translation(
    base_url: str,
    model: str,
    system_prompt: str,
    *,
    api_key: str | None = None,
    timeout: float = DEFAULT_OPENAI_COMPATIBLE_TIMEOUT,
    retries: int = 3,
) -> Callable[[str], str]:
    """Backward-compatible alias for the OpenAI-compatible translator."""
    return get_openai_compatible_translation(
        base_url,
        model,
        system_prompt,
        api_key=api_key,
        timeout=timeout,
        retries=retries,
    )


def tokenize_glossary(text: str, glossary: dict[str, str]) -> tuple[str, dict[str, str]]:
    token_targets: dict[str, str] = {}
    for index, source in enumerate(sorted(glossary, key=len, reverse=True)):
        token = f"{GLOSSARY_PREFIX}{index:05d}ZXQ"
        pattern = re.compile(rf"(?<![\w]){re.escape(source)}(?![\w])", re.IGNORECASE)
        if pattern.search(text):
            text = pattern.sub(token, text)
            token_targets[token] = glossary[source]
    return text, token_targets


def restore_glossary(text: str, token_targets: dict[str, str]) -> str:
    for token, target in token_targets.items():
        text = text.replace(token, target)
    return text


def get_argos_translation(source_code: str, target_code: str) -> Callable[[str], str]:
    try:
        import argostranslate.translate
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise TranslationError(
            "Argos Translate não está instalado. Ative o ambiente com `source .venv/bin/activate` "
            "ou instale `argostranslate`."
        ) from exc

    installed_languages = argostranslate.translate.get_installed_languages()
    source = next((lang for lang in installed_languages if lang.code == source_code), None)
    target = next((lang for lang in installed_languages if lang.code == target_code), None)
    if source is None or target is None:
        raise TranslationError(f"Modelo Argos {source_code} -> {target_code} não está instalado.")
    translation = source.get_translation(target)
    if translation is None:
        raise TranslationError(f"Modelo Argos {source_code} -> {target_code} não está instalado.")
    return translation.translate


def translate_markdown_line(line: str, translate: Callable[[str], str]) -> str:
    """Translate textual content while preserving common Markdown syntax."""
    if not line.strip():
        return line

    heading = re.match(r"^(\s{0,3}#{1,6}\s+)(.*?)(\s*#*\s*)$", line)
    if heading and heading.group(2).strip():
        return f"{heading.group(1)}{translate(heading.group(2))}{heading.group(3)}"

    list_item = re.match(r"^(\s*(?:[-+*]|\d+[.)])\s+(?:\[[ xX]\]\s+)?)(.*)$", line)
    if list_item and list_item.group(2).strip():
        return f"{list_item.group(1)}{translate(list_item.group(2))}"

    quote = re.match(r"^(\s*(?:>\s*)+)(.*)$", line)
    if quote and quote.group(2).strip():
        return f"{quote.group(1)}{translate(quote.group(2))}"

    if re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line):
        return line

    if "|" in line and line.strip().startswith("|"):
        leading = line.startswith("|")
        trailing = line.rstrip().endswith("|")
        cells = line.strip().strip("|").split("|")
        translated_cells = []
        for cell in cells:
            prefix = re.match(r"^\s*", cell).group(0)
            suffix = re.search(r"\s*$", cell).group(0)
            core = cell.strip()
            translated_cells.append(f"{prefix}{translate(core) if core else core}{suffix}")
        rendered = "|".join(translated_cells)
        if leading:
            rendered = "|" + rendered
        if trailing:
            rendered = rendered + "|"
        return rendered

    return translate(line)


def translate_text(
    text: str,
    translate: Callable[[str], str],
    glossary: dict[str, str],
    *,
    strategy: str = "split_blocks",
    on_block: Callable[[int, int, str, float], None] | None = None,
) -> str:
    if not text.strip():
        return text

    protector = Protector()
    protected = protector.protect(text)

    if strategy == "full_document":
        block_started = time.monotonic()
        translated = translate(protected)
        translated = protector.restore(translated)
        if on_block:
            on_block(1, 1, translated, time.monotonic() - block_started)
        return translated

    translated_blocks: list[str] = []
    # Required translations are linguistic preferences carried by the model
    # prompt, not opaque placeholders. Keeping them visible lets the model
    # handle articles, prepositions, number and word order in natural pt-BR.
    blocks = re.split(r"(\n\s*\n)", protected)
    total_blocks = sum(
        1 for block in blocks if block.strip() and not re.fullmatch(r"\n\s*\n", block)
    )
    completed_blocks = 0
    block_started = time.monotonic()
    for index, block in enumerate(blocks):
        if not block.strip() or re.fullmatch(r"\n\s*\n", block):
            translated_blocks.append(block)
            continue
        translated_lines = []
        for line in block.splitlines(keepends=True):
            newline = ""
            content = line
            if content.endswith("\r\n"):
                content = content[:-2]
                newline = "\r\n"
            elif content.endswith("\n"):
                content = content[:-1]
                newline = "\n"
            translated_lines.append(translate_markdown_line(content, translate) + newline)
        translated_blocks.append("".join(translated_lines))
        completed_blocks += 1
        if on_block:
            partial_blocks = list(translated_blocks)
            if index + 1 < len(blocks) and re.fullmatch(r"\n\s*\n", blocks[index + 1]):
                partial_blocks.append(blocks[index + 1])
            partial = protector.restore("".join(partial_blocks))
            on_block(completed_blocks, total_blocks, partial, time.monotonic() - block_started)
        block_started = time.monotonic()

    translated = "".join(translated_blocks)
    translated = protector.restore(translated)
    return translated


def translate_front_matter(
    front_matter: dict[str, Any], translate: Callable[[str], str], glossary: dict[str, str]
) -> dict[str, Any]:
    updated = dict(front_matter)

    # Preserve the original title for stable imported metadata and store the
    # translated title in the editorial pt-BR field.
    title = updated.get("title")
    if isinstance(title, str) and title.strip():
        updated["titulo_pt_br"] = translate_text(title, translate, glossary)

    for key in TEXTUAL_FRONT_MATTER_KEYS:
        value = updated.get(key)
        if isinstance(value, str) and value.strip():
            updated[key] = translate_text(value, translate, glossary)
    return updated


def add_translation_metadata(
    front_matter: dict[str, Any], source: str, target: str, *, engine: str = "argos", model: str | None = None
) -> dict[str, Any]:
    updated = dict(front_matter)
    updated["draft"] = True
    translation_meta = dict(updated.get("translation") or {})
    translation_meta.update(
        {
            "source_language": source,
            "target_language": "pt-BR" if target in {"pt", "pb"} else target,
            "engine": engine,
            "status": "machine_translated",
        }
    )
    if model:
        translation_meta["model"] = model
    else:
        translation_meta.pop("model", None)
    updated["translation"] = translation_meta
    return updated


def render_markdown(front_matter: dict[str, Any], body: str) -> str:
    if yaml is None:
        raise TranslationError("PyYAML não está instalado. Ative .venv e instale as dependências do script.")
    yaml_text = yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False, width=1000).strip()
    return f"---\n{yaml_text}\n---\n\n{body.rstrip()}\n"


def process_document(
    document: MarkdownDocument,
    translate: Callable[[str], str] | None,
    glossary: dict[str, str],
    *,
    apply: bool,
    include_non_draft: bool,
    translate_frontmatter: bool,
    source: str,
    target: str,
    engine: str = "argos",
    model: str | None = None,
    force_retranslate: bool = False,
    strategy: str = "split_blocks",
    translate_fm: Callable[[str], str] | None = None,
    progress: Callable[[int, int, float], None] | None = None,
) -> ProcessResult:
    if document.front_matter.get("draft") is not True and not include_non_draft:
        return ProcessResult(document.path, changed=False, skipped_reason="not draft")
    translation_meta = document.front_matter.get("translation") or {}
    if not force_retranslate and isinstance(translation_meta, dict) and translation_meta.get("target_language") == "pt-BR":
        return ProcessResult(document.path, changed=False, skipped_reason="already translated to pt-BR")

    if translate is None:
        return ProcessResult(document.path, changed=True)

    # Limite de segurança: fallback para split_blocks se o texto for excessivamente longo
    active_strategy = strategy
    if active_strategy == "full_document" and len(document.body) > 15000:
        print(
            f"[warning] {document.path} é muito longo ({len(document.body)} caracteres). "
            f"Fazendo fallback automático para a estratégia 'split_blocks'.",
            flush=True,
        )
        active_strategy = "split_blocks"

    checkpoint_path = document.path.with_suffix(document.path.suffix + ".translation.partial")

    def checkpoint(current: int, total: int, partial_body: str, elapsed: float) -> None:
        if apply:
            checkpoint_path.write_text(
                render_markdown(document.front_matter, partial_body), encoding="utf-8"
            )
        if progress:
            progress(current, total, elapsed)

    translated_body = translate_text(
        document.body, translate, glossary, strategy=active_strategy, on_block=checkpoint
    )
    front_matter = document.front_matter
    if translate_frontmatter and translate_fm is not None:
        front_matter = translate_front_matter(front_matter, translate_fm, glossary)
    front_matter = add_translation_metadata(front_matter, source, target, engine=engine, model=model)

    rendered = render_markdown(front_matter, translated_body)
    original = document.path.read_text(encoding="utf-8")
    changed = rendered != original
    if apply and changed:
        document.path.write_text(rendered, encoding="utf-8")
    if apply:
        checkpoint_path.unlink(missing_ok=True)
    return ProcessResult(document.path, changed=changed)


def publish_completed_adventures(campaign_root: Path, *, apply: bool) -> list[Path]:
    """Publish complete translated adventures and the indexes needed to navigate to them."""
    adventures_root = campaign_root / "adventures"
    if not adventures_root.is_dir():
        return []

    published: list[Path] = []
    for adventure_root in sorted(path for path in adventures_root.iterdir() if path.is_dir()):
        markdown_files = discover_markdown_files(adventure_root)
        content_files = [path for path in markdown_files if path.name != "_index.md"]
        content_files, _ = filter_image_only_handouts(content_files)
        documents = [(path, parse_markdown(path)) for path in content_files]
        if not documents or any(
            document is None
            or not isinstance(document.front_matter.get("translation"), dict)
            or document.front_matter["translation"].get("target_language") != "pt-BR"
            for _, document in documents
        ):
            continue

        indexes = [path for path in markdown_files if path.name == "_index.md"]
        for ancestor_index in (
            adventures_root / "_index.md",
            campaign_root / "_index.md",
        ):
            if ancestor_index.is_file():
                indexes.append(ancestor_index)

        for path in sorted(set(content_files + indexes)):
            document = parse_markdown(path)
            if document is None:
                continue
            front_matter = dict(document.front_matter)
            if front_matter.get("draft") is False and front_matter.get("status") == "published":
                continue
            front_matter["draft"] = False
            front_matter["status"] = "published"
            published.append(path)
            if apply:
                path.write_text(render_markdown(front_matter, document.body), encoding="utf-8")

    return published


def run_document_batch(
    paths: list[Path],
    process_path: Callable[[Path], Any],
    *,
    jobs: int,
    on_result: Callable[[Path, Any, float], None] | None = None,
    on_error: Callable[[ProcessFailure], None] | None = None,
) -> tuple[list[Any], list[ProcessFailure]]:
    """Process every path, preserving successful work when another path fails."""
    results: list[Any] = []
    failures: list[ProcessFailure] = []

    def timed_process(path: Path) -> tuple[Any, float]:
        started = time.monotonic()
        result = process_path(path)
        return result, time.monotonic() - started

    with ThreadPoolExecutor(max_workers=max(1, jobs)) as executor:
        future_paths = {}
        future_started = {}
        for path in paths:
            future = executor.submit(timed_process, path)
            future_paths[future] = path
            future_started[future] = time.monotonic()
        for future in as_completed(future_paths):
            path = future_paths[future]
            try:
                result, elapsed = future.result()
            except Exception as exc:
                elapsed = time.monotonic() - future_started[future]
                failure = ProcessFailure(
                    path=path,
                    error_type=type(exc).__name__,
                    message=str(exc) or repr(exc),
                    elapsed_seconds=elapsed,
                )
                failures.append(failure)
                if on_error:
                    on_error(failure)
                continue
            results.append(result)
            if on_result:
                on_result(path, result, elapsed)

    return results, failures


def main() -> int:
    try:
        args = parse_args()
        root = resolve_scope(args)
        glossary_path = Path(args.glossary)
        glossary = load_glossary(glossary_path)
        glossary_config = load_glossary_config(glossary_path)
        discovered_files = discover_markdown_files(root)
        files, image_only_handouts = filter_image_only_handouts(
            discovered_files,
            include=args.include_image_only_handouts,
        )

        print(f"Escopo: {args.scope}")
        if args.scope == "campaign":
            print(f"Campanha: {args.campaign}")
        print(f"Raiz analisada: {root}")
        jobs = max(1, args.jobs)
        print(f"Modo: {'apply' if args.apply else 'dry-run'}")
        print(f"Workers: {jobs}")
        print(f"Motor: {args.engine}")
        if args.engine == "openai-compatible":
            print(f"Modelo: {args.model}")
        print(f"Arquivos Markdown encontrados: {len(discovered_files)}")
        if image_only_handouts:
            print(f"Handouts somente com imagem ignorados: {len(image_only_handouts)}")
        print(f"Arquivos enviados ao pipeline: {len(files)}")

        thread_local = threading.local()

        def translate_for_document(document: MarkdownDocument, for_frontmatter: bool = False) -> Callable[[str], str] | None:
            if not args.apply:
                return None
            if args.engine == "argos":
                if not hasattr(thread_local, "argos_translate"):
                    thread_local.argos_translate = get_argos_translation(args.source, args.target)
                return thread_local.argos_translate

            document_text = json.dumps(document.front_matter, ensure_ascii=False) + "\n" + document.body
            if args.strategy == "full_document" and not for_frontmatter:
                # Otimização para Prompt Caching: envia o glossário estático fixo sem filtragem dinâmica
                selected_config = glossary_config
            else:
                selected_config = select_glossary_config(glossary_config, document_text)
            system_prompt = build_translation_prompt(selected_config)
            if not hasattr(thread_local, "openai_compatible_translators"):
                thread_local.openai_compatible_translators = {}
            if system_prompt not in thread_local.openai_compatible_translators:
                thread_local.openai_compatible_translators[system_prompt] = get_openai_compatible_translation(
                    args.base_url,
                    args.model,
                    system_prompt,
                    api_key=args.api_key,
                    timeout=args.timeout,
                    retries=args.retries,
                )
            return thread_local.openai_compatible_translators[system_prompt]

        def process_path(path: Path) -> ProcessResult:
            document = parse_markdown(path)
            if document is None:
                return ProcessResult(path, changed=False, skipped_reason="sem front matter YAML válido")
            return process_document(
                document,
                translate_for_document(document, for_frontmatter=False),
                glossary,
                apply=args.apply,
                include_non_draft=args.include_non_draft,
                translate_frontmatter=args.translate_frontmatter,
                source=args.source,
                target=args.target,
                engine=args.engine,
                model=args.model if args.engine == "openai-compatible" else None,
                force_retranslate=args.force_retranslate,
                strategy=args.strategy,
                translate_fm=translate_for_document(document, for_frontmatter=True) if args.translate_frontmatter else None,
                progress=lambda current, total, elapsed: print(
                    f"[block] {path} {current}/{total} ({elapsed:.1f}s)", flush=True
                ),
            )

        processed = 0
        changed = 0
        skipped = len(image_only_handouts)

        def report_result(_path: Path, result: ProcessResult, elapsed: float) -> None:
            nonlocal processed, changed, skipped
            duration = f"{elapsed:.1f}s"
            if result.skipped_reason:
                skipped += 1
                print(f"[skip] {result.path} — {result.skipped_reason} ({duration})", flush=True)
            else:
                processed += 1
                if result.changed:
                    changed += 1
                    print(f"[change] {result.path} ({duration})", flush=True)
                else:
                    print(f"[ok] {result.path} — sem alterações ({duration})", flush=True)

        def report_error(failure: ProcessFailure) -> None:
            print(
                f"[error] {failure.path} — {failure.error_type}: {failure.message} "
                f"({failure.elapsed_seconds:.1f}s)",
                file=sys.stderr,
                flush=True,
            )

        results, failures = run_document_batch(
            files,
            process_path,
            jobs=jobs,
            on_result=report_result,
            on_error=report_error,
        )

        published: list[Path] = []
        if args.scope == "campaign":
            campaign_root = PROJECT_ROOT / "content" / "campaigns" / args.campaign
            published = publish_completed_adventures(campaign_root, apply=args.apply)
            for path in published:
                action = "published" if args.apply else "would publish"
                print(f"[{action}] {path}", flush=True)

        print("\nResumo:")
        print(f"  processados: {processed}")
        print(f"  alterariam/alterados: {changed}")
        print(f"  ignorados: {skipped}")
        print(f"  erros: {len(failures)}")
        if failures:
            print("\nArquivos com erro:", file=sys.stderr)
            for failure in failures:
                print(
                    f"  - {failure.path}: {failure.error_type}: {failure.message} "
                    f"({failure.elapsed_seconds:.1f}s)",
                    file=sys.stderr,
                )
        if not args.apply:
            print("\nDry-run: nenhum arquivo foi modificado. Use --apply para gravar traduções.")
        return 1 if failures else 0
    except TranslationError as exc:
        if str(exc) == "Operação cancelada.":
            print("Operação cancelada.")
            return 0
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
