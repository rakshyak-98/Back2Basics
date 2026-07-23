[[redis-cli]] [[systemd]]

# redis installation

> Install Redis as a managed service — bind address, auth/ACL, memory cap, and persistence before exposing beyond localhost.

## Mental model

```
Package / image ──► redis-server ──► reads redis.conf
                         │
                         ├── systemd unit (restart, limits)
                         ├── TCP/UNIX listen + ACL
                         └── RDB/AOF under dir /var/lib/redis
```

**Default upstream packages** expose `6379` with **protected-mode** if no password and bind not restricted — fine for dev trap, dangerous if firewall wrong.

## Standard config / commands

### Install (Debian/Ubuntu — official redis.io repo)

```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis-server    # or redis-stack-server for modules
```

### systemd

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
sudo journalctl -u redis-server -f

# After config change
sudo systemctl restart redis-server
# Prefer CONFIG REWRITE for runtime-persisted changes when using include
```

Typical unit (`/lib/systemd/system/redis-server.service`):

- `User=redis` `Group=redis`
- `ExecStart=/usr/bin/redis-server /etc/redis/redis.conf`
- `LimitNOFILE=65535` — raise if `maxclients` high

### redis.conf essentials (production baseline)

```ini
# Network — default safe: localhost only
bind 127.0.0.1 ::1
port 6379
protected-mode yes          # yes when no auth + non-local bind blocked

# Auth — pick ACL (6+) or requirepass (legacy)
# requirepass CHANGE_ME_LONG_RANDOM

# ACL (recommended 6+)
# user default on nopass ~* &* +@all    # dev only
# user app on >APP_SECRET ~app:* +get +set +del +expire

# Memory
maxmemory 1gb
maxmemory-policy allkeys-lfu

# Persistence (cache-only can disable both — document the risk)
dir /var/lib/redis
dbfilename dump.rdb
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec

# Security / ops
supervised systemd
daemonize no                # systemd manages foreground
logfile ""                  # log to stdout/journal
slowlog-log-slower-than 10000
slowlog-max-len 128

# Rename dangerous commands (optional)
# rename-command FLUSHALL ""
# rename-command CONFIG "CONFIG_9a7b2c"
```

### ACL setup example

```bash
redis-cli ACL SETUSER app on >$(openssl rand -base64 32) ~app:* +@read +@write +@string -@dangerous
redis-cli ACL SETUSER default off    # disable default after app user works
redis-cli ACL LIST
redis-cli CONFIG REWRITE
```

App connection string:

```
redis://app:SECRET@127.0.0.1:6379/0
```

### Bind + protected-mode decision table

| Deployment | bind | protected-mode | auth |
|------------|------|----------------|------|
| Dev laptop | 127.0.0.1 | yes | optional |
| App on same host | 127.0.0.1 | yes | recommended |
| Private VPC only | internal IP | yes + firewall | ACL required |
| Public internet | **don't** | — | use TLS + VPC + ACL |

```ini
# Private network — still use ACL + firewall SG
bind 10.0.1.50
protected-mode yes
```

Never `bind 0.0.0.0` without auth, firewall, and TLS consideration.

### Post-install verify

```bash
redis-cli PING
redis-cli INFO server | grep redis_version
redis-cli CONFIG GET bind
redis-cli CONFIG GET maxmemory
sudo ss -tlnp | grep 6379          # confirm listen address
```

### File permissions

```bash
sudo chown redis:redis /var/lib/redis /etc/redis/redis.conf
sudo chmod 640 /etc/redis/redis.conf
# secrets outside world-readable paths
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection refused` | `systemctl status`; bind | Start service; fix `bind`; firewall |
| `NOAUTH` | ACL/requirepass | Update app URL; `ACL LIST` |
| Starts then exits | `journalctl -u redis-server` | Bad `dir` permissions; corrupt AOF → `redis-check-aof` |
| Can't write config | `CONFIG SET` without rewrite | Edit redis.conf; restart; fix ownership |
| OOM on host | no `maxmemory` | Set cap + eviction policy |
| Exposed to internet scan | Shodan/censys; `ss -tlnp` | Firewall; bind localhost; ACL; disable default user |

## Gotchas

> [!WARNING]
> **`requirepass` in git** — config management leaks secrets. Use env-substituted template or secret mount.

> [!WARNING]
> **Redis Stack default** — different unit name (`redis-stack-server`); modules change memory profile.

- ** systemd `Type=notify`** — Redis supports `supervised systemd`; wrong `daemonize yes` breaks notify.
- **THP (transparent huge pages)** — Redis docs say disable on Linux for latency (`never` in sysfs).
- **Overcommit memory** — fork for RDB needs `vm.overcommit_memory=1` on Linux (see official FAQ).
- **Package upgrade** — config diff in `/etc/redis/redis.conf.dpkg-old`; merge don't blind overwrite.
- **Docker sidecar** — bind `127.0.0.1` in container ≠ host; use network namespace or shared volume unix socket.

## When NOT to use

- **Multi-master write on open network** — use managed Redis / cluster with proper topology.
- **requirepass only on 6+** — migrate to ACL for command-level least privilege.
- **Installing from random PPA** — use official redis.io or distro you trust; pin version.

## Related

[[redis-cli]] [[systemd]] [[connection pooling]] [[Docker compose]]
