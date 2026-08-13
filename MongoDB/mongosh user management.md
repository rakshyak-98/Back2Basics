[[MongoDB]] [[mongosh]]

# mongosh user management

> MongoDB users and roles live in databases — grant least privilege, usually via `admin`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Create a user with roles scoped to a DB (or cluster); authenticate with that user + `authSource`.

```txt
admin.createUser → roles[{ role, db }] → clients auth with authSource
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Role** | Privilege bundle | “`readWrite` on `app`.” |
| **authSource** | DB that stores the user | “Often `admin`.” |
| **Custom role** | Least privilege set | “Only `find` on one coll.” |
| **SCRAM** | Password auth mechanism | “Default for users.” |

---

## Standard config / commands

```js
use admin
db.createUser({
  user: 'app',
  pwd: passwordPrompt(),
  roles: [{ role: 'readWrite', db: 'app' }],
})
db.getUsers()
db.updateUser('app', { roles: [{ role: 'read', db: 'app' }] })
db.dropUser('app')
```

| Knob | Why it matters |
|------|----------------|
| Built-in roles | Fast start |
| Custom roles | Lock down collections |
| X.509 / LDAP | Enterprise auth stories |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| not authorized | roles on wrong db | Grant on target db |
| Auth failed | authSource mismatch | Point URI at user DB |
| Can’t create user | not admin | Use root/userAdmin |
| Too much privilege | `root` in apps | Replace with readWrite |

---

## Gotchas

> [!WARNING]
> **Users in app DB vs admin** — URI `authSource` must match where the user was created.

> [!WARNING]
> **Shared root credentials in apps** — blast radius on leak.

---

## When NOT to use

- **Local disposable docker** — root is fine for throwaway demos.
- **Managed Atlas** — prefer UI/API database users.

## Related

[[mongosh]] [[mongodb connection]]
