[[redis-cli]] [[systemd]] [[connection pooling]] [[Docker compose]]

# redis installation

> Install and harden Redis: package or image runs `redis-server` with `redis.conf`, systemd supervision, bind/ACL, and RDB/AOF under `/var/lib/redis`.

## Interview Relevance

Interviewers probe bind/protected-mode, ACL versus `requirepass`, `maxmemory` policy, and why an open `0.0.0.0:6379` is an instant incident.

## Sources

- [Redis — Install](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) — overview
- [Redis — Configuration](https://redis.io/docs/latest/operate/oss_and_stack/management/config/) — deep-dive
- [Redis — ACL](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/) — deep-dive

## Key Concepts

- **Process model:** `redis-server` + systemd + listen address + persistence directory.
- **Protected-mode:** default safety when unbound auth would expose you — not a substitute for ACL + firewall.
- **ACL (6+):** per-user command/key permissions; prefer over legacy `requirepass`.
- **Memory + persistence:** `maxmemory` + eviction; RDB/AOF trade durability for latency.

## Technical Details

```
Package / image ──► redis-server ──► reads redis.conf
                         │
                         ├── systemd unit (restart, limits)
                         ├── TCP/UNIX listen + ACL
                         └── RDB/AOF under dir /var/lib/redis
```

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
sudo systemctl restart redis-server
```

Typical unit: `User=redis`, `ExecStart=/usr/bin/redis-server /etc/redis/redis.conf`, `LimitNOFILE=65535`.

### redis.conf essentials

```ini
bind 127.0.0.1 ::1
port 6379
protected-mode yes

# ACL (recommended 6+)
# user app on >APP_SECRET ~app:* +get +set +del +expire

maxmemory 1gb
maxmemory-policy allkeys-lfu

dir /var/lib/redis
dbfilename dump.rdb
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec

supervised systemd
daemonize no
logfile ""
slowlog-log-slower-than 10000
slowlog-max-len 128
```

### ACL setup

```bash
redis-cli ACL SETUSER app on >$(openssl rand -base64 32) ~app:* +@read +@write +@string -@dangerous
redis-cli ACL SETUSER default off
redis-cli ACL LIST
redis-cli CONFIG REWRITE
```

Connection string: `redis://app:SECRET@127.0.0.1:6379/0`

| Deployment | bind | protected-mode | auth |
|------------|------|----------------|------|
| Dev laptop | 127.0.0.1 | yes | optional |
| App on same host | 127.0.0.1 | yes | recommended |
| Private VPC only | internal IP | yes + firewall | ACL required |
| Public internet | **don't** | — | use TLS + VPC + ACL |

```bash
redis-cli PING
redis-cli INFO server | grep redis_version
redis-cli CONFIG GET bind
sudo ss -tlnp | grep 6379
sudo chown redis:redis /var/lib/redis /etc/redis/redis.conf
sudo chmod 640 /etc/redis/redis.conf
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection refused` | `systemctl status`; bind | Start service; fix `bind`; firewall |
| `NOAUTH` | ACL/requirepass | Update app URL; `ACL LIST` |
| Starts then exits | `journalctl -u redis-server` | Bad `dir` permissions; corrupt AOF → `redis-check-aof` |
| Can't write config | `CONFIG SET` without rewrite | Edit redis.conf; restart; fix ownership |
| OOM on host | no `maxmemory` | Set cap + eviction policy |
| Exposed to internet scan | `ss -tlnp` | Firewall; bind localhost; ACL; disable default user |

## Real-World Applications

Local cache for a monolith, sidecar Redis in [[Docker compose]], and VPC-private Redis for session stores.

**Example:** App and Redis on one host bind `127.0.0.1`, ACL user `app` limited to `~app:*`, `maxmemory-policy allkeys-lfu`.

## Pros/Cons or Trade-offs

- **Pro:** Fast install path with strong defaults if you keep bind local + ACL.
- **Con:** Wrong bind exposes an in-memory database to the internet.
- **Con:** Self-managed multi-master/cluster topology is harder than managed Redis.

## Comparison

- vs managed Redis (ElastiCache/Memorystore): managed wins for HA/patching; self-install wins for local/dev control.
- vs Redis Stack packages: different unit name and module memory profile — do not assume identical.

## Mistakes to Avoid

- `requirepass` committed in git — use secret mounts/templates.
- `daemonize yes` under systemd notify — breaks supervision.
- Leaving transparent huge pages enabled — latency spikes (Redis recommends `never`).
- Missing `vm.overcommit_memory=1` so RDB fork fails.
- Blind package upgrades overwriting `/etc/redis/redis.conf`.
- Binding `127.0.0.1` inside Docker and expecting the host to reach it without network setup.
