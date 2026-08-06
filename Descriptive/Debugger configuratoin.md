[[Descriptive]]

# Debugger configuratoin

> One-line: what / why for **Debugger configuratoin** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Next.js: debug server-side",
            "type": "node-terminal",
            "request": "launch",
            "command": "npm run dev"
        },
        {
            "name": "Next.js: debug client-side",
            "type": "chrome",
            "request": "launch",
            "url": "http://localhost:3000"
        },
        {
            "name": "Next.js: debug full stack",
            "type": "node-terminal",
            "request": "launch",
            "command": "npm run dev",
            "serverReadyAction": {
                "pattern": "started server on .+, url: (https?://.+)",
                "uriFormat": "%s",
                "action": "debugWithChrome"
            }
        },
		{
            "name": "Next.js: debug client-side (Firefox)",
            "type": "firefox",
            "request": "launch",
            "url": "http://localhost:3000",
            "webRoot": "${workspaceFolder}"
        }
    ]
}
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
