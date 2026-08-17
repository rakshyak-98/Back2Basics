[[ASGI]] [[GIL (Global interpreter lock)]] [[wheel]] [[pandas]] [[create python package from source]]

# Python

> High-level language with a batteries-included standard library — CPython is the common runtime for scripting, services, and data work.





## Interview Relevance
Interviewers probe runtime basics: virtual environments, import/`sys.path`, packaging, debugging with `pdb`, and concurrency limits from the [[GIL (Global interpreter lock)|GIL]].

## Sources
- [Python 3 documentation](https://docs.python.org/3/) — deep-dive
- [Python glossary](https://docs.python.org/3/glossary.html) — overview
- [pdb — The Python Debugger](https://docs.python.org/3/library/pdb.html) — deep-dive

## Core Definition
Python source compiles to bytecode executed by a virtual machine (usually CPython). Indentation defines blocks; everything is an object; modules are found via `sys.path` and installed distributions.

## Key Concepts
- **Runtime vs language:** CPython vs PyPy/others — behavior and extension APIs differ; most production is CPython.
- **Virtual environments:** isolate dependencies per project — avoid installing into the system interpreter.
- **Imports:** `sys.path` search order; packages need `__init__.py` (or namespace packages) — dashes are illegal in identifiers.
- **Debugging:** `python -m pdb script.py` or breakpoints — stack inspection without a full IDE.
- **Ecosystem lanes:** web ([[ASGI]]), data ([[pandas]]), packaging ([[wheel]]) — pick tools per domain.

## Technical Details
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pdb myscript.py          # debug
python -c "import sys; print(sys.path)"
```

```python
import sys
print(sys.version)
print(sys.path)  # module search path
```

Useful stdlib modules in interviews: `asyncio`, `concurrent.futures`, `pathlib`, `json`, `unittest`/`pytest` (third-party), `inspect` for runtime reflection.

| Symptom | Check | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` | `sys.path` / venv active? | Install into the environment; fix package layout |
| Wrong Python on PATH | `which python3` | Use venv or explicit version |
| IndentationError | mixed tabs/spaces | Keep one style; editor shows invisibles |

## Real-World Applications
Glue code on a jump host: venv + small script calling cloud APIs, debugged with `pdb` when a token refresh fails — same language as the service for shared mental model.

## Pros/Cons or Trade-offs
- **Pro:** Fast to write, huge libraries, readable for ops and ML alike.
- **Con:** CPU-bound threads limited by GIL; packaging and environment drift need discipline.

## Comparison
- vs Node.js: both excel at I/O-bound services; Python stronger in scientific/data; Node stronger in isomorphic web tooling.
- vs Go/Java: those compile to heavier static binaries/services with different concurrency stories.

## Mistakes to Avoid
- Using the distro `python` for project deps — always venv/container.
- Naming modules after stdlib (`email.py`, `random.py`) — shadowing breaks imports.
- Treating threads as multi-core CPU scaling — see [[GIL (Global interpreter lock)]].
