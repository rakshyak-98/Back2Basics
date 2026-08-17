[[Python]] [[create python package from source]] [[pandas]]

# wheel

> Built Python distribution format (`.whl`) — a zip of code + metadata so `pip install` skips a local compile when a matching wheel exists.

```txt
        wheel ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Packaging interviews: wheel vs sdist, platform tags (`manylinux`, `py3-none-a…

## Sources
- [PEP 427 — The Wheel Binary Package Format](https://peps.python.org/pep-0427/) — deep-dive
- [Python Packaging User Guide — Installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/) — overview
- [manylinux](https://github.com/pypa/manylinux) — deep-dive

## Key Concepts
- **Build → dist:** `python -m build` emits `.whl` and `.tar.gz` from [[create python package fro…
- **Tags:** `{python}-{abi}-{platform}`
- **manylinux / musllinux:** community platform tags for Linux binaries
- **Publish:** Twine (or trusted publishers) upload to PyPI/private index


- **Core:** A wheel is a pre-built artifact installable by copying files and running reco…

## Technical Details
```
pyproject.toml → build backend → dist/*.whl → pip install
```

```bash
pip install build
python -m build
pip install dist/mypackage-0.1.0-py3-none-any.whl

pip install twine
twine upload dist/*
```

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `is not a supported wheel on this platform` | Filename tags | Build for target arch/ABI or ship pure `py3-none-any` |
| Pip compiles from sdist anyway | No matching wheel | Publish manylinux via cibuildwheel |
| Alpine import/crash | glibc wheel on musl | Debian slim base or musllinux wheel |
| Import error after install | Package layout | Fix setuptools package discovery |

## Mistakes to Avoid
- **Mistake:** Labeling a platform-specific binary wheel as `py3-none-any`
- **Mistake:** Hand-editing contents inside a `.whl` — rebuild from source
- **Mistake:** Assuming a manylinux wheel works on Alpine without checking musl

## Pros/Cons or Trade-offs
- **Pro:** Fast, reproducible installs; smaller runtime images without toolchains.
- **Con:** Matrix of Python × ABI × OS for native code — CI complexity (cibuildwheel).

## Comparison
- vs sdist (`.tar.gz`): source requires build on install when no wheel matches.
- vs system packages (`apt`): wheels are Python-centric and versioned per environment


### Use cases
- CI builds `cp312-manylinux` wheels for a C-extension metrics library
