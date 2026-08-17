[[DNS]] [[public resolver]] [[name server]] [[dnsmasq]] [[BIND]] [[unbound variable]]

# Unbound

> Unbound is a validating recursive DNS resolver designed for security and performance — run it on servers or laptops to cache queries locally, enforce DNSSEC, and forward or recurse without trusting ISP DNS.

```txt
        Unbound ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers expect Unbound as the validating recursive choice

## Sources
- [Unbound documentation](https://unbound.docs.nlnetlabs.nl/) — deep-dive
- [NLnet Labs — Unbound](https://nlnetlabs.nl/projects/unbound/about/) — overview

## Key Concepts
- **Recursive focus:** walks or forwards; not a full zone-master replacement for [[BIND]].
- **DNSSEC validator:** broken DS/chain → `SERVFAIL` instead of insecure answers.
- **Access control:** never open recursion to the world without rate limits.
- **Not bash nounset:** shell “unbound variable” is [[unbound variable]], not this daemon.

## Technical Details
| Role | Configuration |
|------|---------------|
| **Local recursive resolver** | Full iteration from root hints |
| **Forwarding resolver** | Forwards to [[public resolver]] or ISP |
| **DNSSEC validator** | `module-config: "validator iterator"` |
| **Corporate internal** | Split DNS with local zones + forward public |

```yaml
server:
  interface: 127.0.0.1
  access-control: 127.0.0.0/8 allow
  do-ip6: yes
  hide-identity: yes
  hide-version: yes
  harden-glue: yes
  use-caps-for-id: yes
  prefetch: yes
  num-threads: 2

forward-zone:
  name: "."
  forward-addr: 1.1.1.1@53
  forward-addr: 8.8.8.8@53
```

- Restrict `access-control`

```bash
sudo systemctl enable --now unbound
resolvectl status   # ensure not fighting systemd-resolved on :53
dig @127.0.0.1 example.com A +dnssec
unbound-control status
```

- When validation fails, Unbound returns `SERVFAIL`.
- Broken parental DS records or clock skew cause false negatives.

| Unbound | BIND |
|---------|------|
| Recursive focus | Authoritative + recursive |
| Lightweight | Full zone master features |
| Default on many Linux stubs | Enterprise authoritative standard |

- Pair **BIND authoritative** internally with **Unbound** on clients or DMZ res…

## Mistakes to Avoid
- **Mistake:** Opening `access-control` to `0.0.0.0/0` on a public IP
- **Mistake:** Misreading DNSSEC `SERVFAIL` as “network down” without `dig +dns…
- **Mistake:** Running Unbound and systemd-resolved both on `:53` without coord…

## Pros/Cons or Trade-offs
- **Pro:** Strong default security posture and DNSSEC validation.
- **Con:** Not ideal as your only Internet authoritative zone server.
- **Con:** Port 53 fights with systemd-resolved / [[dnsmasq]] if both listen.

## Comparison
- vs [[BIND]]: Unbound for recursion; BIND for authoritative Internet zones.
- vs [[dnsmasq]]: Unbound is the validating resolver; dnsmasq adds DHCP/LAN convenience.
- vs [[unbound variable]]: completely different topic (Bash `set -u`).


### Use cases
- Laptop local resolver, office recursive tier, and DMZ validating resolvers in…

- **Example:** Bind Unbound to `127.0.0.1` on a laptop
