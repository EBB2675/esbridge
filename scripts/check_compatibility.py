"""Task 2 experiment only: does not adopt PROV mappings into ESBridge."""
import json
import os
import subprocess
import sys

from dependencies import ROOT, catalog, verify


def main():
    verify()
    tool = json.loads((ROOT / 'scripts/tools.lock').read_text())['robot']
    import hashlib
    jar = ROOT / tool['path']
    if hashlib.sha256(jar.read_bytes()).hexdigest() != tool['sha256']:
        raise ValueError('ROBOT checksum mismatch; run make robot-setup')
    command = [os.environ.get('JAVA', 'java'), '-Xmx4G', '-jar', str(jar)]
    out = ROOT / 'build/compatibility'
    out.mkdir(parents=True, exist_ok=True)
    common = ['--reasoner', 'HermiT', '--equivalent-classes-allowed', 'all']
    local_catalog = catalog()
    cases = {
        'pmdco': ['reason', '--input', 'imports/pmdco-full.owl', *common],
        'combined': ['merge', '--catalog', str(local_catalog),
                     '--input', 'imports/pmdco-full.owl',
                     '--input', 'imports/prov-o.ttl',
                     '--input', 'imports/prov-to-bfo-bfo.ttl',
                     '--input', 'imports/prov-to-bfo-ro.ttl',
                     'reason', *common],
    }
    results = {}
    for name, args in cases.items():
        full_command = command + args + ['--output', str(out / f'{name}.owl')]
        with (out / f'{name}.log').open('w') as log:
            result = subprocess.run(full_command, cwd=ROOT, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=600)
        results[name] = {'exit_code': result.returncode, 'command': full_command}
        print(f'{name}: exit {result.returncode}; see build/compatibility/{name}.log', flush=True)
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(item['exit_code'] for item in results.values()))


if __name__ == '__main__':
    sys.exit(main())
