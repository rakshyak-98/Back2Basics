[[Python]] [[wheel]] [[pandas]]

# create python package from source

> Turn a source tree into an installable distribution — `pyproject.toml` + build backend so others can `pip install` your library.

```txt
        create python pack ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Packaging questions separate “scripts in a folder” from shippable libraries: …

## Sources
- [Python Packaging User Guide — Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) — deep-dive
- [PEP 517 — build system interface](https://peps.python.org/pep-0517/) — deep-dive
- [PEP 621 — project metadata](https://peps.python.org/pep-0621/) — overview

## Key Concepts
- **`pyproject.toml`:** declares build-system and project metadata (PEP 518/621) → reproducible build…
- **src layout:** `src/mypkg/...` avoids accidentally importing the working tree instead of the…
- **Editable install:** `pip install -e .` links the project for local development → changes show up …
- **Artifacts:** sdist (source) vs wheel (built) — prefer publishing wheels; see [[wheel]].


- **Core:** A Python package for distribution needs importable modules, metadata (name, v…

## Technical Details
- Minimal layout:

```
mypackage/
  pyproject.toml
  src/
    mypackage/
      __init__.py
      core.py
  tests/
```

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "Example library"
requires-python = ">=3.10"
dependencies = ["requests"]

[tool.setuptools.packages.find]
where = ["src"]
```

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # editable
pip install build
python -m build                  # dist/*.whl and *.tar.gz
pip install dist/mypackage-0.1.0-*.whl
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` after install | Package discovery | `packages.find` / include package data |
| Editable import wrong tree | Flat layout shadowing | Prefer `src/` layout |
| Build fails on clean CI | Missing build-system | Declare backend in `pyproject.toml` |

## Mistakes to Avoid
- **Mistake:** Dashes in import names
- **Mistake:** Forgetting to include package data (templates, py.typed) in the …
- **Mistake:** Publishing without a virtual environment

## Pros/Cons or Trade-offs
- **Pro:** Versioning, dependencies, and entry points travel with the code.
- **Con:** Overkill for a one-off notebook script — a module in the app tree may be enough.

## Comparison
- vs [[wheel]]: this note is *how to author*; wheel is the *binary/built install format*.
- vs copying a folder onto `PYTHONPATH`: fragile across environments; packaging encodes metadata.


### Use cases
- Internal metrics helper used by three services: package once, version on the …
