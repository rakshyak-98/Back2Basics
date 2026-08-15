[[psql essential]] [[SQL]] [[SQL/postgres]]

# psql keywords

> Reserved and unreserved SQL keywords in PostgreSQL — identifiers that need quoting when used as table or column names.

## Interview Relevance
Explains mysterious syntax errors around `"user"` tables and teaches identifier folding rules (unquoted → lowercase).

## Sources
- [SQL Key Words](https://www.postgresql.org/docs/current/sql-keywords-appendix.html) — overview
- [Identifiers and Key Words](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS) — deep-dive

## Key Concepts
- **Reserved vs unreserved:** Reserved words need quoting as identifiers.
- **Folding:** Unquoted identifiers fold to lowercase.
- **Quoted identifiers:** Preserve case; must match exactly afterward.
- **Catalog check:** `pg_get_keywords()`.

## Technical Details
```sql
SELECT "user".id FROM "user";  -- "user" is reserved
SELECT * FROM my_table;        -- unquoted folds to lowercase

SELECT word FROM pg_get_keywords() WHERE word = 'user';
```

Style: prefer `app_user` over `user` so quoting is unnecessary.

## Real-World Applications
Schema reviews rename reserved identifiers; ORMs that quote everything still bite when raw SQL does not.

## Pros/Cons or Trade-offs
- **Pro:** Quoting escapes reserved words when rename is impossible.
- **Con:** Mixed quoted/unquoted use creates “missing relation” ghosts (`User` vs `user`).
- **Trade-off:** Always-quote policy vs never-use-reserved-words policy — prefer the latter.

## Comparison
vs MySQL: reserved lists differ; MySQL also has quoting with backticks. Do not assume portability of identifier names.

## Mistakes to Avoid
- Creating `"User"` then querying `user` without quotes.
- Copying MySQL backtick SQL into Postgres unchanged.
- Using reserved words in public APIs that generate SQL.
