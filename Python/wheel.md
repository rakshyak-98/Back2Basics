[[Python/pandas]] [[NodeJS/node package json]] [[Release cycle]]

# Python wheel (`.whl`)

> Built distribution format — pre-built zip of code + metadata for fast `pip install` without compile on target.

## Mental model

**sdist** (source tarball) may compile C extensions on install. **wheel** ships pre-built artifacts for a platform tag (`cp312-manylinux_x86_64`). `pip` prefers wheels when tag matches. You build wheels in CI; consumers install in seconds.

```
pyproject.toml / setup.py → build backend → dist/*.whl → pip install
```

## Standard config / commands

### Modern build (PEP 517)

```bash
pip install build
python -m build              # produces dist/*.whl and *.tar.gz
pip install dist/mypackage-0.1.0-py3-none-any.whl
```

### Legacy (still seen)

```bash
pip install setuptools wheel
python setup.py bdist_wheel    # prefer python -m build
```

### pyproject.toml minimal

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
dependencies = ["requests"]
```

### Publish

```bash
pip install twine
twine upload dist/*
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `not a supported wheel` | Platform tag | Build on target arch or use pure `py3-none-any` |
| Compile on install anyway | No wheel for platform | Publish manylinux wheel via cibuildwheel |
| Wrong version installed | PyPI name clash | Unique package name; pin in requirements |
| Import error after install | Package layout | `packages=` in setuptools config |
| Huge wheel | Bundled data | Exclude tests; use MANIFEST.in carefully |

## Gotchas

> [!WARNING]
> **Manylinux vs musl (Alpine)** — glibc wheels fail on Alpine; use slim Debian base or build musllinux wheel.
>
> **Commit wheels to git** — usually wrong; publish to index or artifact store.
>
> **`setup.py` only projects** — migrate to `pyproject.toml` for reproducible builds.

## When NOT to use

- Don't hand-edit wheel contents — rebuild from source.
- Don't ship platform-specific wheels as `py3-none-any` — runtime import errors.

## Related

[[Python/pandas]] [[compiler/compiler]] [[Deployment/spinnaker]]
