[[NodeJS]] [[worker]] [[clustering]] [[Node events driven]]

# child process

> Spawn another OS process from Node — shell out, run binaries, or isolate crashable work. Mind shell injection.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Interview map (words you can say)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `exec` runs a shell command string (buffers output); `execFile`/`spawn` run a program with argv (safer); `fork` starts another Node process with IPC.

```txt
parent ──spawn──► child (separate memory)
         IPC / stdout / exit code
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **exec** | Shell + buffered output | “Pipes/`&&` work; injection risk.” |
| **spawn** | Streaming stdio | “Long-running / large output.” |
| **fork** | Node + `process.send` | “IPC channel built in.” |

## Standard config / commands

```js
import { execFile, spawn } from 'node:child_process'

execFile('ls', ['-l'], (err, stdout) => {
  if (err) throw err
  console.log(stdout)
})

const child = spawn('ffmpeg', ['-i', inFile, outFile], { stdio: 'inherit' })
child.on('exit', (code) => console.log('done', code))
```

| Knob | Why it matters |
|------|----------------|
| argv array | Avoids shell injection |
| `maxBuffer` (exec) | Prevent huge stdout OOM |
| `detached` / `unref` | Daemonize carefully |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Shell injection | User string in `exec` | `execFile` + fixed argv |
| `maxBuffer` exceeded | Large output via exec | `spawn` and stream |
| Zombie / hang | Not consuming stdio | Drain or `stdio: 'ignore'` |
| ENOENT | PATH / wrong binary | Absolute path; check `env` |

---

## Gotchas

> [!WARNING]
> **`exec(userInput)` is RCE** — never pass unsanitized input to a shell.

> [!WARNING]
> **Windows vs POSIX** — shells and signals differ; prefer `execFile` for portability.

---

## When NOT to use

- **CPU parallelism inside one app** — [[worker]] threads share memory differently.
- **Tiny sync helpers** — maybe just a library call, not a process.

---

## Related

[[worker]] [[clustering]] [[Runtime Errors]]
