[[NodeJS]] [[child process]] [[fork]] [[NodeJS CLI]] [[Node.js run as a non-privileged user]]

# spawn

> run an external binary with piped stdio — no shell by default; use for ffmpeg, git, openssl, and other CLI tools from Node.

```txt
        spawn ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **spawn** to see if you understand what it does operationa…

## Sources
- [Node.js — child_process.spawn](https://nodejs.org/api/child_process.html#child_processspawncommand-args-options) — deep-dive
- [Wikipedia — spawn](https://en.wikipedia.org/wiki/spawn) — overview

## Key Concepts
- **`child_process.spawn(command, args[]:** `child_process.spawn(command, args[], options)` starts a **child process** an…
- **Use `spawn`:** Use `spawn` for long-running or high-volume output


- **Core:** `child_process.spawn(command, args[], options)` starts a **child process** an…

## Technical Details
- `child_process.spawn(command, args[], options)` starts a **child process** an…
- Unlike `exec`, **no shell** is invoked unless `shell: true`

```
Node parent                    Child process
    │                              │
    ├── spawn('git', ['status']) ─►│ git binary
    │◄── stdout stream ──────────│
    │──► stdin (optional) ───────►│
    └── 'close' event (exit code) ◄│
```

- Use `spawn` for long-running or high-volume output.
- Use `exec`/`execFile` when you need buffered output in a callback (small outp…

### Basic spawn

```javascript
import { spawn } from 'node:child_process';

const child = spawn('ls', ['-la'], { cwd: '/tmp' });

child.stdout.on('data', (data) => process.stdout.write(data));
child.stderr.on('data', (data) => process.stderr.write(data));

child.on('close', (code) => {
  if (code !== 0) console.error(` exited ${code}`);
});
```

### Promise wrapper (common pattern)

```javascript
import { spawn } from 'node:child_process';

function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { ...opts, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (d) => { stdout += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('error', reject);
    child.on('close', (code) => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(Object.assign(new Error(stderr || `exit ${code}`), { code, stdout, stderr }));
    });
  });
}

await run('openssl', ['version']);
```

### Shell when needed (careful)

```javascript
// Prefer explicit shell only when you need pipes/globs
spawn('echo hello | wc -l', { shell: true, stdio: 'inherit' });
```

### Environment and cwd

```javascript
spawn('node', ['app.js'], {
  env: { ...process.env, NODE_ENV: 'production' },
  cwd: '/app',
  detached: false,
});
```

### Kill tree on timeout

```javascript
const child = spawn('long-running-cmd', []);
const timer = setTimeout(() => {
  child.kill('SIGTERM');
}, 30_000);
child.on('close', () => clearTimeout(timer));
```

## Mistakes to Avoid
- **Mistake:** **Unread pipes deadlock**
- **Mistake:** **`shell: true` + user input = injection**
- **Mistake:** **Windows vs Unix**
- **Mistake:** **`ENOENT`:** check Binary not in PATH
- **Mistake:** **Hangs forever:** check Child waits for stdin
- **Mistake:** **Buffer fills
- **Mistake:** **Shell injection:** check User input in command string
- **Mistake:** **Zombie children:** check No `close` handler
- **Mistake:** **Exit code null + signal:** check Killed by SIGKILL/OOM

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (run an external binary with piped stdio — no shell by default; use for ffmpeg, g…).
- **Con / when not:** **Run another Node script with IPC**
- **Con / when not:** **Tiny one-liner, small output** — `execFile` is simpler.
- **Con / when not:** **CPU work in-process**

## Comparison
- vs [[child process]]: know when each applies


### Use cases
- In production APIs and tooling, **spawn** shows up whenever teams ship Node/J…
