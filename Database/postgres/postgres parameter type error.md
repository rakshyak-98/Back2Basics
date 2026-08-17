[[postgres Error]] [[psql essential]] [[SQL/postgres]] [[SQL error]]

# postgres parameter type error

> `could not determine data type of parameter $N` and related bind mismatches — fix with explicit casts or typed placeholders in prepared statements.

```txt
        postgres parameter ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows debugging skill with prepared statements and ORMs that send untyped `nu…

## Sources
- [PREPARE](https://www.postgresql.org/docs/current/sql-prepare.html) — deep-dive
- [Error code 42P18](https://www.postgresql.org/docs/current/errcodes-appendix.html) — overview

## Key Concepts
- **Type inference:** Planner must know parameter types; ambiguity fails fast.
- **Explicit casts:** `$1::text`, `$2::int`, `::timestamptz` remove guesswork.
- **ORM nulls:** JavaScript `null` often needs a type hint.
- **Related SQLSTATEs:** `42P18` indeterminate_datatype; `42804` datatype_mismatch.

## Technical Details
```sql
-- Ambiguous parameter in prepared statement
PREPARE p AS SELECT * FROM t WHERE col = $1 AND other = $1;
-- Fix: cast / separate params
PREPARE p AS SELECT * FROM t WHERE col = $1::text AND other = $2::int;
```

- Driver tips: enable prepared statements only when parameter types are stable

## Mistakes to Avoid
- **Mistake:** Reusing one unbound parameter for incompatible column types
- **Mistake:** Passing string dates without `timestamptz` context when sessions…
- **Mistake:** Catching the error and retrying the identical untyped query

## Pros/Cons or Trade-offs
- **Pro:** Strict typing prevents silent wrong-plan casts.
- **Con:** More verbose SQL than engines that guess more aggressively.
- **Trade-off:** Always-prepared statements vs simple text protocols for dynamic shapes.

## Comparison
- vs [[postgres Error]]: general error fields; this note is the bind/typing fai…


### Use cases
- Raw SQL in Node/Python services with optional filters
