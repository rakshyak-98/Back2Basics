[[DNS]] [[localhost]] [[CORS (Cross Origin Request Sharing)]] [[Security]] [[dns record]]

# DNS rebinding

> DNS rebinding tricks a browser into treating an attacker-controlled hostname as same-origin with an internal IP — the attack rotates DNS answers from a public IP to `127.0.0.1` or RFC1918 space after the same-origin che…

```txt
        DNS rebinding ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Security and frontend reviews use this to test same-origin policy depth

## Sources
- [Stanford — DNS Rebinding Protection in Web Browsers](https://crypto.stanford.edu/dns/dns-rebinding.pdf) — deep-dive
- [W3C Private Network Access](https://wicg.github.io/private-network-access/) — deep-dive
- [MDN — Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) — overview

## Technical Details
1. Victim visits `evil.example` controlled by attacker.
2. First DNS answer points to attacker's server — browser loads page, sets cookies for `evil.example`.
3. Attacker lowers TTL; DNS now resolves `evil.example` → `192.168.1.1` (router) or `127.0.0.1`.
4. JavaScript on the still-open page fetches `http://evil.example/admin` — browser sends request to **internal** target, appearing same-origin.

```
Time T0: evil.example → 203.0.113.50 (attacker)
Time T1: evil.example → 127.0.0.1       (victim loopback)
Browser: same host label, different IP — bypasses naive IP pinning
```

| Layer | Defense |
|-------|---------|
| **Browser** | DNS pinning removed; rely on other checks; Private Network Access (Chrome) prompts for public→private fetches |
| **Application** | Validate `Host` header; require auth tokens; do not trust localhost listeners without auth |
| **Service binding** | Bind admin UIs to localhost only with token; use Unix sockets |
| **DNS** | Block external resolution of internal names (split horizon) |
| **Network** | Firewall internal services from client subnets |

- **Developer checklist:** 

- Never assume "only our JS runs on this origin" when DNS is attacker-controlle…
- Use **HTTPS** with correct certificates
- Implement **CSRF tokens** and **Origin/Referer** checks on state-changing API…

- Tools like `rbndr.us` demonstrate rebinding in controlled environments (autho…

## Mistakes to Avoid
- **Mistake:** Binding admin UIs to all interfaces without authentication
- **Mistake:** Trusting “private IP” alone as a security boundary for browser-r…
- **Mistake:** Skipping Host/Origin validation because “our SPA is the only cli…

## Pros/Cons or Trade-offs
- **Pro (mitigations):** Private Network Access and mandatory auth shrink the a…
- **Con (pure DNS pinning):** historically brittle and largely abandoned
- **Con:** HTTPS helps but fails open if the internal service is cleartext HTTP.

## Comparison
- vs [[CORS (Cross Origin Request Sharing)]]: CORS constrains cross-origin XHR
- vs [[mDNS]] spoofing: link-local name lies vs flipping global DNS for a browser origin.


### Use cases
- Hardening home routers, developer dashboards on `:3000`, and IoT admin UIs ag…

- **Example:** A Node debugger bound to `0.0.0.0` without auth is reachable aft…
