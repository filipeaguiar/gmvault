"""Shared editorial content-role helpers for importers and tests."""

from __future__ import annotations

import re
from typing import Any

CONTENT_ROLE_INTRODUCTION = "introduction"
VALID_CONTENT_ROLES = {CONTENT_ROLE_INTRODUCTION}

_INTRODUCTION_TITLES = {
    "introduction",
    "introducao",
    "welcome",
    "welcome to the radiant citadel",
    "using this book",
    "using the adventures",
    "adventure background",
    "background",
    "running the adventure",
    "adventure hook",
    "adventure hooks",
    "character hooks",
    "setting the adventure",
    "starting the adventure",
    "story overview",
    "overview",
    "about the adventure",
    "character level",
    "pronunciations",
    "configurando a aventura",
}

_PLAYABLE_TITLE_PATTERNS = [
    re.compile(r"^\s*(?:area\s*)?[a-z]?\d+[\.:\s-]", re.IGNORECASE),
    re.compile(r"^\s*\d+[\.:\s-]"),
]


def normalize_title_key(title: str | None) -> str:
    text = (title or "").strip().lower()
    text = text.replace("’", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def content_role_from_front_matter(front_matter: dict[str, Any]) -> str | None:
    role = front_matter.get("content_role")
    params = front_matter.get("params")
    if role is None and isinstance(params, dict):
        role = params.get("content_role")
    return role if isinstance(role, str) and role in VALID_CONTENT_ROLES else None


def is_introduction_role(role: str | None) -> bool:
    return role == CONTENT_ROLE_INTRODUCTION


def classify_imported_content_role(title: str | None, *, level: str) -> str | None:
    """Return an explicit role for imported 5e.tools material.

    This is intentionally conservative. Titles are used only at import time;
    Hugo templates consume the persisted front matter and never reclassify by title.
    """
    if not title:
        return None

    # Remove prefixo numérico inicial de ordenação (ex: "01. ", "1: ", "1 - ") para fins de classificação
    clean_title = re.sub(r"^\s*\d+[\.:\s-]+\s*", "", title)
    key = normalize_title_key(clean_title)
    if not key:
        return None
    if any(pattern.search(clean_title) for pattern in _PLAYABLE_TITLE_PATTERNS):
        return None

    if level == "campaign_chapter":
        if key.startswith("welcome to ") or key in {"introduction", "using this book"}:
            return CONTENT_ROLE_INTRODUCTION
        return None

    if level in {"adventure_section", "session_scene"}:
        if key in _INTRODUCTION_TITLES:
            return CONTENT_ROLE_INTRODUCTION
        if key.startswith("adventure hook") or key.startswith("character hook"):
            return CONTENT_ROLE_INTRODUCTION
        return None

    return None
