"""Source integrity checks, independent of RDF syntax and reasoning."""
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = json.loads((ROOT / 'imports/versions.lock').read_text())['dependencies']


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda entry: entry['path'])
def test_pinned_bytes(entry):
    assert hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    assert entry['version_iris']
    assert entry['retrieval_date']
    assert entry['url'].startswith('https://')


def test_import_closure_is_pinned():
    resolved = {iri for entry in ENTRIES
                for iri in entry['ontology_iris'] + entry['version_iris']}
    assert {iri for entry in ENTRIES for iri in entry['imports']} <= resolved
