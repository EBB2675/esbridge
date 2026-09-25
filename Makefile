UV ?= uv
.DEFAULT_GOAL := help

.PHONY: help setup test syntax reasoning shacl queries conservativity
help:
	@echo "setup           Sync the locked Python environment"
	@echo "test            Run syntax checks and the three test layers"
	@echo "syntax          Parse the RDF source files"
	@echo "reasoning       Run reasoning tests (pending implementation)"
	@echo "shacl           Run SHACL tests (pending implementation)"
	@echo "queries         Run competency tests (pending implementation)"
	@echo "conservativity  Reserved for the external hierarchy comparison"
	@echo "imports-check  Verify pinned upstream bytes and import closure"
	@echo "imports-fetch  Restore upstream files from versions.lock"
	@echo "robot-setup    Download checksum-pinned ROBOT"
	@echo "compatibility  Run the Task 2 HermiT experiment (requires Java 17)"

setup:
	$(UV) sync --locked

test:
	$(UV) run --locked pytest

syntax:
	$(UV) run --locked pytest tests/test_syntax.py

reasoning:
	$(UV) run --locked pytest tests/test_reasoning.py

shacl:
	$(UV) run --locked pytest tests/test_shacl.py

queries:
	$(UV) run --locked pytest tests/test_queries.py

conservativity:
	@echo "Not implemented: requires pinned imports and bridge axioms."
	@exit 1

.PHONY: imports-check imports-fetch robot-setup compatibility
imports-check:
	$(UV) run --locked python scripts/dependencies.py check

imports-fetch:
	$(UV) run --locked python scripts/dependencies.py fetch

robot-setup:
	$(UV) run --locked python scripts/dependencies.py robot

# JAVA may name a Java 17 executable; otherwise use java from PATH.
compatibility: imports-check
	$(UV) run --locked python scripts/check_compatibility.py
