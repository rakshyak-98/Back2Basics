[[ASGI]] [[GIL (Global interpreter lock)]] [[wheel]] [[pandas]] [[create python package from source]]

# Python

> High-level language with a batteries-included standard library — CPython is the common runtime for scripting, services, and data work.

```txt
        Python ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe runtime basics: virtual environments, import/`sys.path`, p…

## Sources
- [Python 3 documentation](https://docs.python.org/3/) — deep-dive
- [Python glossary](https://docs.python.org/3/glossary.html) — overview
- [pdb — The Python Debugger](https://docs.python.org/3/library/pdb.html) — deep-dive

## Key Concepts
- **Runtime vs language:** CPython vs PyPy/others
- **Virtual environments:** isolate dependencies per project
- **Imports:** `sys.path` search order; packages need `__init__.py` (or namespace packages)
- **Debugging:** `python -m pdb script.py` or breakpoints
- **Ecosystem lanes:** web ([[ASGI]]), data ([[pandas]]), packaging ([[wheel]])


- **Core:** Python source compiles to bytecode executed by a virtual machine (usually CPy…

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

- Useful stdlib modules in interviews: `asyncio`, `concurrent.futures`, `pathli…

| Symptom | Check | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` | `sys.path` / venv active? | Install into the environment; fix package layout |
| Wrong Python on PATH | `which python3` | Use venv or explicit version |
| IndentationError | mixed tabs/spaces | Keep one style; editor shows invisibles |

## Mistakes to Avoid
- **Mistake:** Using the distro `python` for project deps
- **Mistake:** Naming modules after stdlib (`email.py`, `random.py`)
- **Mistake:** Treating threads as multi-core CPU scaling

## Pros/Cons or Trade-offs
- **Pro:** Fast to write, huge libraries, readable for ops and ML alike.
- **Con:** CPU-bound threads limited by GIL; packaging and environment drift need discipline.

## Comparison
- vs Node.js: both excel at I/O-bound services
- vs Go/Java: those compile to heavier static binaries/services with different concurrency stories.


### Use cases
- Glue code on a jump host: venv + small script calling cloud APIs, debugged wi…
