[[NodeJS]] [[child process]] [[fork]]

# spawn

> One-line: run an external binary with piped stdio — no shell by default; use for ffmpeg, git, openssl, and other CLI tools from Node.

## Mental model

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

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ENOENT` | Binary not in PATH | Absolute path; set `env.PATH` in spawn options |
| Hangs forever | Child waits for stdin | `stdio: 'ignore'` or close stdin |
| Buffer fills; process stalls | stdout not consumed | Pipe and drain stdout/stderr |
| Shell injection | User input in command string | Use arg array; never `shell: true` with user input |
| Zombie children | No `close` handler | Always listen `close`; `child.unref()` if intentional daemon |
| Exit code null + signal | Killed by SIGKILL/OOM | Check dmesg/cgroups |

## Gotchas

> [!WARNING]
> **Unread pipes deadlock** — if stdout buffer fills (~64KB default), child blocks. Always consume or `'ignore'`.

> [!WARNING]
> **`shell: true` + user input = injection** — same class of bug as SQL injection.

> [!WARNING]
> **Windows vs Unix** — `.cmd`/`.bat` need shell or `execFile` with `shell: true` on Windows.

## When NOT to use

- **Run another Node script with IPC** — use [[fork]] for built-in message channel.
- **Tiny one-liner, small output** — `execFile` is simpler.
- **CPU work in-process** — use [[worker threads]], not shelling out.

## Related

[[child process]] [[fork]] [[CLI]] [[Node.js run as a non-privileged user]]
