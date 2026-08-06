[[MongoDB]]

# mongodb shell

> One-line: what / why for **mongodb shell** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

[mongodb shell run Command](https://www.mongodb.com/docs/manual/reference/method/db.runCommand/)
```shell
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "age"],
      properties: {
        name: { bsonType: "string", description: "must be a string" },
        email: { bsonType: "string", pattern: "^.+@.+$", description: "must be an email" },
        age: { bsonType: "int", minimum: 0, description: "must be a positive integer" }
      }
    }
  }
})
```
### Create transaction
```js
session = db.getMongo().startSession();
sessionDb = session.getDatabase("test");
session.startTransaction();
session.commitTransaction();
session.abortTransaction();
session.endSession();
```
```js
db.adminCommand({ listSessions: {} }); // return all active session
db.adminCommand({ listSessions: { allUsers: false }}); // returns only sessions owned by the current user.
```
```js
db.runCommand({ help: 1})
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
