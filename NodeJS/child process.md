[[NodeJS]] [[worker]] [[clustering]] [[Node events driven]] [[Runtime Errors]]

# child process

> Spawn another OS process from Node — shell out, run binaries, or isolate crashable work. Mind shell injection.





## Interview Relevance
Interviewers use **child process** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **exec**, **spawn**, **fork**.

## Sources
- [Node.js — Child process](https://nodejs.org/api/child_process.html) — deep-dive
- [Wikipedia — child process](https://en.wikipedia.org/wiki/child_process) — overview

## Key Concepts
- **exec:** Shell + buffered output — Pipes/`&&` work; injection risk.
- **spawn:** Streaming stdio — Long-running / large output.
- **fork:** Node + `process.send` — IPC channel built in.

## Technical Details
```txt
parent ──spawn──► child (separate memory)
         IPC / stdout / exit code
```

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

## Real-World Applications
In production APIs and tooling, **child process** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`exec(userInput)` is RCE** — never pass unsanitized input to a shell; **Windows vs POSIX** — shells and signals differ; prefer `execFile` for portability.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Spawn another OS process from Node — shell out, run binaries, or isolate crashab…).
- **Con / when not:** **CPU parallelism inside one application** — [[worker]] threads share memory differently.
- **Con / when not:** **Tiny sync helpers** — maybe just a library call, not a process.

## Comparison
vs [[worker]]: know when each applies — do not treat them as interchangeable. vs [[clustering]]: know when each applies — do not treat them as interchangeable. vs [[Node events driven]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`exec(userInput)` is RCE** — never pass unsanitized input to a shell.
- **Windows vs POSIX** — shells and signals differ; prefer `execFile` for portability.
- **Shell injection:** check User string in `exec`; fix: `execFile` + fixed argv
- **`maxBuffer` exceeded:** check Large output via exec; fix: `spawn` and stream
- **Zombie / hang:** check Not consuming stdio; fix: Drain or `stdio: 'ignore'`
- **ENOENT:** check PATH / wrong binary; fix: Absolute path; check `env`
