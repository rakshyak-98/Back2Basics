[[TL;DR]] [[general]] [[DevOps/Jenkins]] [[Code review]] [[Release cycle]]

# Repro

> Repro — the minimal steps that reliably show whether a bug still exists; the human-executable test for triage and QA handoff.

## Interview Relevance
Strong engineers turn “it broke once” into a stable reproduction. Interview signal: preconditions, environment pins, expected vs actual — same discipline as writing tests.

## Sources
- [Google Testing Blog — Flaky tests](https://testing.googleblog.com/) — overview (stability mindset)
- [Wikipedia — Bug report](https://en.wikipedia.org/wiki/Bug_report) — overview

## Core Definition
A reproduction case is a short, deterministic procedure: given known preconditions, when you perform steps, then you observe a specific failure (or confirm a fix). If two engineers get different results, the repro is not done yet.

## Key Concepts
- **Preconditions:** Accounts, feature flags, data IDs, time/locale.
- **Environment pin:** OS, app version, browser, commit SHA, config.
- **Expected vs actual:** Both required; “wrong” alone is useless.
- **Minimal:** Strip unrelated steps until failure still happens.
- **Stability:** Prefer 10/10 failures over “sometimes.”

## Technical Details
```txt
Given → When → Then (+ environment pin)
```

Template:

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

Automate once stable: unit/integration test or CI job ([[DevOps/Jenkins]]).

## Real-World Applications
Handoff to QA or another team: attach the repro in the ticket before debate. Incident follow-up: convert the outage trigger into a regression test so [[Release cycle]] cannot silently revive it.

## Pros/Cons or Trade-offs
- **Pro:** Cuts mean-time-to-diagnosis; enables parallel debugging.
- **Con:** Some bugs are timing/load dependent — invest in stress or race-detector repros instead of giving up.

## Comparison
vs stack trace alone: traces show *where*; repro shows *how to get there*. vs [[TL;DR]]: TL;DR compresses communication; repro proves the defect. Related: [[Code review]] asks “how do we know this stays fixed?”

## Mistakes to Avoid
- “Works on my machine” without environment pins.
- Steps that require secret tribal clicks not written down.
- Marking fixed without re-running the original repro.
- Huge data dumps instead of a minimal fixture.
