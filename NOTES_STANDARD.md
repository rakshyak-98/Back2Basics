[[NOTETAKING_STRATEGIES]] [[NOTES_STANDARD.md]]

# Notes Standard — Staff Engineer Field Notes

> How to write notes in this vault — retrieve fast, debug fast, configure correctly.

**Before writing:** pick a strategy from [[NOTETAKING_STRATEGIES]], set `<!-- note-strategy: <id> -->` on line 1, then fill the matching template below.

---

## Mental model

**Say it in one breath:** Each note names one real process (install, configure, debug, or decide) in words that match what actually happens on the machine or in the service — using the section shape that fits the reader's job.

### Writing rules (all strategies)

| Rule | Do | Do not |
|------|-----|--------|
| **Full words** | Write "authentication", "configuration", "environment", "production" | Casual shortenings: auth, config, env, prod, repo, creds |
| **Name the process** | "The kernel holds sockets in TIME-WAIT for two minutes after TCP close" | Hidden meaning: "TIME-WAIT storms" without saying what TIME-WAIT is |
| **One breath summary** | Restate the one-line summary as a complete sentence about the real steps | Generic filler: "infra/security tooling — least privilege" |
| **Triage rows** | Symptom → command or log to run → exact fix for **this** topic | Copy-paste Auth/TLS/Deploy rows unrelated to the note |
| **Abbreviations in tables** | Spell out in the "Plain meaning" column: "ESTABLISHED (fully open TCP connection)" | Leave kernel or protocol shorthand unexplained |
| **Commands** | Keep flags and tool names literal (`git diff`, `ss -luntp`) | Expand command names inside code blocks |
| **Strategy tag** | `<!-- note-strategy: operational -->` on line 1 when creating or restructuring | Mixing runbook steps into a reference card layout |

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **mental model** | One sentence that names the real objects and steps | "Explain what runs, what it reads, what it writes." |
| **failure mode** | The first observable signal that something broke | "Say what you check first — logs, metrics, or a command." |
| **triage table** | Symptom → check → fix for this topic only | "Each row is a playbook step I have run before." |

---

## Strategy templates

Copy the block for your strategy. Replace `…` placeholders; delete unused subsections.

### Operational Field Note (`operational`) — default

```markdown
<!-- note-strategy: operational -->
[[ParentTopic]]

# Title

> One breath: what runs, on what wire, and what breaks first.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** …

```txt
(optional ASCII diagram — actors, data flow, failure domain)
```

### Interview map (optional)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| … | … | … |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working versus broken environment
```

| Setting / flag | Why |
|----------------|-----|
| … | … |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs and software versions | Reproduce with the smallest input that shows the bug |
| Works on one machine only | environment differences | Compare configuration files and versions |
| Silent failure | logs and metrics | Add checks at the step that should have produced output |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview — spell out abbreviations the first time they appear in prose.

---

## When NOT to use

- Skip when a simpler existing tool already fits.

---

## Related

[[Sibling]] · [[Tool]]
```

---

### Reference Card (`reference`)

```markdown
<!-- note-strategy: reference -->
[[ParentTopic]]

# Title

> One breath: what this command surface is for.

---

## Index

- [[#Quick reference]]
- [[#Common commands]]
- [[#Options / flags]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

---

## Common commands

```bash
# most-used invocations — copy-paste ready
```

---

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

---

## Examples

```bash
# scenario: …
```

---

## Related

[[Operational note for debugging]] · [[Sibling]]
```

---

### Concept Note (`concept`)

```markdown
<!-- note-strategy: concept -->
[[ParentTopic]]

# Title

> One breath: the idea in plain language.

---

## Index

- [[#Mental model]]
- [[#Core idea]]
- [[#Variations / implementations]]
- [[#Trade-offs]]
- [[#When to use / When NOT]]
- [[#Related]]

## Mental model

**Say it in one breath:** …

---

## Core idea

- …

---

## Variations / implementations

```language
// minimal sketch showing the mechanism
```

---

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

---

## When to use / When NOT

**Use when:** …

**Avoid when:** …

---

## Related

[[Operational note]] · [[Comparison note]]
```

---

### Comparison Note (`comparison`)

```markdown
<!-- note-strategy: comparison -->
[[ParentTopic]]

# Title A vs Title B

> One breath: what decision this comparison unlocks.

---

## Index

- [[#Decision context]]
- [[#Comparison matrix]]
- [[#Selection guide]]
- [[#Per-option gotchas]]
- [[#Related]]

## Decision context

- Constraints: …
- Non-goals: …

---

## Comparison matrix

| Criterion | Option A | Option B |
|-----------|----------|----------|
| … | … | … |

---

## Selection guide

- Choose **A** when …
- Choose **B** when …

---

## Per-option gotchas

### Option A

> [!WARNING]
> …

### Option B

> [!WARNING]
> …

---

## Related

[[Operational note A]] · [[Operational note B]]
```

---

### Runbook (`runbook`)

```markdown
<!-- note-strategy: runbook -->
[[ParentTopic]]

# Title — recovery

> One breath: what incident this runbook addresses.

---

## Index

- [[#Trigger / symptoms]]
- [[#Preconditions]]
- [[#Steps]]
- [[#Verification]]
- [[#Rollback]]
- [[#Escalation]]
- [[#Related]]

## Trigger / symptoms

- …

---

## Preconditions

- Access: …
- Maintenance window: …

---

## Steps

1. …
2. …
3. …

---

## Verification

```bash
# command or check that proves recovery
```

---

## Rollback

1. …

---

## Escalation

- If … then contact … / open …

---

## Related

[[Operational note]] · [[INDEX]]
```

---

### Procedure Note (`procedure`)

```markdown
<!-- note-strategy: procedure -->
[[ParentTopic]]

# Title — setup

> One breath: what gets installed or bootstrapped.

---

## Index

- [[#Prerequisites]]
- [[#Steps]]
- [[#Verification]]
- [[#Troubleshooting]]
- [[#Related]]

## Prerequisites

- OS / versions: …
- Credentials: …

---

## Steps

1. …
2. …
3. …

---

## Verification

```bash
# smoke test
```

---

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

→ Deep debug: [[Operational note]]

---

## Related

[[Operational note]] · [[Sibling setup]]
```

---

### Hub / Map of Content (`hub`)

```markdown
<!-- note-strategy: hub -->
[[ParentTopic]]

# Domain hub title

> One breath: what this index routes to.

---

## Index

- [[#Purpose]]
- [[#Routing table]]
- [[#Domain links]]
- [[#Related]]

## Purpose

…

---

## Routing table

| Symptom / need | Go to |
|----------------|-------|
| … | [[Note]] |

---

## Domain links

- Sub-area: [[Note]] · [[Note]]

---

## Related

[[INDEX]] · [[NOTES_STANDARD]] · [[NOTETAKING_STRATEGIES]]
```

---

### Decision Record (`decision`)

```markdown
<!-- note-strategy: decision -->
[[ParentTopic]]

# Title — decision

> One breath: what we decided and the main constraint.

---

## Index

- [[#Context]]
- [[#Decision]]
- [[#Consequences]]
- [[#Alternatives considered]]
- [[#Related]]

## Context

- Problem: …
- Constraints: …
- Date / status: …

---

## Decision

We will … because …

---

## Consequences

**Positive:** …

**Negative / trade-offs:** …

---

## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |

---

## Related

[[Operational notes affected]] · [[Comparison note]]
```

---

## Triage (when things break)

Use this table only in **Operational**, **Procedure**, or **Runbook** notes when you have not yet filled topic-specific rows:

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs and software versions | Reproduce with the smallest input that shows the bug |
| Works on one machine only | environment differences between machines | Compare configuration files and software versions |
| Silent failure | logs and metrics | Add checks and alerts at the step that should have produced output |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview — spell out abbreviations the first time they appear in prose.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.
- Skip the wrong strategy — see [[NOTETAKING_STRATEGIES#Decision tree]].

---

## Related

[[NOTETAKING_STRATEGIES]] · [[INDEX]] · [[README]]
