[[NodeJS]] [[CLI]] [[Stream]]

# Node.js stdin / readline inputs

> Node.js stdin / readline inputs — CLI tools get input from process.stdin (readable stream) and write to process.stdout. The readline module provides an Interface that emits

---

## How it works

CLI tools get input from **`process.stdin`** (readable stream) and write to **`process.stdout`**. The `readline` module provides an **Interface** that emits `'line'` events for each newline-terminated chunk — no manual buffering.

```
Keyboard / pipe ──► stdin ──► readline Interface ──► 'line' event ──► handler
                              │
prompt ───────────────────────┴──► stdout
```

For password input, use `readline` with muted output or a dedicated package. For one-shot arguments, prefer `process.argv` or a CLI parser (`commander`, `yargs`) over interactive prompts in scripts.


## Configuration and commands

### Basic prompt loop

```javascript
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

const rl = readline.createInterface({ input, output });

try {
  const name = await rl.question('Name? ');
  console.log(`Hello, ${name}`);
} finally {
  rl.close();
}
```

### Callback style (legacy)

```javascript
import readline from 'node:readline';
import { stdin, stdout } from 'node:process';

const rl = readline.createInterface({ input: stdin, output: stdout });

rl.on('line', (line) => {
  if (line === 'quit') rl.close();
  else console.log(`You said: ${line}`);
});

rl.on('close', () => process.exit(0));
```

### Read from piped input (non-TTY)

```bash
echo "line1\nline2" | node script.js
```

```javascript
// readline works on piped stdin — no prompt needed
for await (const line of rl) {
  processLine(line);
}
```

### Handle Ctrl+C

```javascript
rl.on('SIGINT', () => {
  rl.close();
  process.exit(130);
});
```

### Raw stdin (without readline)

```javascript
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { /* chunk may be partial line */ });
```


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Prompt never appears | stdin not TTY | Check `process.stdin.isTTY`; support argv fallback |
| Double echo | Raw mode + readline | Don't mix; pick one API |
| Script hangs at end | Interface not closed | `rl.close()` in finally |
| Broken pipes | Piped to `head` | Ignore `EPIPE` on stdout |
| Unicode garbled | Encoding | `setEncoding('utf8')` on stdin |
| `ReferenceError: stdir` | Typo | Use `stdin`, not `stdir` |


## Gotchas

> [!WARNING]
> **Partial lines on raw `data` events** — lines can split across chunks; use readline or buffer until `\n`.

> [!WARNING]
> **Logging while prompting** — concurrent `console.log` corrupts prompt; pause interface or serialize output.

> [!WARNING]
> **CI/non-interactive** — always provide env/flag bypass for automation.


## When not to use

- **HTTP/API input** — use request body parsers, not readline.
- **Binary stdin** — use stream `read()` without UTF-8 encoding.
- **Complex CLI** — use `commander`/`yargs` for flags/subcommands.


## Related

[[CLI]] [[REPL]] [[Stream]] [[node command]]

## Sources

- [Wikipedia — inputs](https://en.wikipedia.org/wiki/inputs)
