[[Linux/Scripting]] [[NodeJS/node command]] [[NodeJS/CLI]] [[javascript]]

# HashBang comment (`#!`)

> First-line interpreter hint for Unix shells — stripped by the JS engine, meaningful only to the OS launcher — **POSIX + Node shebang practice**.

## Mental model

`#!` (hash-bang) at **byte 0, line 1** tells the kernel which program executes the file when run as `./script.js`. The JavaScript engine treats it as a **single-line comment** and removes it before parse.

```
./cli.js  ──► kernel reads #!/usr/bin/env node
                    │
                    └── exec node with script path as argv[1]

node cli.js  ──► shebang ignored (node invoked directly)
```

| Runner | Shebang effect |
|--------|----------------|
| `./script` (executable + shebang) | OS picks interpreter |
| `node script.js` | Comment only |
| Import/require from another file | Comment only |

## Standard config / commands

### Node CLI script

```javascript
#!/usr/bin/env node
'use strict';

console.log('Hello world');
```

```bash
chmod +x cli.js
./cli.js
```

### Pin Node version (nvm/fnm layouts)

```javascript
#!/usr/bin/env node
// or explicit: #!/home/you/.nvm/versions/node/v20.10.0/bin/node
```

### npm `bin` entry (package.json)

```json
{
  "bin": {
    "mytool": "./dist/cli.js"
  }
}
```

Ensure built file retains shebang; bundlers may need `banner` plugin.

### TypeScript source (run compiled output)

Shebang belongs on ** emitted** `.js`, not usually on `.ts` unless ts-node/esbuild injects it.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `bad interpreter: No such file` | Windows CRLF broke shebang | `dos2unix script.js`; shebang must be first bytes |
| `./script: Permission denied` | Not executable | `chmod +x` |
| Wrong Node version | `which node` vs shebang path | Use `env node` + nvm default |
| Shebang not first line | BOM or blank line before `#!` | Move to line 1; remove BOM |
| Works with `node x` not `./x` | Missing shebang or exec bit | Add both |

## Gotchas

> [!WARNING]
> Shebang line length is limited (~128 bytes on Linux) — use `/usr/bin/env node`, not long absolute paths, when possible.

- **Only one argument** historically on some systems — `env node --experimental-vm-modules` may fail; use wrapper script.
- **Windows:** shebang ignored unless WSL/Git Bash; use `node script.js` in `.cmd` shims for npm bins.
- **ES modules:** shebang + `"type":"module"` in package.json is fine.

## When NOT to use

- Files only ever imported, never executed directly.
- Browser bundles — bundler strips or breaks shebang if misplaced.

## Related

[[NodeJS/node command]] [[NodeJS/CLI]] [[Linux/Scripting]] [[javascript]]
