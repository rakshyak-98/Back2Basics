[[Python]] [[create python package from source]] [[pandas]]

# wheel

> Built Python distribution format (`.whl`) — a zip of code + metadata so `pip install` skips a local compile when a matching wheel exists.

## Interview Relevance

Packaging interviews: wheel vs sdist, platform tags (`manylinux`, `py3-none-any`), and why Alpine/musl breaks glibc wheels.

## Sources

- [PEP 427 — The Wheel Binary Package Format](https://peps.python.org/pep-0427/) — deep-dive
- [Python Packaging User Guide — Installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/) — overview
- [manylinux](https://github.com/pypa/manylinux) — deep-dive

## Core Definition

A wheel is a pre-built artifact installable by copying files and running recorded steps — faster and more reproducible than building from an sdist on every target machine. Pure-Python wheels use tags like `py3-none-any`; native extensions need platform-specific tags.

## Key Concepts

- **Build → dist:** `python -m build` emits `.whl` and `.tar.gz` from [[create python package from source|project metadata]].
- **Tags:** `{python}-{abi}-{platform}` — pip selects a wheel compatible with the interpreter and OS.
- **manylinux / musllinux:** community platform tags for Linux binaries — glibc wheels fail on musl (Alpine) and vice versa.
- **Publish:** Twine (or trusted publishers) upload to PyPI/private index — don’t commit wheels to git as the primary distribution channel.

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

## Real-World Applications

CI builds `cp312-manylinux` wheels for a C-extension metrics library; app images `pip install` in seconds with no compiler in the runtime image.

## Pros/Cons or Trade-offs

- **Pro:** Fast, reproducible installs; smaller runtime images without toolchains.
- **Con:** Matrix of Python × ABI × OS for native code — CI complexity (cibuildwheel).

## Comparison

- vs sdist (`.tar.gz`): source requires build on install when no wheel matches.
- vs system packages (`apt`): wheels are Python-centric and versioned per environment; OS packages follow distro policy.

## Mistakes to Avoid

- Labeling a platform-specific binary wheel as `py3-none-any`.
- Hand-editing contents inside a `.whl` — rebuild from source.
- Assuming a manylinux wheel works on Alpine without checking musl.
