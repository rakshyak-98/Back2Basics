[[database migration]] [[Database design]] [[mysql dump]]

# database seeding

> Populating databases with initial or test data—reference rows, fixtures, and anonymized production subsets—for development, staging, and automated tests.

## Seeding versus migration

| Mechanism | Purpose |
|-----------|---------|
| [[database migration]] | Schema structure |
| Seeding | Required reference data (`roles`, `currencies`) and dev fixtures |

## Practices

- Keep seeds **idempotent** (`INSERT ... ON CONFLICT DO NOTHING`)
- Never commit production PII — generate synthetic data or scrub exports
- Separate **minimal smoke seeds** from large performance datasets

```sql
INSERT INTO roles (id, name) VALUES (1, 'admin'), (2, 'user')
ON CONFLICT (id) DO NOTHING;
```

## Sources

- Rails Guides — [Active Record Migrations](https://guides.rubyonrails.org/active_record_migrations.html) (seed patterns)
- PostgreSQL Documentation — [COPY](https://www.postgresql.org/docs/current/sql-copy.html)
