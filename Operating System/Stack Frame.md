[[Stack trace]] [[stack pointer]] [[context switching]] [[system call]]

# Stack frame

> One activation record per function call — holds return address, saved registers, locals, and spill slots on the process stack.

---

## Mental model

Each time a function is **called**, the CPU pushes a **stack frame** (activation record) onto the thread's stack. Each **return** pops it. Nested calls nest frames:

```txt
high addresses
┌──────────────────┐
│ main() frame     │  return to _start
├──────────────────┤
│ foo() frame      │  return to main+offset
├──────────────────┤
│ bar() frame      │  locals, saved rbp  ◄── stack pointer (rsp/esp)
└──────────────────┘
low addresses (stack grows down on x86-64)
```

Typical frame contents (ABI-dependent):
- **Return address** — where to jump after `ret`
- **Saved frame pointer** — link to caller frame (enables stack unwinding)
- **Local variables** and compiler temporaries
- **Outgoing argument space** for calls this function makes

**Stack overflow** happens when recursion or huge locals exceed the mapped stack region — SIGSEGV, not a catchable exception in C.

**Service impact:** deep recursion in parsers, JSON decoders, or ORMs → crash under adversarial input; stack traces in logs map 1:1 to these frames.

---

## Standard config / commands

### Capture stack frames (live)

```bash
# All thread backtraces for PID
gdb -batch -ex "thread apply all bt" -p PID

# Lightweight sampler
perf record -g -p PID -- sleep 5 && perf report

# Node/V8
node --inspect-brk app.js   # then Chrome DevTools → Call Stack
kill -USR1 PID              # Node: triggers debug dump if enabled
```

### Stack size limits

```bash
ulimit -s          # KB per thread (default often 8192 = 8 MiB on Linux)
cat /proc/PID/maps | grep stack
```

```c
// pthread: explicit stack size for deep-recursion workers
pthread_attr_t attr;
pthread_attr_init(&attr);
pthread_attr_setstacksize(&attr, 4 * 1024 * 1024);
```

**Why:** default 8 MiB × 10k threads = address-space pressure even if stacks aren't fully used (guard pages help, but not unlimited).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `SIGSEGV` near stack top | `ulimit -s`; recursion depth | Increase stack limit; rewrite to iterative; tail-call where safe |
| Garbage stack traces | `-fomit-frame-pointer` builds | Rebuild with `-fno-omit-frame-pointer`; use `perf`/`eBPF` |
| Stack clash / overlap with heap | ASLR off, huge stack alloca | Fix bug; enable ASLR; audit `alloca` / VLA |
| Coroutine/green-thread weirdness | Mixed native + interpreted stacks | Ensure each fiber has its own stack region |

---

## Gotchas

> [!WARNING]
> **Optimized builds omit frame pointers** — `bt` in gdb shows `???`. Always keep frame pointers for production services you profile.

> [!WARNING]
> **`async/` stack traces show await boundaries**, not native frames — use `--async-stack-traces` (Node) or language-specific profilers.

> [!WARNING]
> **Stack is per-thread.** Global variables live elsewhere; only locals and call chain are in the frame.

---

## When NOT to use

Do not hand-roll stack switching unless building a runtime (coroutines, VMs). Use language/runtime support — incorrect stack alignment or red-zone violations cause silent corruption.

---

## Related

[[Stack trace]] [[stack pointer]] [[context switching]] [[Thread]] [[Heap memory]]
