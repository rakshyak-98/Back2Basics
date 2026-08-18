[[NOTES_STANDARD.md]]

# Notes Standard — Staff Engineer Field Notes

> How to write notes in this vault — retrieve fast, debug fast, configure correctly.

## Mental model

**Say it in one breath:** Each note names one real process (install, configure, debug, or operate) in words that match what actually happens on the machine or in the service.

### Writing rules (plain language)

| Rule | Do | Do not |
| --- | --- | --- |
| **Full words** | Write "authentication", "configuration", "environment", "production" | Casual shortenings: auth, config, env, prod, repo, creds |
| **Name the process** | "The kernel holds sockets in TIME-WAIT for two minutes after TCP close" | Hidden meaning: "TIME-WAIT storms" without saying what TIME-WAIT is |
| **One breath summary** | Restate the one-line summary as a complete sentence about the real steps | Generic filler: "infra/security tooling — least privilege" |
| **Triage rows** | Symptom → command or log to run → exact fix for **this** topic | Copy-paste Auth/TLS/Deploy rows unrelated to the note |
| **Abbreviations in tables** | Spell out in the "Plain meaning" column: "ESTABLISHED (fully open TCP connection)" | Leave kernel or protocol shorthand unexplained |
| **Commands** | Keep flags and tool names literal (`git diff`, `ss -luntp`) | Expand command names inside code blocks |

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **mental model** | One sentence that names the real objects and steps | "Explain what runs, what it reads, what it writes." |
| --- | --- | --- |
| **failure mode** | The first observable signal that something broke | "Say what you check first — logs, metrics, or a command." |
| **triage table** | Symptom → check → fix for this topic only | "Each row is a playbook step I have run before." |

## Standard config / commands

```bash
# reproduce with minimal input
# compare working versus broken environment
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Unexpected result | inputs and software versions | Reproduce with the smallest input that shows the bug |
| Works on one machine only | environment differences between machines | Compare configuration files and software versions |
| Silent failure | logs and metrics | Add checks and alerts at the step that should have produced output |

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview — spell out abbreviations the first time they appear in prose.

## When NOT to use

- Skip it when a simpler existing tool already fits.

## Related

[[NOTES_STANDARD.md]]
