"""Apply the approved syntax-only repair to checksum-verified upstream bytes."""
from rdflib import Graph


def repair(data, entry):
    source = data.decode('utf-8')
    if entry['repair'] != 'prov-bfo-syntax-v1':
        raise ValueError(f'Unknown repair: {entry["repair"]}')
    if source.count('rdfs:comment:') != 1:
        raise ValueError('Expected exactly one malformed comment predicate')
    # These are existing SWRL variables, not ESBridge domain individuals.
    namespace = entry['ontology_iris'][0] + '#'
    prefixes = f'@prefix : <{namespace}> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
    repaired = prefixes + source.replace('rdfs:comment:', 'rdfs:comment')
    Graph().parse(data=repaired, format='turtle')
    return repaired.encode('utf-8')
