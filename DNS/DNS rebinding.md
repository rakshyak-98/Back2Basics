[[DNS]] [[localhost]] [[CORS (Cross Origin Request Sharing)]] [[Security]] [[dns record]]

# DNS rebinding

> DNS rebinding tricks a browser into treating an attacker-controlled hostname as same-origin with an internal IP — the attack rotates DNS answers from a public IP to `127.0.0.1` or RFC1918 space after the same-origin check passes.

## Interview Relevance

Security and frontend interviews use this to test same-origin policy depth — host vs IP — and whether you secure localhost/admin UIs beyond “it’s only local.”

## Sources

- [Stanford — DNS Rebinding Protection in Web Browsers](https://crypto.stanford.edu/dns/dns-rebinding.pdf) — deep-dive
- [W3C Private Network Access](https://wicg.github.io/private-network-access/) — deep-dive
- [MDN — Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) — overview

## Key Concepts

- **Same-origin is scheme + host + port** — not the IP behind the name.
- **Short TTL:** lets the attacker flip A/AAAA after the page loads ([[dns record]]).
- **Target space:** loopback and RFC1918 routers/admin panels are common victims.
- **Defense in depth:** browser Private Network Access, Host checks, auth tokens, network firewalls.

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

**Developer checklist**

- Never assume "only our JS runs on this origin" when DNS is attacker-controlled.
- Use **HTTPS** with correct certificates — internal IPs will fail cert validation unless attacker also forges certs.
- Implement **CSRF tokens** and **Origin/Referer** checks on state-changing APIs.

Tools like `rbndr.us` demonstrate rebinding in controlled environments (authorized lab only).

## Real-World Applications

Hardening home routers, developer dashboards on `:3000`, and IoT admin UIs against hostile web pages.

**Example:** A Node debugger bound to `0.0.0.0` without auth is reachable after rebinding even if you thought “only localhost clients exist.”

## Pros/Cons or Trade-offs

- **Pro (mitigations):** Private Network Access and mandatory auth shrink the attack surface.
- **Con (pure DNS pinning):** historically brittle and largely abandoned — do not rely on it alone.
- **Con:** HTTPS helps but fails open if the internal service is cleartext HTTP.

## Comparison

- vs [[CORS (Cross Origin Request Sharing)]]: CORS constrains cross-origin XHR; rebinding stays same-origin by keeping the host label.
- vs [[mDNS]] spoofing: link-local name lies vs flipping global DNS for a browser origin.

## Mistakes to Avoid

- Binding admin UIs to all interfaces without authentication.
- Trusting “private IP” alone as a security boundary for browser-reachable services.
- Skipping Host/Origin validation because “our SPA is the only client.”
