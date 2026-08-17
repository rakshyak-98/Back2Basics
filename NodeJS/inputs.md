[[NodeJS]] [[CLI]] [[Stream]] [[REPL]] [[node command]]

# Node.js stdin / readline inputs

> Node.js stdin / readline inputs — CLI tools get input from process.stdin (readable stream) and write to process.stdout. The readline module provides an Interface that emits

```txt
        Node.js stdin / re ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Node.js stdin / readline inputs** to see if you understa…

## Sources
- [Node.js — Readline](https://nodejs.org/api/readline.html) — deep-dive
- [Wikipedia — inputs](https://en.wikipedia.org/wiki/inputs) — overview

## Key Concepts
- **CLI tools:** CLI tools get input from **`process.stdin`** (readable stream) and write to *…
- **For password:** For password input, use `readline` with muted output or a dedicated package


- **Core:** CLI tools get input from **`process.stdin`** (readable stream) and write to *…

## Technical Details
- CLI tools get input from **`process.stdin`** (readable stream) and write to *…
- The `readline` module provides an **Interface** that emits `'line'` events fo…

```
Keyboard / pipe ──► stdin ──► readline Interface ──► 'line' event ──► handler
                              │
prompt ───────────────────────┴──► stdout
```

- For password input, use `readline` with muted output or a dedicated package.
- For one-shot arguments, prefer `process.argv` or a CLI parser (`commander`, `…

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

## Mistakes to Avoid
- **Mistake:** **Partial lines on raw `data` events**
- **Mistake:** **Logging while prompting**
- **Mistake:** **CI/non-interactive**
- **Mistake:** **Prompt never appears:** check stdin not TTY
- **Mistake:** **Double echo:** check Raw mode + readline
- **Mistake:** **Script hangs at end:** check Interface not closed
- **Mistake:** **Broken pipes:** check Piped to `head`
- **Mistake:** **Unicode garbled:** check Encoding
- **Mistake:** **`ReferenceError: stdir`:** check Typo

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node.js stdin / readline inputs — CLI tools get input from process.stdin (readab…).
- **Con / when not:** **HTTP/API input**
- **Con / when not:** **Binary stdin**
- **Con / when not:** **Complex CLI**

## Comparison
- vs [[CLI]]: know when each applies


### Use cases
- In production APIs and tooling, **inputs** shows up whenever teams ship Node/…
- `; **Logging while prompting**
