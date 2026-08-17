[[nc]] [[ss]] [[telnet]] [[Linux network commands]] [[Security]]

# nmap

> Controlled port and service discovery — map what is listening; authorization and scope come before any scan.

```txt
        nmap ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Tests whether you understand scan types (SYN vs connect), noisy flags (`-A`, …

## Sources
- [Nmap Reference Guide](https://nmap.org/book/man.html) — deep-dive
- [Wikipedia — nmap](https://en.wikipedia.org/wiki/nmap) — overview

## Key Concepts
- **Open / closed / filtered:** SYN-ACK, RST, or silence (often firewall).
- **`-sS` vs `-sT`:** SYN needs root/`CAP_NET_RAW`
- **`-sV` / `-sC`:** version and default scripts — slower, noisier.
- **Authorization first:** internal segments still need change tickets on sensitive networks.


- **Core:** nmap sends crafted packets (TCP SYN, connect, UDP, and more) and classifies r…

## Technical Details
```
Your host ──SYN scan──► target:port
         ◄──SYN-ACK──  open
         ◄──RST──────  closed
         (silence)     filtered (FW)
```

| Scan type | Flag | Notes |
|-----------|------|-------|
| TCP SYN | `-sS` | Needs root/CAP_NET_RAW |
| TCP connect | `-sT` | Unprivileged; full handshake |
| Version detect | `-sV` | Slower; more packets |
| Default scripts | `-sC` | Safer defaults with `-sV` |
| All ports | `-p-` | Slow; maintenance window |
| Fast top ports | `-F` | Top 100; good first pass |

```bash
nmap -F scanme.nmap.org
sudo nmap -p- -T4 internal-app.local
sudo nmap -sV -p 22,80,443,5432,6379 db.internal
sudo nmap -sT -p- localhost
ss -lntp
sudo nmap -sU -F dns.internal
nmap -oA /tmp/scan-hostname -sV -p 1-1024 hostname
ndiff scan1.xml scan2.xml
```

- Avoid on production without approval:

```bash
nmap -A -T4 target       # OS + version + scripts + traceroute — noisy
nmap --script=vuln       # intrusive; can change fragile services
```

| Symptom | Check | Fix |
|---------|-------|-----|
| All ports filtered | Wrong IP; cloud security group | Verify target; scan from allowed jump host |
| Shows open, app unreachable | Bind `127.0.0.1`; other IP | `ss -lntp`; fix listen address |
| `-sS` requires root | Capability | `sudo` or use `-sT` |
| Slow scan | `-p-` on large ranges | Narrow ports; `-T4`; care with `--min-rate` |
| SOC alert | Scan source logged | Approved scanner IP; ticket reference |

## Mistakes to Avoid
- **Mistake:** Scanning without authorization
- **Mistake:** Running `-sV` / vuln scripts against legacy embedded gear withou…
- **Mistake:** Forgetting IPv6 (`-6`) and different firewall rules than IPv4
- **Mistake:** Treating “port open” as application healthy

## Pros/Cons or Trade-offs
- **Pro:** Rich discovery (ports, versions, scripts) across many hosts.
- **Con:** Noisy; can crash brittle devices; not a substitute for application health checks.

## Comparison
- vs [[ss]]: local socket table — use for this host; nmap for remote/authorized discovery.
- vs [[nc]]: single-port probe/debug; nmap for systematic sweeps.


### Use cases
- Authorized inventory before a firewall change, localhost listen audit, or dif…

- **Example:** Prefer `ss -lntp` for “what is my application listening on?”
