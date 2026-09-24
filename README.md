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


