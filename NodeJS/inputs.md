[[NodeJS]] [[CLI]] [[Stream]] [[REPL]] [[node command]]

# Node.js stdin / readline inputs

> Node.js stdin / readline inputs — CLI tools get input from process.stdin (readable stream) and write to process.stdout. The readline module provides an Interface that emits

## Interview Relevance

Interviewers probe **Node.js stdin / readline inputs** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Node.js — Readline](https://nodejs.org/api/readline.html) — deep-dive
- [Wikipedia — inputs](https://en.wikipedia.org/wiki/inputs) — overview

## Core Definition

CLI tools get input from **`process.stdin`** (readable stream) and write to **`process.stdout`**. The `readline` module provides an **Interface** that emits `'line'` events for each newline-terminated chunk — no manual buffering.

## Key Concepts

- CLI tools get input from **`process.stdin`** (readable stream) and write to **`process.stdout`**. The `readline` module provides an **Interface** that emits `'line'` events for …
- For password input, use `readline` with muted output or a dedicated package. For one-shot arguments, prefer `process.argv` or a CLI parser (`commander`, `yargs`) over interactiv…

## Technical Details

CLI tools get input from **`process.stdin`** (readable stream) and write to **`process.stdout`**. The `readline` module provides an **Interface** that emits `'line'` events for each newline-terminated chunk — no manual buffering.

```
Keyboard / pipe ──► stdin ──► readline Interface ──► 'line' event ──► handler
                              │
prompt ───────────────────────┴──► stdout
```

For password input, use `readline` with muted output or a dedicated package. For one-shot arguments, prefer `process.argv` or a CLI parser (`commander`, `yargs`) over interactive prompts in scripts.

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

## Real-World Applications

In production APIs and tooling, **inputs** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Partial lines on raw `data` events** — lines can split across chunks; use readline or buffer until `
`; **Logging while prompting** — concurrent `console.log` corrupts prompt; pause interface or serialize output.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Node.js stdin / readline inputs — CLI tools get input from process.stdin (readab…).
- **Con / when not:** **HTTP/API input** — use request body parsers, not readline.
- **Con / when not:** **Binary stdin** — use stream `read()` without UTF-8 encoding.
- **Con / when not:** **Complex CLI** — use `commander`/`yargs` for flags/subcommands.

## Comparison

vs [[CLI]]: know when each applies — do not treat them as interchangeable. vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[REPL]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Partial lines on raw `data` events** — lines can split across chunks; use readline or buffer until `\n`.
- **Logging while prompting** — concurrent `console.log` corrupts prompt; pause interface or serialize output.
- **CI/non-interactive** — always provide env/flag bypass for automation.
- **Prompt never appears:** check stdin not TTY; fix: Check `process.stdin.isTTY`; support argv fallback
- **Double echo:** check Raw mode + readline; fix: Don't mix; pick one API
- **Script hangs at end:** check Interface not closed; fix: `rl.close()` in finally
- **Broken pipes:** check Piped to `head`; fix: Ignore `EPIPE` on stdout
- **Unicode garbled:** check Encoding; fix: `setEncoding('utf8')` on stdin
- **`ReferenceError: stdir`:** check Typo; fix: Use `stdin`, not `stdir`
