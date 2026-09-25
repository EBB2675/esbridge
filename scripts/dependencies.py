"""Restore or verify pinned dependencies, including explicitly locked repairs."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree as ET

from prepare_mapping import repair

ROOT = Path(__file__).resolve().parents[1]


def dependencies():
    return json.loads((ROOT / 'imports/versions.lock').read_text())['dependencies']


def verify():
    for entry in dependencies():
        path = ROOT / entry['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f'Checksum mismatch: {entry["path"]}')


def catalog():
    """Resolve all declared imports locally, including version IRIs."""
    ns = 'urn:oasis:names:tc:entity:xmlns:xml:catalog'
    ET.register_namespace('', ns)
    root = ET.Element(f'{{{ns}}}catalog', prefer='public')
    entries = dependencies()
    resolved = set()
    for entry in entries:
        for iri in entry['ontology_iris'] + entry['version_iris']:
            resolved.add(iri)
            ET.SubElement(root, f'{{{ns}}}uri', name=iri,
                          uri=(ROOT / entry['path']).as_uri())
    missing = {iri for entry in entries for iri in entry['imports']} - resolved
    if missing:
        raise ValueError(f'Unpinned imports: {sorted(missing)}')
    path = ROOT / 'build/catalog-v001.xml'
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'fetch', 'robot'])
    args = parser.parse_args()
    if args.action == 'robot':
        entries = [json.loads((ROOT / 'scripts/tools.lock').read_text())['robot']]
    else:
        entries = dependencies()
    for entry in entries:
        path = ROOT / entry['path']
        if args.action in ('fetch', 'robot'):
            with urlopen(entry['url'], timeout=120) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != entry.get('source_sha256', entry['sha256']):
                raise ValueError(f'Upstream checksum mismatch: {entry["url"]}')
            if 'repair' in entry:
                data = repair(data, entry)
            if hashlib.sha256(data).hexdigest() != entry['sha256']:
                raise ValueError(f'Generated checksum mismatch: {entry["path"]}')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f'Checksum mismatch: {path}')
        print(f'OK {entry["path"]}')
    if args.action != 'robot':
        catalog()


if __name__ == '__main__':
    main()
