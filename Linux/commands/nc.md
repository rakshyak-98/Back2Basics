[[telnet]] [[ss]] [[nmap]] [[half-open connections]] [[Linux network commands]]

# nc (netcat)

> nc opens a raw TCP/UDP socket as client or listener — the common ops pattern is a connect probe: did SYN get SYN-ACK?

```txt
        nc (netcat) ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Reachability triage: `nc -zv`, timeout `-w`, OpenBSD vs GNU flag differences,…

## Sources
- [nc(1) — OpenBSD](https://man.openbsd.org/nc.1) — deep-dive
- [ncat(1) — Nmap](https://nmap.org/ncat/guide/) — overview

## Key Concepts
- **`-z`:** Zero-I/O scan — connect only.
- **`-w`:** Timeout so DROP doesn’t hang scripts.
- **`-l` / `-p`:** Listen (GNU often needs `-p PORT`).
- **UDP (`-u`):** Weaker signal — no RST like TCP.
- **Layer limit:** Proves TCP handshake, not app correctness.


- **Core:** netcat creates a raw socket. **Connect probe** (`-z`) tests whether a port an…

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

## Mistakes to Avoid
- **Mistake:** Leaving `nc -l` bound on `0.0.0.0` on production
- **Mistake:** Treating open TCP as valid TLS/HTTP
- **Mistake:** Using UDP `-z` success as strong proof

## Pros/Cons or Trade-offs
- **Pro:** Tiny, everywhere, great for TCP reachability.
- **Con:** Flag dialect hell; listeners are accidental backdoors if left open.
- **Trade-off:** bash `/dev/tcp` for portable scripts vs full ncat features.

## Comparison
- vs [[ss]]: local listeners/process ownership. vs [[nmap]]: scoped audits, not…


### Use cases
- Quick “is 443 open from this subnet?”, SMTP banner smoke tests, and temporary…
