<!-- note-strategy: operational -->
[[Operating System]] [[Stack Frame]] [[stack pointer]] [[gdb]] [[NodeJS]]

# Stack trace

> A stack trace is the chain of call frames at a moment in time — read top-down to find where you blew up, then who called it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Each function call pushes a frame; the trace prints those frames from the fault site up to `main` (or the thread start).

```txt
TOP    at myCode (app.js:42)          ← start here — your bug usually
       at handler (router.js:10)
       at Module._compile (node:…)    ← runtime / framework
BOTTOM at runMain (node:…)            ← process entry
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Frame** | One active function’s locals + return addr | “Each line is a stack frame.” |
| **Top frame** | Innermost call / fault site | “I read the top first for the throw location.” |
| **Caller** | Frame below | “Walk down to see the call path.” |
| **Symbolication** | Map addresses → file:line | “Need debug symbols or source maps.” |
| **Async stack** | Logical chain across awaits | “Not always the same as the OS stack.” |
| **Core dump** | Frozen memory + stacks | “Post-mortem: `gdb` + `bt`.” |

### How the story goes (4 steps)

1. **Capture** — exception, abort, `SIGSEGV`, or debugger break.
2. **Unwind** — walk frame pointers / DWARF / language metadata.
3. **Symbolize** — resolve to function names and source lines.
4. **Interpret** — top = what failed; middle = application path; bottom = runtime boot.

---

## Standard config / commands

```bash
# Live process
gdb -p <pid>
(gdb) thread apply all bt

# Core file
gdb ./binary core
(gdb) bt full

# Linux quick stacks
cat /proc/<pid>/stack          # kernel stack of task
eu-stack -p <pid>              # elfutils

# Node
node --enable-source-maps app.js
# Error.stack; or --async-stack-traces (modern default-ish)

# Go
kill -QUIT <pid>               # stack dump to stderr / log
```

Example (Node) — **top frame is your code**:

```txt
at Object.<anonymous> (/home/…/script.cjs:19:9)     ← look here first
at Module._compile (node:internal/modules/cjs/loader:…)
at Module.load (node:internal/modules/cjs/loader:…)
```

| Knob | Why it matters |
|------|----------------|
| `-g` / DWARF | Without symbols, `bt` is hex soup |
| Source maps | Minified JS/TS otherwise points at noise |
| Frame pointers (`-fno-omit-frame-pointer`) | Reliable unwind for profilers |
| `ulimit -c` | Allow core dumps when you need them |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Trace only shows `node:internal` | Error in eval / missing source map | Maps on; log your frame |
| Truncated stack | Depth limit / async gap | Increase stackTraceLimit; async hooks |
| Different every time | Race | Capture under lock; ThreadSanitizer |
| No symbols in prod | Stripped binary | Keep debuginfo packages side-by-side |
| Hang, no exception | All-thread `bt` | Find who waits on whom |

---

## Gotchas

> [!WARNING]
> **Bottom frames are rarely the bug.** Don’t “fix” Node’s module loader — keep climbing until you hit *your* file.

> [!WARNING]
> **Optimized builds inline frames** — the line you see may be a neighbor; reproduce with `-O0` if confused.

> [!WARNING]
> **Async/await** — the OS stack at `await` is not the logical causal chain unless the runtime stitches it.

> [!WARNING]
> **Signal handlers / alternate stacks** — corrupt or incomplete traces if you printf-heavy inside a handler.

---

## When NOT to use

- **As the only production telemetry** — prefer structured errors + metrics; stacks are fat and PII-prone.
- **Hot path logging of full stacks** — allocation and unwind cost will hurt.
- **When you need allocation history** — use a heap profiler, not a stack trace alone.

---

## Related

[[Stack Frame]] [[stack pointer]] [[gdb]] [[How to manipulate memory directly]] [[multi-threaded]] [[Error status code]]
