[[database migration]] [[Database design]] [[mysql dump]]

# database seeding

> Populating databases with initial or test data—reference rows, fixtures, and anonymized production subsets—for development, staging, and automated tests.

```txt
        database seeding ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Seeding questions check whether you separate schema migrations from data, kee…

## Sources
- [Rails Guides — Active Record Migrations](https://guides.rubyonrails.org/active_record_migrations.html) — overview
- [PostgreSQL Documentation — COPY](https://www.postgresql.org/docs/current/sql-copy.html) — deep-dive

## Key Concepts
- **Seeding ≠ migration:** migrations change structure; seeds load reference/fixture rows.
- **Idempotent seeds:** safe to rerun (`INSERT ... ON CONFLICT DO NOTHING`).
- **No production PII:** in repos — synthetic data or scrubbed exports only.
- **Tiered datasets:** minimal smoke seeds vs large performance corpora.

## Technical Details
| Mechanism | Purpose |
|-----------|---------|
| [[database migration]] | Schema structure |
| Seeding | Required reference data (`roles`, `currencies`) and dev fixtures |

```sql
INSERT INTO roles (id, name) VALUES (1, 'admin'), (2, 'user')
ON CONFLICT (id) DO NOTHING;
```

- Bulk loads often use `COPY` / `LOAD DATA` for speed

## Mistakes to Avoid
- **Mistake:** Committing real customer PII as “fixtures.”
- **Mistake:** Non-idempotent seeds that fail on second run and break CI
- **Mistake:** Mixing huge performance datasets into every developer’s default …
- **Mistake:** Using seeds to change schema — that belongs in migrations

## Pros/Cons or Trade-offs
- **Pro:** Predictable environments; tests and demos do not depend on manual clicks.
- **Con:** Oversized seeds slow CI; seeds that encode business logic drift from production truth.

## Comparison
- vs [[database migration]]: migrations own DDL


### Use cases
- Bootstrapping roles/permissions in every environment and loading anonymized s…
