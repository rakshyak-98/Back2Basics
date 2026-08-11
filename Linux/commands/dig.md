[[Linux]] [[DNS]] [[dns record]] [[DNS server]] [[DNS zone]] [[TCP]]

# dig

> `dig` asks DNS questions and prints the raw answer — use it to see whether a name, type, or resolver is wrong.

---

## Mental model

**Say it in one breath:** You query a resolver (or an authoritative NS) for a name + type; look at `status` and the `ANSWER SECTION` before blaming the application.

```txt
dig example.com A
        │
        ▼
   resolver (@8.8.8.8 or /etc/resolv.conf)
        │
        ▼
   status: NOERROR + ANSWER    → usable records
   status: NXDOMAIN            → name doesn’t exist
   NOERROR + empty ANSWER      → name exists, that type doesn’t
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Resolver** | Server you ask first | “Stub resolver → recursive → authoritative.” |
| **Authoritative** | NS that owns the zone | “Query `@ns1…` to bypass cache lies.” |
| **NOERROR** | Query processed OK | “Not the same as ‘has an A record’.” |
| **NXDOMAIN** | Name does not exist | “Typo or zone missing.” |
| **ANSWER SECTION** | Records you asked for | “Empty answer + NOERROR → wrong type.” |
| **TTL** | Cache lifetime | “High TTL slows rollback after a fix.” |

### How the story goes (4 steps)

1. **Ask** — `dig name [type]` (hostname only — no `https://`).
2. **Read status** — NXDOMAIN versus NOERROR.
3. **Read answer** — A/AAAA/CNAME/MX/… present?
4. **Isolate cache** — `@8.8.8.8`, `@1.1.1.1`, then `@` authoritative NS; `+trace` if needed.

---

## Standard config / commands

```bash
dig example.com
dig +short example.com
dig @8.8.8.8 example.com A
dig example.com AAAA
dig example.com MX
dig example.com CNAME
dig example.com NS

dig +trace example.com
dig @ns1.example.net example.com A    # authoritative

resolvectl status                     # systemd-resolved upstream
```

| Knob | Why it matters |
|------|----------------|
| `@server` | Bypass local cache / broken ISP DNS |
| `+short` | Script-friendly; hide noise |
| `+trace` | Walk root → TLD → auth — finds delegation breaks |
| Type (`A` vs `AAAA`) | Dual-stack bugs look like “DNS is down” |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No ANSWER SECTION | `status:` line | NXDOMAIN → name; NOERROR empty → add type / fix CNAME chain |
| Works on 8.8.8.8, not locally | Local resolver / cache | Flush; fix `resolv.conf` / corporate DNS |
| Wrong IP after change | TTL; auth vs cache | Query auth NS; wait TTL; lower TTL before cuts |
| App fails, dig OK | App DNS / Happy Eyeballs | Check AAAA, search domains, `/etc/nsswitch.conf` |
| `dig https://…` fails | URL shaped query | Use bare hostname |

### Empty ANSWER playbook

```bash
dig example.com            # status?
dig example.com A
dig example.com AAAA
dig example.com NS
dig @$(dig +short example.com NS | head -1) example.com A
```

---

## Gotchas

> [!WARNING]
> **NOERROR + empty answer** is normal when the type is missing — not “DNS is broken.”

> [!WARNING]
> **CNAME at apex** / conflicting records — follow the chain; don’t stop at the first response.

> [!WARNING]
> **Split-horizon DNS** — VPN vs public answers differ; dig from the same network as the app.

> [!WARNING]
> **`search` domains** in resolv.conf rewrite short names — `dig` of FQDN with trailing dot avoids search.

---

## When NOT to use

- **HTTP debugging** — use `curl -v`; dig only proves name→IP.
- **DNSSEC deep validation UX** — specialized tools; dig can show `AD` bits but isn’t a full auditor.
- **Load-balancer health** — dig won’t tell you if port 443 is up; combine with `nc`/`curl`.

---

## Related

[[DNS]] [[dns record]] [[DNS server]] [[DNS zone]] [[getent]] [[nc]] [[Linux network commands]]
