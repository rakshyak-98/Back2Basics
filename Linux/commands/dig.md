[[DNS]] [[dns record]] [[DNS server]] [[DNS zone]] [[getent]] [[nc]] [[Linux network commands]]

# dig

> dig asks DNS questions and prints the raw answer — use it to see whether a name, type, or resolver is wrong.

```txt
        dig ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** DNS debugging: NOERROR vs NXDOMAIN vs empty answer, `+trace`, querying auth N…

## Sources
- [dig(1)](https://man.bind9.net/man1/dig.html) — deep-dive
- [RFC 1035 — DNS](https://www.rfc-editor.org/rfc/rfc1035) — overview

## Key Concepts
- **NOERROR + ANSWER:** Usable records for that type.
- **NXDOMAIN:** Name does not exist.
- **NOERROR + empty:** Name exists; that type doesn’t (common for missing AAAA).
- **`+trace`:** Walk from root to leaf.
- **Auth query:** `@ns1…` bypasses recursive cache for truth from the zone.


- **Core:** `dig` sends DNS queries to a resolver (from `/etc/resolv.conf` or `@server`) …

## Technical Details
```bash
dig example.com
dig +short example.com
dig @8.8.8.8 example.com A
dig example.com AAAA
dig example.com MX
dig example.com CNAME
dig example.com NS

dig +trace example.com
dig @ns1.example.net example.com A

resolvectl status
dig example.com.          # trailing dot = FQDN, no search

dig @$(dig +short example.com NS | head -1) example.com A
```

| Symptom | Check | Fix |
|---------|-------|-----|
| App fails, dig OK | nsswitch / search | Compare [[getent]] hosts; check search domains |
| Empty ANSWER | Wrong type | Query A and AAAA; read status |
| Split-horizon mismatch | VPN vs public | dig from same network as app |
| Stale answer | Cache | Query auth NS; lower TTL wait |

## Mistakes to Avoid
- **Mistake:** Treating empty NOERROR as “DNS broken.”
- **Mistake:** Stopping at a CNAME without following the chain
- **Mistake:** Forgetting search domains rewrite short names (use trailing dot)

## Pros/Cons or Trade-offs
- **Pro:** Explicit, typed, scriptable DNS truth.
- **Con:** Doesn’t show what glibc NSS will do for short names.
- **Trade-off:** `+short` for scripts vs full output for humans.

## Comparison
- vs [[getent]] hosts: NSS path including files


### Use cases
- Proving a missing AAAA is intentional empty NOERROR, verifying a change hit a…
