<!-- note-strategy: reference -->
[[commands]] [[ss]] [[netstat]] [[lsof]] [[ip]] [[dig]] [[nc]] [[ufw]]

# Linux network commands

> Pocket kit for “is it listening, reachable, or DNS?” — `ss`/`lsof` for sockets, `nc`/`tcpdump` to probe, `dig`/resolvectl for names.

---

## Index

- [[#Quick reference]]
- [[#Common commands]]
- [[#Options / flags]]
- [[#Mental model]]
- [[#Sockets & listeners]]
- [[#Probe & capture]]
- [[#DNS]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

## Common commands

```bash
# …
```

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Mental model

**Say it in one breath:** inventory with `ss`, ownership with `lsof`, path with `ip`/`ping`, application reachability with `nc`, packets with `tcpdump`, names with `dig`.

```txt
Listen?  ss -lntup / lsof -i
Reach?   nc -zv host port
Route?   ip route get 1.1.1.1
Name?    dig +short / resolvectl
Packets? tcpdump -ni eth0 port 443
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`ss -lntup`** | Listeners + process | “First command on ‘port already in use’.” |
| **`Recv-Q` / `Send-Q`** | Bytes waiting | “High Send-Q → peer not reading; Recv-Q → local app slow.” |
| **`nc -zv`** | TCP connect probe | “Firewall vs process down — one packet tells you.” |
| **`tcpdump`** | Packet trace | “Prove SYN leaves and SYN-ACK returns.” |
| **`resolvectl`** | systemd-resolved status | “Stub vs real resolvers on modern Ubuntu.” |

---

## Sockets & listeners

```bash
ss -lntup                          # prefer over netstat
ss -tan
sudo lsof -i -P -n | grep LISTEN
sudo netstat -tuln                 # legacy; see [[netstat]]

# Column cheat (ss/netstat style)
# Proto  Recv-Q  Send-Q  Local  Foreign  State
```

| Flag family | Meaning |
|-------------|---------|
| `-l` | Listening |
| `-t`/`-u` | TCP/UDP |
| `-n` | Numeric |
| `-p` | Process |

---

## Probe & capture

```bash
nc -zv example.com 443
nc -z -v host 20-100
nc -l -p 1234                      # listener lab
# file copy lab: nc -l -p PORT > in.txt   /   nc host PORT < out.txt

sudo tcpdump -ni any port 80 or port 443

# iptables glance (host firewall)
sudo iptables -L -n
# Prefer [[ufw]] status on Ubuntu desktops/servers that use it
```

---

## DNS

```bash
dig +short example.com
nslookup example.com
resolvectl status                  # was systemd-resolve
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `ss -lnt` on target | Start service / fix bind address |
| Timeout | `nc -zv`; tcpdump SYN | Security group / [[ufw]] / route |
| Works by IP, not name | `dig`; resolvectl | Fix resolvers / search domain |
| Port in use | `ss -lntp 'sport = :8080'` | Stop PID or change port |
| High TIME-WAIT / churn | `ss -s` | See [[ss]] / connection churn notes |

---

## Gotchas

> [!WARNING]
> **`nc -e` bind shells are malware patterns** — many distros disable `-e`; don’t “test” that on shared hosts.

> [!WARNING]
> **`netstat` may be missing** — install net-tools or use [[ss]].

> [!WARNING]
> **Cloud firewall ≠ host firewall** — open both paths.

---

## When NOT to use

- **Deep TCP internals** — prefer [[ss]] `-ti` and dedicated notes.
- **Service mesh / K8s NetworkPolicy debug** — `kubectl` + CNI tools.
- **Long-term metrics** — exporters, not one-shot `ss`.

---

## Examples

```bash
# …
```

## Related

[[ss]] [[netstat]] [[lsof]] [[ip]] [[dig]] [[nc]] [[ufw]] [[commands]]
