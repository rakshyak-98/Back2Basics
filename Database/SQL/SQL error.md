[[SQL]] [[cli]] [[mysql]] [[mysql user]] [[TLS (Transport Layer Security)]]

# SQL error

> `Public Key Retrieval is not allowed` — MySQL 8 password auth needs the server public key over insecure links; the JDBC client refused to fetch it.

## Mental model

**Say it in one breath:** With `caching_sha2_password`, the client must encrypt the password using the server’s RSA public key; JDBC won’t download that key unless you allow it or use TLS.

```txt
Client (JDBC)                    MySQL 8
  │                                │
  ├─ auth: caching_sha2_password ──┤
  │                                │
  ├─ need server public key ───────┤  (or TLS session)
  │                                │
  └─ blocked if allowPublicKeyRetrieval=false (default)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **caching_sha2_password** | MySQL 8 default auth plugin | “Stronger than native; picky with old clients.” |
| --- | --- | --- |
| **Public key retrieval** | Client fetches server RSA key | “Needed for sha2 auth without TLS.” |
| **allowPublicKeyRetrieval** | JDBC URL flag | “OK for trusted networks; prefer TLS in prod.” |
| **useSSL / TLS** | Encrypt the session | “With TLS, key exchange isn’t the weak path.” |
| **mysql_native_password** | Older plugin | “Compatibility escape hatch — not the long-term fix.” |

## Standard config / commands

```sql
SELECT user, host, plugin FROM mysql.user;
SHOW DATABASES;
SHOW TABLES FROM db_name;
SHOW COLUMNS FROM table_name;
SHOW INDEX FROM table_name;
```

JDBC (development / trusted network):

```txt
jdbc:mysql://host:3306/db?allowPublicKeyRetrieval=true&useSSL=false
```

Prefer production:

```txt
jdbc:mysql://host:3306/db?sslMode=REQUIRED
```

| Knob | Why it matters |

| `allowPublicKeyRetrieval=true` | Unblocks sha2 over cleartext — MITM risk on hostile nets |
| --- | --- |
| TLS required | Proper fix for auth + data in transit |
| User plugin | Confirm `caching_sha2_password` vs native |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Public Key Retrieval is not allowed | JDBC URL + user plugin | Allow retrieval **or** enable TLS |
| Works in CLI, fails in Java | Driver defaults | Update Connector/J; set URL flags |
| Only some users fail | `plugin` per user | Align plugin or client capabilities |
| TLS handshake errors | Certs / `sslMode` | Fix trust store; don’t silently disable SSL in prod |
| Confused with ERROR 1698 | Auth plugin socket | That’s CLI root socket auth — see [[cli]] |

## Gotchas

> [!WARNING]
> **`allowPublicKeyRetrieval=true` is not “security”** — it only unblocks a client policy; use TLS for real protection.

> [!WARNING]
> **Downgrading every user to `mysql_native_password`** — hides the symptom; prefer modern clients + TLS.

> [!WARNING]
> **Copy-pasting `useSSL=false` into prod** — common and wrong.

## When NOT to use

- **Disabling SSL to “make JDBC work” on the public internet** — fix certs instead.
- **Treating this note as a general SQL error catalog** — it’s the MySQL 8 + JDBC public-key failure mode.
- **Changing authentication plugins without understanding clients** — breaks other apps mid-flight.

## Related

[[cli]] [[mysql]] [[mysql user]] [[mysql ssl connection]] [[TLS (Transport Layer Security)]] [[Configuration]]
