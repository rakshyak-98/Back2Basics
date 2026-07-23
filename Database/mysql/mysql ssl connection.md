[[mysql/mysql connection]] [[mysql pool connection]] [[Security/TLS (Transport Layer Security)]] [[connection pooling]]

# MySQL SSL/TLS connections

> One-line: encrypt client↔server traffic and optionally verify server (and client) identity — required for compliance and public-network RDS; configure both server certs and driver `ssl` options.

## Mental model

MySQL supports TLS on connection (like Postgres `sslmode`). Server presents certificate; client verifies CA (`ssl-ca`). **Mutual TLS** adds client cert (`ssl-cert`, `ssl-key`) for auth.

```
App (mysql2/pg driver) ──TLS──► MySQL server
         │ verify ca.pem
         └── optional client cert for REQUIRE X509
```

Without TLS, credentials and result sets traverse network in cleartext. Cloud managed MySQL often **requires** SSL.

## Standard config / commands

### Server (my.cnf)

```ini
[mysqld]
require_secure_transport = ON
ssl_ca   = /etc/mysql/certs/ca.pem
ssl_cert = /etc/mysql/certs/server-cert.pem
ssl_key  = /etc/mysql/certs/server-key.pem
tls_version = TLSv1.2,TLSv1.3
```

### Require SSL for user

```sql
ALTER USER 'app'@'%' REQUIRE SSL;
-- mutual TLS:
ALTER USER 'app'@'%' REQUIRE X509;
```

### Node.js mysql2 pool

```javascript
import fs from 'node:fs';
import mysql from 'mysql2/promise';

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
  ssl: {
    ca: fs.readFileSync('./ca.pem'),
    rejectUnauthorized: true,  // not rejectUnauthorize (typo breaks verify)
  },
  connectionLimit: 10,
});
```

### Verify SSL in session

```sql
SHOW STATUS LIKE 'Ssl_cipher';
-- empty = no encryption
```

```sql
SHOW SESSION STATUS LIKE 'Ssl%';
```

### CLI

```bash
mysql -h host -u user -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem
```

### RDS / cloud

Download combined CA bundle from provider; use `ssl: { ca: rdsCa }` in driver.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `SSL connection error` | CA mismatch; expired cert | Update ca.pem; rotate server cert |
| Connects but `Ssl_cipher` empty | ssl not requested | Add driver `ssl` object; `--ssl-mode=REQUIRED` |
| `SELF_SIGNED_CERT_IN_CHAIN` | Corporate proxy / wrong CA | Install correct CA; never disable verify in prod |
| `ER_ACCESS_DENIED` with REQUIRE X509 | Client cert missing | Provide cert/key in ssl config |
| Works locally, fails in K8s | Wrong secret mount path | Mount CA as secret volume |
| Typo `rejectUnauthorize: false` | Copy-paste | Use `rejectUnauthorized: true` |

## Gotchas

> [!WARNING]
> **`rejectUnauthorized: false`** — MITM can steal DB password.

> [!WARNING]
> **Certificate expiry** — calendar reminder; managed DB rotates CAs.

> [!WARNING]
> **TLS ≠ auth** — still need strong password/IAM; SSL only encrypts channel.

## When NOT to use

- **Local dev on localhost socket only** — optional; still good practice.
- **Performance micro-optimization on private VPC** — TLS overhead usually negligible vs query cost.

## Related

[[mysql pool connection]] [[connection pooling]] [[Security/TLS (Transport Layer Security)]] [[mysql/mysql connection]]
