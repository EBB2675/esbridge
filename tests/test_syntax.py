"""Syntax checks only; parsing does not establish semantic validity."""
from pathlib import Path

import pytest
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
RDF_FILES = sorted(
    path
    for directory in ("src/ontology", "shapes", "examples", "imports")
    for path in (ROOT / directory).rglob("*")
    if path.suffix in {".ttl", ".owl", ".rdf", ".nt"}
)


@pytest.mark.parametrize("path", RDF_FILES, ids=lambda path: str(path.relative_to(ROOT)))
def test_rdf_syntax(path):
    Graph().parse(path, format={".ttl": "turtle", ".nt": "nt"}.get(path.suffix, "xml"))
