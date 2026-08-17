[[Linux/Scripting]] [[NodeJS/node command]] [[NodeJS/CLI]] [[javascript]]

# HashBang comment (`#!`)

> First-line interpreter hint for Unix shells — stripped by the JS engine, meaningful only to the OS launcher — **POSIX + Node shebang practice**.

```txt
        HashBang comment ( ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Hashbang in JS modules is niche

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** `#!` (hash-bang) at **byte 0, line 1** tells the kernel which program execute…

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

## Technical Details
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

- Ensure built file retains shebang; bundlers may need `banner` plugin.

### TypeScript source (run compiled output)

- Shebang belongs on ** emitted** `.js`, not usually on `.ts` unless ts-node/es…

## Mistakes to Avoid
> [!WARNING]
> Shebang line length is limited (~128 bytes on Linux) — use `/usr/bin/env node`, not long absolute paths, when possible.

- **Mistake:** **Only one argument** historically on some systems
- **Mistake:** **Windows:** shebang ignored unless WSL/Git Bash
- **Mistake:** **ES modules:** shebang + `"type":"module"` in package.json is f…

| Symptom | Check | Fix |
|---------|-------|-----|
| `bad interpreter: No such file` | Windows CRLF broke shebang | `dos2unix script.js`; shebang must be first bytes |
| `./script: Permission denied` | Not executable | `chmod +x` |
| Wrong Node version | `which node` vs shebang path | Use `env node` + nvm default |
| Shebang not first line | BOM or blank line before `#!` | Move to line 1; remove BOM |
| Works with `node x` not `./x` | Missing shebang or exec bit | Add both |

## Pros/Cons or Trade-offs
- Files only ever imported, never executed directly.
- Browser bundles — bundler strips or breaks shebang if misplaced.
