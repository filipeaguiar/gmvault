import json
import tempfile
from pathlib import Path

from audit_glossary import audit_corpus
from translate_drafts import load_glossary_config


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_reviewed_2024_and_area_terms_are_controlled():
    config = load_glossary_config(PROJECT_ROOT / "translation_glossary.json")
    terms = config["required_translations"]["rules_2024_and_areas"]

    assert terms["Weapon Mastery"] == "Maestria de Arma"
    assert terms["Creature Type"] == "Tipo de Criatura"
    assert terms["Cylinder"] == "Cilindro"
    assert "<think>" in config["forbidden_outputs"]


def test_audit_reports_only_uncovered_occurring_candidates_without_modifying_glossary():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        corpus = root / "corpus"
        corpus.mkdir()
        (corpus / "rule.md").write_text("---\ntitle: Test\n---\n\nUse Weapon Mastery and an Emanation.\n", encoding="utf-8")
        glossary = root / "glossary.json"
        glossary.write_text(json.dumps({
            "required_translations": {"rules": {"Weapon Mastery": "Maestria de Arma"}},
            "protected_terms": [], "contextual_terms": {}, "forbidden_outputs": []
        }), encoding="utf-8")
        before = glossary.read_bytes()

        report = audit_corpus(corpus, glossary)

        assert report["uncovered_candidates"] == [{"term": "Emanation", "occurrences": 1}]
        assert glossary.read_bytes() == before


def test_staged_corpus_has_no_unresolved_5etools_markup_or_glossary_gaps():
    staging = PROJECT_ROOT / ".compendium-staging/compendium"
    if not staging.exists():
        return
    report = audit_corpus(staging, PROJECT_ROOT / "translation_glossary.json")
    assert report["unresolved_5etools_tags"] == 0
    assert report["uncovered_candidates"] == []
