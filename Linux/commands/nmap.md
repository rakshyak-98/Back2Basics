[[nc]] [[ss]] [[Linux network commands]] [[Security]]

# nmap

> One-line: **controlled port and service discovery** — map what's listening before an incident becomes a breach audit. Scope and authorization first; `-A` on prod without approval is a career event.

## Mental model

nmap sends crafted packets (TCP SYN, connect, UDP, etc.) and classifies responses: **open**, **closed** (RST), **filtered** (timeout/no response). Version detection (`-sV`) and scripts (`-sC`) add banner fingerprinting. You are generating traffic that IDS/SOC may alert on.

```
Your host ──SYN scan──► target:port
         ◄──SYN-ACK──  open
         ◄──RST──────  closed
         (silence)     filtered (FW)
```

| Scan type | Flag | Notes |
|-----------|------|-------|
| TCP SYN (stealth-ish) | `-sS` | Needs root/CAP_NET_RAW |
| TCP connect | `-sT` | Unprivileged; full handshake |
| Version detect | `-sV` | Slower; more packets |
| Default scripts | `-sC` | Safe-ish defaults with `-sV` |
| All ports | `-p-` | Slow; use in maintenance window |
| Fast top ports | `-F` | Top 100; good first pass |

## Standard config / commands

**Internal inventory (authorized):**

```bash
# Quick: top ports on one host
nmap -F scanme.nmap.org

# All TCP ports (maintenance window)
sudo nmap -p- -T4 internal-app.local

# Service versions on known ports
sudo nmap -sV -p 22,80,443,5432,6379 db.internal

# Localhost — what's actually bound?
sudo nmap -sT -p- localhost
ss -lntp   # Often faster for local listen audit — see [[ss]]

# UDP (slow, often incomplete)
sudo nmap -sU -F dns.internal

# Output for ticket
nmap -oA /tmp/scan-hostname -sV -p 1-1024 hostname
# Creates .nmap, .gnmap, .xml
```

**Diff scans over time:**

```bash
ndiff scan1.xml scan2.xml
```

**Don't on prod without approval:**

```bash
nmap -A -T4 target    # -A = OS detect + version + scripts + traceroute — noisy
nmap --script=vuln    # intrusive; change state on fragile services
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| All ports filtered | Wrong IP; cloud SG | Verify target; scan from allowed jump host |
| Shows open, app unreachable | App on other IP; bind 127.0.0.1 | `ss -lntp`; fix listen address |
| `-sS` requires root | Capability | `sudo` or use `-sT` |
| Slow scan | `-p-` on /24 | Narrow ports; `-T4`; `--min-rate` with care |
| SOC alert | Scan source logged | Use approved scanner IP; ticket reference |
| Wrong service name | `-sV` guess | Confirm with `curl`, `openssl s_client`, app logs |

## Gotchas

> [!WARNING]
> **Scanning without authorization** — illegal/unethical on networks you don't own. Internal still needs change ticket on sensitive segments.

> [!WARNING]
> **`-sV` / NSE against legacy gear** — can crash brittle embedded devices. Start with `-F` or `-p known`.

- **Cloud metadata `169.254.169.254`** — never scan from compromised instance outward without understanding SSRF context.
- **Docker published ports** — `nmap localhost` shows host bindings; not same as container network namespace.
- **IPv6** — `-6` required; different firewall rules than v4.

## When NOT to use

- **App-layer health** — use HTTP checks, synthetic monitoring, not port open alone.
- **Continuous monitoring** — use dedicated CMDB/service discovery, not cron nmap of /16.
- **Local "what port is my app on"** — [[ss]] `-lntp` is instant and non-invasive.

## Related

[[nc]] [[ss]] [[telnet]] [[Linux network commands]] [[Security]]
