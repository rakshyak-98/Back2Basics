[[DNS]] · [[localhost]] · [[CORS (Cross Origin Request Sharing)]] · [[Security]]

# DNS rebinding

> DNS rebinding tricks a browser into treating an attacker-controlled hostname as same-origin with an internal IP — the attack rotates DNS answers from a public IP to `127.0.0.1` or RFC1918 space after the same-origin check passes.

---

## Attack shape

1. Victim visits `evil.example` controlled by attacker.
2. First DNS answer points to attacker's server — browser loads page, sets cookies for `evil.example`.
3. Attacker lowers TTL; DNS now resolves `evil.example` → `192.168.1.1` (router) or `127.0.0.1`.
4. JavaScript on the still-open page fetches `http://evil.example/admin` — browser sends request to **internal** target, appearing same-origin.

```
Time T0: evil.example → 203.0.113.50 (attacker)
Time T1: evil.example → 127.0.0.1       (victim loopback)
Browser: same host label, different IP — bypasses naive IP pinning
```

Documented in academic and industry literature (e.g. Stanford Web Security research); mitigations evolved with browsers and server design.

## Why it works

Browsers historically keyed same-origin policy on **scheme + host + port**, not IP. Short TTLs ([[dns record]]) enable flip after initial page load.

## Mitigations

| Layer | Defense |
|-------|---------|
| **Browser** | DNS pinning removed; rely on other checks; Private Network Access (Chrome) prompts for public→private fetches |
| **Application** | Validate `Host` header; require auth tokens; do not trust localhost listeners without auth |
| **Service binding** | Bind admin UIs to localhost only with token; use Unix sockets |
| **DNS** | Block external resolution of internal names (split horizon) |
| **Network** | Firewall internal services from client subnets |

## Developer checklist

- Never assume "only our JS runs on this origin" when DNS is attacker-controlled.
- Use **HTTPS** with correct certificates — internal IPs will fail cert validation unless attacker also forges certs.
- Implement **CSRF tokens** and **Origin/Referer** checks on state-changing APIs.

## Testing (authorized lab only)

Tools like `rbndr.us` demonstrate rebinding in controlled environments.

## Recall

- Why does HTTPS often block rebinding even when DNS flips?
- How does Private Network Access change public sites calling `192.168.x.x`?

## Sources

- [Stanford — DNS Rebinding Protection in Web Browsers](https://crypto.stanford.edu/dns/dns-rebinding.pdf)
- [W3C Private Network Access](https://wicg.github.io/private-network-access/)
- [MDN — Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
