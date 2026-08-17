[[NodeJS]] [[worker]] [[clustering]] [[Node events driven]] [[Runtime Errors]]

# child process

> Spawn another OS process from Node — shell out, run binaries, or isolate crashable work. Mind shell injection.

```txt
        child process ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **child process** to check whether you can explain the mecha…

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

## Mistakes to Avoid
- **Mistake:** **`exec(userInput)` is RCE**
- **Mistake:** **Windows vs POSIX**
- **Mistake:** **Shell injection:** check User string in `exec`
- **Mistake:** **`maxBuffer` exceeded:** check Large output via exec
- **Mistake:** **Zombie / hang:** check Not consuming stdio
- **Mistake:** **ENOENT:** check PATH / wrong binary

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Spawn another OS process from Node — shell out, run binaries, or isolate crashab…).
- **Con / when not:** **CPU parallelism inside one application**
- **Con / when not:** **Tiny sync helpers**

## Comparison
- vs [[worker]]: know when each applies


### Use cases
- In production APIs and tooling, **child process** shows up whenever teams shi…
