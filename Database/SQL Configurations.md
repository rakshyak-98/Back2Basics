[[mysql]] [[postgres essential]] [[TLS (Transport Layer Security)]] [[connection pooling]] [[ACID]]

# SQL Configurations (MySQL / Postgres)

> **Server knobs that survive reboot** — connection limits, memory, replication, SSL, and logging. Tune for workload (OLTP vs batch), not copy-paste "my.cnf from blog."

## Mental model

RDBMS config layers: **defaults** → **`my.cnf` / `postgresql.conf`** → **runtime `SET` (session)** → **per-user/DB overrides**. Some need restart (`max_connections`, `shared_buffers`); some hot-reload. Wrong combo = OOM, replication lag, or silent full-table scans.

```
Client ──► max_connections / pool ──► buffer pool / shared_buffers ──► disk (WAL, redo)
                                              │
                                              └── slow query log when over threshold
```

Always size with **connection pool** in front ([[connection pooling]]) — 500 app threads ≠ 500 DB connections.

## Standard config / commands

### MySQL 8 — production baseline (adjust to RAM)

`/etc/mysql/mysql.conf.d/mysqld.cnf`:
```ini
[mysqld]
bind-address = 0.0.0.0          # or private IP only
max_connections = 200             # pool limits real concurrency
innodb_buffer_pool_size = 4G      # ~60-70% RAM on dedicated DB host
innodb_redo_log_capacity = 1G     # 8.0.30+
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
slow_query_log = 1
long_query_time = 1
log_bin = mysql-bin               # replication / PITR
server-id = 1
```

Encrypted connections ([MySQL encrypted connections](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html)):
```ini
require_secure_transport = ON       # prod: reject plaintext
ssl_ca = /etc/mysql/ssl/ca.pem
ssl_cert = /etc/mysql/ssl/server-cert.pem
ssl_key = /etc/mysql/ssl/server-key.pem
```

Client:
```bash
mysql -h db.internal -u app --ssl-mode=VERIFY_IDENTITY \
  --ssl-ca=/etc/app/ca.pem -p
```

### PostgreSQL — production baseline

`postgresql.conf`:
```ini
listen_addresses = '*'
max_connections = 200
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 16MB                   # watch: max_connections * work_mem
maintenance_work_mem = 512MB
wal_level = replica                 # replication / PITR
max_wal_size = 4GB
log_min_duration_statement = 500    # ms — slow query log
```

SSL (`pg_hba.conf` + certs):
```ini
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
```

`pg_hba.conf`:
```
hostssl all all 10.0.0.0/8 scram-sha-256
```

Reload: `SELECT pg_reload_conf();` or `systemctl reload postgresql`.

### Verify SSL

```sql
-- MySQL
SHOW STATUS LIKE 'Ssl_cipher';

-- Postgres
SELECT ssl, version, cipher FROM pg_stat_ssl WHERE pid = pg_backend_pid();
```

### Connection pooling (mandatory at scale)

- **PgBouncer** (Postgres) / **ProxySQL** (MySQL) / RDS Proxy — transaction pooling for stateless app queries.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Too many connections` | App pool size × replicas; `max_connections` | Lower pool; raise max slightly; add pooler |
| OOM killer on DB host | `innodb_buffer_pool` + OS cache | Reduce buffer pool; fix oversized `work_mem` |
| Replication lag | `SHOW SLAVE STATUS` / `pg_stat_replication` | Parallel workers; reduce long transactions |
| SSL handshake fail | Cert expiry; wrong CA; `require_secure_transport` | Renew certs; align `ssl-mode` |
| Charset garbled | `utf8` vs `utf8mb4` | Convert to utf8mb4 end-to-end |
| Slow after "config tune" | `long_query_time` too high hid issues | Enable slow log; EXPLAIN |
| Config change no effect | Wrong file path; need restart | `mysqld --verbose --help | grep my.cnf`; restart |

## Gotchas

> [!WARNING]
> **Postgres `work_mem` is per sort/hash node per query** — high value × many connections = RAM explosion.

> [!WARNING]
> **MySQL query cache removed in 8.0** — don't follow old tuning guides.

> [!WARNING]
> **`bind-address = 127.0.0.1` on Docker/K8s** — app can't reach DB; bind private interface or `0.0.0.0` with SG/firewall.

> [!WARNING]
> **Changing charset on live huge table** — locks; plan online migration ([[migration]]).

## When NOT to use

- **Per-query hint tuning before indexes** — fix [[mysql index]] / [[covering index]] first.
- **Disabling fsync/sync_binlog "for speed"** — [[ACID]] and durability trade you may not afford ([[WAL (Write-Ahead Log)]]).

## Related

[[mysql]] · [[postgres essential]] · [[TLS (Transport Layer Security)]] · [[connection pooling]] · [[ACID]] · [[Database mistakes]]
