[[TL;DR]] [[general]] [[DevOps/Jenkins]]

# Repro (reproduction case)

> Minimal steps that **reliably** show whether a bug still exists — the human executable test for triage and QA handoff.

## Mental model

A good repro removes ambiguity: **preconditions**, **steps**, **expected**, **actual**. If two engineers follow it and see different results, the repro isn't stable yet. Attach environment (OS, version, feature flags, data snapshot id).

```
Given → When → Then (plus environment pin)
```

## Standard repro template

```markdown
## Environment
- App v1.4.2, Chrome 125, prod-like staging, user role: admin

## Steps
1. Log in as admin@example.com
2. Open Settings → Billing
3. Click "Update card" with test Visa 4242…

## Expected
Toast "Card updated"; `/api/billing` returns 200

## Actual
500; response `{"error":"stripe_timeout"}`
```

## Quality bar

| Good | Bad |
|------|-----|
| Starts from clean/login state | "Sometimes breaks" |
| Names exact clicks/API | "Use the app normally" |
| Includes IDs/logs | Screenshot only |
| Works on fresh clone | Needs your local DB |

## Related

[[TL;DR]] [[general]] [[Github action]]
