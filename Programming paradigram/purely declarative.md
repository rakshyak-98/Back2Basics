[[Programming paradigram/Functional Programing]] [[Database/OLAP]] [[Descriptive/Mermaid (DSL)]]

# Purely declarative

> Describe **what** result you want; runtime chooses **how** — SQL, regex, HTML/CSS, Prolog-style rules.

## Mental model

Imperative: step-by-step mutations. Declarative: state the desired outcome or relation. Engine optimizes execution (query planner, layout engine, regex NFA). You trade control of execution order for brevity and optimization headroom — until you need hints (`INDEX`, `EXPLAIN`, CSS `!important`).

```
Imperative: loop rows, if age>30, append name
Declarative: SELECT name FROM users WHERE age > 30
```

## Standard config / commands

### SQL (canonical)

```sql
SELECT name, COUNT(*) AS orders
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.active = TRUE
GROUP BY name
HAVING COUNT(*) > 5;
```

### CSS (what layout should look like)

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
```

### Kubernetes desired state

```yaml
spec:
  replicas: 3   # declare count; controller reconciles
```

### When you need control

```sql
EXPLAIN ANALYZE SELECT ...;
-- force index hint only when planner wrong (vendor-specific)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow SQL | `EXPLAIN` | Indexes; rewrite joins; stats vacuum |
| Wrong CSS layout | DevTools box model | Change declarative props, not manual pixel nudge loops |
| K8s drift | `kubectl diff` | GitOps reconcile; fix manifest not pods by hand |
| Regex catastrophic backtrack | Pattern review | Possessive groups; RE2 engine |
| "Can't express logic" | Leaky abstraction | Escape to imperative UDF/script |

## Gotchas

> [!WARNING]
> **Pure declarative myth** — hints, pragmas, and `$where` re-introduce imperative.
>
> **SQL injection** — declarative strings still need parameterization.
>
> **CSS specificity wars** — declarative cascade fights predictability.

## When NOT to use

- Don't use declarative DSL for procedural algorithms (sort implementation) — use a general language.
- Don't SQL everything in app strings — ORM/query builder for structure + safety.

## Related

[[Programming paradigram/Functional Programing]] [[Database/OLAP]] [[Database/mysql/MySQL Events]]
