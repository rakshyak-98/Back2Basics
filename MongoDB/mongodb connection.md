[[MongoDB]] [[mongoose middleware]] [[DNS]] [[connection pooling]]

# MongoDB connection

> URI + driver options that keep your app talking to the right cluster under load and failover — **MongoDB Manual** + production incident patterns.

## Mental model

The driver maintains a **connection pool** to mongod/mongos processes. Each URI encodes auth, replica set name, TLS, and read/write preference. On startup the driver discovers topology (standalone → replica set → sharded). Writes go to the primary (unless you explicitly use secondary reads with caveats); reads follow `readPreference`.

```
App → Driver pool → Primary (writes)
                  → Secondary (reads, if allowed)
                  → mongos (sharded cluster)
```

## Standard config / commands

### Connection string (replica set, prod-safe defaults)

```
mongodb://user:pass@host1:27017,host2:27017,host3:27017/mydb?replicaSet=rs0&authSource=admin&tls=true&retryWrites=true&w=majority&maxPoolSize=50&serverSelectionTimeoutMS=5000
```

| Option | Why |
|--------|-----|
| `replicaSet` | Required for RS discovery; wrong name = silent wrong host |
| `authSource=admin` | User often lives in `admin`, not app DB |
| `retryWrites=true` | Idempotent retry on transient network blips |
| `w=majority` | Durability across replica set |
| `serverSelectionTimeoutMS` | Fail fast instead of hang forever |
| `maxPoolSize` | Cap connections per app instance |

### Mongoose

```js
await mongoose.connect(process.env.MONGODB_URI, {
  maxPoolSize: 50,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
});
```

### Compass / CLI smoke test

```bash
mongosh "mongodb://user:pass@host:27017/mydb?authSource=admin" --eval 'db.runCommand({ ping: 1 })'
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `getaddrinfo EAI_AGAIN` | `dig host`, Docker network, VPN | Fix [[DNS]]; use service name on same network |
| `MongoServerSelectionError: timed out` | Firewall, SG, wrong port | Open 27017 between app ↔ DB; verify RS members reachable |
| `Authentication failed` | `authSource`, user DB | Create user in correct DB; match URI `authSource` |
| `not primary` on write | `rs.status()` | Wait for election; fix primary; don't write to secondary |
| Pool exhausted / slow | `db.serverStatus().connections` | Lower per-app `maxPoolSize`; scale app or DB |
| TLS handshake fail | cert SAN, CA bundle | Add CA to trust store; use `tlsCAFile` |

## Gotchas

> [!WARNING]
> **Atlas IP allowlist** — app on dynamic IP or new k8s node → connection works locally, fails in prod until IP added.
>
> **Docker `localhost`** — container `localhost` is itself, not host MongoDB. Use service name or `host.docker.internal`.
>
> **Secondary reads** — stale reads + no writes; use `readPreference=secondaryPreferred` only when you accept lag.

## When NOT to use

- Don't open MongoDB to `0.0.0.0` on the public internet without TLS + auth + network ACL.
- Don't create one connection per request — always pool via driver/mongoose.

## Related

[[mongodb replicaset]] [[mongodb errors]] [[connection pooling]] [[DNS]]
