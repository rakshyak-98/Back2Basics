A database migration is the process of changing a database's structure (schema) in a controlled, versioned way as an application evolves.
- When the migration runs, the database schema is updated without recreating the table.

Why use migrations?
- Lack of Synchronization -> Instead of making direct changes to the database, you create Migration files. These are typically small scripts (written in SQL or your language's specific ORM format) that describe two things:
	- Up the code needed to apply the change
	- Down the code needed to roll back the change if something goes wrong

```sql
-- Up
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- Down
ALTER TABLE users DROP COLUMN email;
```

> Everyone can apply the same renovation plan and end up with the same building structure.

The migration workflow
- Generate -> you trigger a command `npm run generate-migration` to create a timestamped file.
- Define -> You write the schema change in that file.
- Run -> You execute a command (`migrate up`) that applies any pending scripts to the database.
- Track -> the migration tool keeps a special table in your database (often called `migrations` or `schema_history`) to remember which files have already been executed, ensuring they aren't run twice.

## Best practices 

- Never edit past migrations -> once a migration has been pushed to a shared repository or production, it is "locked". If you made a mistake, create a new migration to fix it rather than altering the old one.
- Keep them Atomic -> Each migration file should ideally represent a single, logical change (e.g., adding a table, reaming a column, adding an index).
- Always test the down -> Ensure your rollback logic actually works so you can recover quickly from a bad deployment.