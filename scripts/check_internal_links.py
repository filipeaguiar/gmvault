#!/usr/bin/env python3
"""Audit internal href/src targets emitted by a Hugo build."""

from __future__ import annotations

import argparse
import json
import posixpath
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urldefrag, urljoin, urlparse


@dataclass(frozen=True)
class Finding:
    kind: str
    source_file: str
    attribute: str
    target: str
    detail: str = ""


@dataclass(frozen=True)
class Reference:
    source_file: Path
    attribute: str
    value: str


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name.lower(): value for name, value in attrs if value is not None}
        for attribute in ("href", "src"):
            if attribute in attrs_dict:
                self.references.append((attribute, attrs_dict.get(attribute) or ""))
        anchor_id = attrs_dict.get("id") or attrs_dict.get("name")
        if anchor_id:
            self.anchors.add(anchor_id)


class PublicIndex:
    def __init__(self, public_dir: Path) -> None:
        self.public_dir = public_dir.resolve()
        self.anchors_by_file: dict[Path, set[str]] = {}
        for html_file in sorted(self.public_dir.rglob("*.html")):
            parser = LinkParser()
            parser.feed(html_file.read_text(encoding="utf-8", errors="replace"))
            self.anchors_by_file[html_file.resolve()] = parser.anchors

    def html_sources(self, scope: str | None) -> Iterable[Path]:
        scope_prefix = (scope or "").strip("/")
        for html_file in sorted(self.anchors_by_file):
            rel = html_file.relative_to(self.public_dir).as_posix()
            page_path = rel[:-len("index.html")] if rel.endswith("index.html") else rel
            if scope_prefix and not page_path.startswith(scope_prefix):
                continue
            yield html_file

    def path_to_file(self, path: str) -> Path:
        decoded = unquote(path)
        normalized = posixpath.normpath("/" + decoded.lstrip("/"))
        if normalized == "/":
            relative = "index.html"
        elif normalized.endswith("/"):
            relative = normalized.lstrip("/") + "index.html"
        else:
            name = normalized.lstrip("/")
            candidate = self.public_dir / name
            if candidate.is_dir():
                relative = name.rstrip("/") + "/index.html"
            elif candidate.exists():
                relative = name
            else:
                suffix = Path(name).suffix
                relative = name if suffix else name.rstrip("/") + "/index.html"
        return (self.public_dir / relative).resolve()

    def contains(self, file_path: Path) -> bool:
        try:
            file_path.relative_to(self.public_dir)
        except ValueError:
            return False
        return file_path.exists() and file_path.is_file()


def _base_path(base_url: str) -> str:
    parsed = urlparse(base_url)
    path = parsed.path or "/"
    if not path.endswith("/"):
        path += "/"
    return path


def _is_ignored_scheme(parsed) -> bool:
    return parsed.scheme in {"mailto", "tel", "data", "javascript"}


def _source_url_path(source_file: Path, public_dir: Path) -> str:
    rel = source_file.relative_to(public_dir.resolve()).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


def audit_public_dir(
    public_dir: Path | str,
    base_url: str,
    *,
    scope: str | None = None,
    include_external: bool = False,
) -> list[Finding]:
    public_path = Path(public_dir).resolve()
    base = urlparse(base_url)
    base_path = _base_path(base_url)
    index = PublicIndex(public_path)
    findings: list[Finding] = []

    for source_file in index.html_sources(scope):
        parser = LinkParser()
        parser.feed(source_file.read_text(encoding="utf-8", errors="replace"))
        source_path = _source_url_path(source_file, public_path)
        source_url = base_path.rstrip("/") + source_path
        for attribute, raw_target in parser.references:
            if not raw_target.strip():
                findings.append(Finding("empty-target", str(source_file), attribute, raw_target))
                continue
            parsed_raw = urlparse(raw_target)
            if _is_ignored_scheme(parsed_raw):
                continue
            if parsed_raw.scheme in {"http", "https"}:
                if parsed_raw.netloc != base.netloc:
                    if include_external:
                        findings.append(Finding("external", str(source_file), attribute, raw_target))
                    continue
                target_url = raw_target
            elif raw_target.startswith("//"):
                if include_external:
                    findings.append(Finding("external", str(source_file), attribute, raw_target))
                continue
            else:
                target_url = urljoin(source_url, raw_target)

            parsed = urlparse(target_url)
            target_no_fragment, fragment = urldefrag(target_url)
            parsed_no_fragment = urlparse(target_no_fragment)
            target_path = parsed_no_fragment.path or "/"

            if not target_path.startswith(base_path):
                findings.append(
                    Finding(
                        "outside-base-path",
                        str(source_file),
                        attribute,
                        raw_target,
                        f"expected path under {base_path}",
                    )
                )
                continue

            public_relative_path = "/" + target_path[len(base_path):].lstrip("/")
            target_file = index.path_to_file(public_relative_path)
            if not index.contains(target_file):
                findings.append(Finding("missing-file", str(source_file), attribute, raw_target))
                continue
            if fragment and attribute == "href":
                anchors = index.anchors_by_file.get(target_file, set())
                if unquote(fragment) not in anchors:
                    findings.append(Finding("missing-anchor", str(source_file), attribute, raw_target, fragment))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audita links internos de um build Hugo publicado.")
    parser.add_argument("--public", required=True, help="Diretório public/ ou destination do Hugo.")
    parser.add_argument("--base-url", required=True, help="baseURL usada no build.")
    parser.add_argument("--scope", help="Prefixo de páginas HTML de origem a auditar.")
    parser.add_argument("--include-external", action="store_true", help="Inclui URLs externas no relatório.")
    parser.add_argument("--json", action="store_true", help="Emite JSON Lines.")
    args = parser.parse_args(argv)

    findings = audit_public_dir(
        Path(args.public),
        args.base_url,
        scope=args.scope,
        include_external=args.include_external,
    )
    for finding in findings:
        if args.json:
            print(json.dumps(asdict(finding), ensure_ascii=False))
        else:
            print(
                f"{finding.kind}\t{finding.attribute}\t{finding.target}\t{finding.source_file}\t{finding.detail}".rstrip()
            )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
