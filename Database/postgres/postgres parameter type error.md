[[postgres/postgres Error]] [[postgres/psql essential]] [[connection pooling]] [[Prisma query]]

# PostgreSQL Error: `inconsistent types deduced for parameter $n`

> PostgreSQL inferred **different data types** for the **same placeholder (`$n`)** in one statement — fix by splitting placeholders or adding explicit casts.

---

## Mental model

**Say it in one breath:** PostgreSQL Error: `inconsistent types deduced for parameter $n` — I can explain the job, the config, and the top failure without jargon.


Prepared statements bind each `$n` to **one** PostgreSQL type for the whole query. The planner deduces that type from **every** occurrence of the placeholder. If `$2` appears once as `TEXT` and once as `INTEGER`, Postgres cannot pick a single type and raises this error.

```
$params ──► $2 used in SET status (text) ──┐
            $2 used in WHERE version (int) ─┴──► type conflict → ERROR
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **PostgreSQL Error: `inconsistent types deduced for parameter $n`** | This note’s core idea | “I explain PostgreSQL Error: `inconsistent types deduced for parameter $n` in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow | EXPLAIN / slow log | Index or rewrite |
| Auth/connect fail | pg_hba / users | Fix grants and bind |
| Bad migration | backup + version | Roll forward carefully |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[postgres/postgres Error]] [[postgres/psql essential]] [[connection pooling]] [[Prisma query]]
