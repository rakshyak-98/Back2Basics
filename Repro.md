[[TL;DR]] [[general]] [[DevOps/Jenkins]] [[Code review]] [[Release cycle]]

# Repro

> Repro — the minimal steps that reliably show whether a bug still exists; the human-executable test for triage and QA handoff.

```txt
        Repro ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Strong engineers turn “it broke once” into a stable reproduction

## Sources
- [Google Testing Blog — Flaky tests](https://testing.googleblog.com/) — overview (stability mindset)
- [Wikipedia — Bug report](https://en.wikipedia.org/wiki/Bug_report) — overview

## Key Concepts
- **Preconditions:** Accounts, feature flags, data IDs, time/locale.
- **Environment pin:** OS, app version, browser, commit SHA, config.
- **Expected vs actual:** Both required; “wrong” alone is useless.
- **Minimal:** Strip unrelated steps until failure still happens.
- **Stability:** Prefer 10/10 failures over “sometimes.”


- **Core:** A reproduction case is a short, deterministic procedure: given known precondi…

## Technical Details
```txt
Given → When → Then (+ environment pin)
```

```txt
Env: OS / app version / commit / flags
Data: user id / fixture / snapshot id
Steps:
  1. …
  2. …
Expected: …
Actual: …
Artifacts: logs, screenshot, HAR, metrics link
```

- Automate once stable: unit/integration test or CI job ([[DevOps/Jenkins]]).

## Mistakes to Avoid
- **Mistake:** “Works on my machine” without environment pins
- **Mistake:** Steps that require secret tribal clicks not written down
- **Mistake:** Marking fixed without re-running the original repro
- **Mistake:** Huge data dumps instead of a minimal fixture

## Pros/Cons or Trade-offs
- **Pro:** Cuts mean-time-to-diagnosis; enables parallel debugging.
- **Con:** Some bugs are timing/load dependent — invest in stress or race-detector repros instead of giving up.

## Comparison
- vs stack trace alone: traces show *where*


### Use cases
- Handoff to QA or another team: attach the repro in the ticket before debate
