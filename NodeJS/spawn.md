[[NodeJS]] [[child process]] [[fork]] [[CLI]] [[Node.js run as a non-privileged user]]

# spawn

> run an external binary with piped stdio — no shell by default; use for ffmpeg, git, openssl, and other CLI tools from Node.

## Interview Relevance

Interviewers probe **spawn** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Node.js — child_process.spawn](https://nodejs.org/api/child_process.html#child_processspawncommand-args-options) — deep-dive
- [Wikipedia — spawn](https://en.wikipedia.org/wiki/spawn) — overview

## Core Definition

`child_process.spawn(command, args[], options)` starts a **child process** and returns a `ChildProcess` with `.stdin`, `.stdout`, `.stderr` streams. Unlike `exec`, **no shell** is invoked unless `shell: true` — safer and faster for fixed binaries.

## Key Concepts

- `child_process.spawn(command, args[], options)` starts a **child process** and returns a `ChildProcess` with `.stdin`, `.stdout`, `.stderr` streams. Unlike `exec`, **no shell** …
- Use `spawn` for long-running or high-volume output. Use `exec`/`execFile` when you need buffered output in a callback (small output only).

## Technical Details

`child_process.spawn(command, args[], options)` starts a **child process** and returns a `ChildProcess` with `.stdin`, `.stdout`, `.stderr` streams. Unlike `exec`, **no shell** is invoked unless `shell: true` — safer and faster for fixed binaries.

```
Node parent                    Child process
    │                              │
    ├── spawn('git', ['status']) ─►│ git binary
    │◄── stdout stream ──────────│
    │──► stdin (optional) ───────►│
    └── 'close' event (exit code) ◄│
```

Use `spawn` for long-running or high-volume output. Use `exec`/`execFile` when you need buffered output in a callback (small output only).

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

## Real-World Applications

In production APIs and tooling, **spawn** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Unread pipes deadlock** — if stdout buffer fills (~64KB default), child blocks. Always consume or `'ignore'`; **`shell: true` + user input = injection** — same class of bug as SQL injection.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (run an external binary with piped stdio — no shell by default; use for ffmpeg, g…).
- **Con / when not:** **Run another Node script with IPC** — use [[fork]] for built-in message channel.
- **Con / when not:** **Tiny one-liner, small output** — `execFile` is simpler.
- **Con / when not:** **CPU work in-process** — use [[worker threads]], not shelling out.

## Comparison

vs [[child process]]: know when each applies — do not treat them as interchangeable. vs [[fork]]: `spawn` runs any executable; `fork` is Node-only with built-in IPC. vs [[CLI]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Unread pipes deadlock** — if stdout buffer fills (~64KB default), child blocks. Always consume or `'ignore'`.
- **`shell: true` + user input = injection** — same class of bug as SQL injection.
- **Windows vs Unix** — `.cmd`/`.bat` need shell or `execFile` with `shell: true` on Windows.
- **`ENOENT`:** check Binary not in PATH; fix: Absolute path; set `env.PATH` in spawn options
- **Hangs forever:** check Child waits for stdin; fix: `stdio: 'ignore'` or close stdin
- **Buffer fills; process stalls:** check stdout not consumed; fix: Pipe and drain stdout/stderr
- **Shell injection:** check User input in command string; fix: Use arg array; never `shell: true` with user input
- **Zombie children:** check No `close` handler; fix: Always listen `close`; `child.unref()` if intentional daemon
- **Exit code null + signal:** check Killed by SIGKILL/OOM; fix: Check dmesg/cgroups
