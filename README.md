# ESBridge

A minimal BFO/PMDco integration profile for electronic-structure calculations.


## Local setup

Use Python 3.12, uv and GNU Make:

```sh
uv sync --locked
make test
```

The project is a collection of ontology/profile artifacts, not an installable
Python package. uv creates `.venv/`; `uv.lock` pins the Python dependencies.
RDFLib, pySHACL and pytest are installed. To activate the environment manually:

```sh
source .venv/bin/activate
```

## Pinned dependencies

Dependency versions, source URLs and checksums are recorded in
`imports/versions.lock`. Use `make imports-check` to verify local files and
`make imports-fetch` to regenerate them from the pinned sources. With Java 17 available, `make robot-setup` and
`make compatibility` reproduce the separate PMDco/PROV compatibility experiment.
The BFO mapping is a generated, syntactically corrected dependency. The lock
records the original download checksum, corrected checksum, and repair steps;
`make imports-fetch` reproduces it. All other imports are unchanged upstream
files. Syntax and checksum tests validate the files actually used by HermiT.
