[[telnet]] [[ss]] [[nmap]] [[half-open connections]] [[Linux network commands]]

# nc (netcat)

> nc opens a raw TCP/UDP socket as client or listener — the common ops pattern is a connect probe: did SYN get SYN-ACK?





## Interview Relevance
Reachability triage: `nc -zv`, timeout `-w`, OpenBSD vs GNU flag differences, and knowing TCP open ≠ HTTP/TLS OK.

## Sources
- [nc(1) — OpenBSD](https://man.openbsd.org/nc.1) — deep-dive
- [ncat(1) — Nmap](https://nmap.org/ncat/guide/) — overview

## Core Definition
netcat creates a raw socket. **Connect probe** (`-z`) tests whether a port answers; **listen** (`-l`) accepts connections for debug sinks. Variants (OpenBSD `nc`, GNU netcat, `ncat`) differ in flags.

## Key Concepts
- **`-z`:** Zero-I/O scan — connect only.
- **`-w`:** Timeout so DROP doesn’t hang scripts.
- **`-l` / `-p`:** Listen (GNU often needs `-p PORT`).
- **UDP (`-u`):** Weaker signal — no RST like TCP.
- **Layer limit:** Proves TCP handshake, not app correctness.

## Technical Details
| Variant | `-z` scan | Listen | Notes |
|---------|-----------|--------|-------|
| OpenBSD `nc` | yes | `-l` | Common on Debian/Ubuntu |
| GNU netcat | `-z` | `-l -p PORT` | `-p` required |
| `ncat` | `-z` | `-l` | `--ssl`, proxy features |

```bash
nc -zv example.com 443
nc -zv example.com 22 80 443
nc -zv -w 3 example.com 22
nc -zuv example.com 53

printf 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n' | nc -w 3 example.com 80
nc -w 5 mail.example.com 25

nc -lk 8080          # OpenBSD; GNU: nc -l -p 8080
ss -lntp | grep :8080
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | Service/port | `ss -lntp`; start unit; bind address |
| Hang then timeout | Firewall DROP | Path/SG; use `-w` |
| `-zv` open, app fails | TLS/HTTP layer | `openssl s_client`, curl |
| UDP “open” flaky | Normal | App-specific probe (`dig @host`) |

## Real-World Applications
Quick “is 443 open from this subnet?”, SMTP banner smoke tests, and temporary localhost listeners for webhook debugging.

## Pros/Cons or Trade-offs
- **Pro:** Tiny, everywhere, great for TCP reachability.
- **Con:** Flag dialect hell; listeners are accidental backdoors if left open.
- **Trade-off:** bash `/dev/tcp` for portable scripts vs full ncat features.

## Comparison
vs [[ss]]: local listeners/process ownership. vs [[nmap]]: scoped audits, not ad-hoc probes. vs [[telnet]]: similar banner poking; nc is more scriptable.

## Mistakes to Avoid
- Leaving `nc -l` bound on `0.0.0.0` on production.
- Treating open TCP as valid TLS/HTTP.
- Using UDP `-z` success as strong proof.
