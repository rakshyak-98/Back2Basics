[[Operating System]] [[linker]] [[runtime]] [[Runtime Environment]]

# Interpreter

> Runs program source (or bytecode) by executing it now — no separate ahead-of-time machine binary required.

---

## Mental model

**Say it in one breath:** Parse or load code → walk AST / bytecode → dispatch operations; JIT may later compile hot paths to machine code.

```txt
source ──► parse/AST ──► bytecode ──► interpret loop
                              │
                              └──► JIT (optional) ──► native
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Interpret** | Execute without AOT binary | “VM reads ops and runs them.” |
| **Bytecode** | Compact portable ops | “Compile once to bytecode; run anywhere with a VM.” |
| **AST walk** | Tree-driven eval | “Simple languages eval the parse tree.” |
| **JIT** | Compile hot code at runtime | “Pay compile cost when a loop is hot.” |
| **VM** | Runtime that hosts bytecode | “JVM / CPython / V8 are VMs.” |
| **FFI** | Call native libs | “Escape to C when the interpreter is too slow.” |

### How the story goes

1. **Load** — source or precompiled bytecode.
2. **Prepare** — parse, optionally compile to bytecode; drop AST if unused.
3. **Dispatch** — loop: fetch op → execute → next.
4. **Optimize** — profiling + JIT / inline caches (JS, JVM, etc.).

---

## Standard config / commands

```bash
python -c 'print(1)'          # CPython interpret
python -m dis demo.py         # show bytecode
node --print-bytecode app.js  # V8 (flag varies by version)
java -XX:+PrintCompilation    # HotSpot JIT activity
```

| Knob | Why it matters |
|------|----------------|
| `-O` / optimize flags | Fewer checks, different perf |
| JIT on/off | Cold start vs peak throughput |
| Bytecode cache (`.pyc`) | Skip reparse |
| Worker / isolate | Parallel interpret without sharing heap |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow loops | Profiler / `dis` / bytecode | Algorithm; Cython/Rust; enable JIT |
| High RSS after load | AST kept + bytecode + JIT code | Stream modules; limit caches |
| “Works in REPL, fails packaged” | Missing bytecode / zipimport | Ship correct runtime + deps |
| Version skew | Language minor version | Pin runtime in images |
| Native crash in extension | FFI / GIL misuse | Isolate native bugs from VM |
| Startup latency | Cold JIT / import graph | Lazy import; AOT where available |

---

## Gotchas

> [!WARNING]
> **Interpreted ≠ always slower forever** — JITs beat naive C in some hot paths; measure.

> [!WARNING]
> **Bytecode is not encryption** — ship source-equivalent; don’t put secrets in client bundles.

> [!WARNING]
> **GIL / single-thread VM** — CPU parallelism needs processes or native threads outside the lock ([[CPU IO Bound Task]]).

> [!WARNING]
> **Eval is a security hole** — treating user strings as code is RCE.

---

## When NOT to use

- **Hard realtime / tiny MCU** — prefer compiled firmware.
- **Ship one static binary with no runtime** — Go/Rust AOT style.
- **Max cold-start on edge** — AOT or wasm with pre-initialize; avoid huge JIT warmups.

---

## Related

[[linker]] [[runtime]] [[Runtime Environment]] [[opcode]] [[assembly language]] [[OS program]]
