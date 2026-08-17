[[Commands]] [[ss]] [[netstat]] [[lsof]] [[ip]] [[dig]] [[nc]] [[ufw]]

# Linux network commands

> Pocket kit for “is it listening, reachable, or DNS?” — ss/lsof for sockets, nc/tcpdump to probe, dig/resolvectl for names.

```txt
        Linux network comm ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Incident first five minutes: listening ports, route, DNS, and reachability

## Sources
- [ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html) — deep-dive
- [tcpdump(1)](https://www.tcpdump.org/manpages/tcpdump.1.html) — overview

## Key Concepts
- **Listen vs reach:** Something bound locally ≠ remote can connect.
- **ss over netstat:** Modern socket stats; netstat may be absent.
- **DNS vs NSS:** `dig` is DNS; `getent hosts` follows nsswitch.
- **Cloud + host firewall:** Both must allow the path.
- **Capture sparingly:** tcpdump is powerful and noisy.


- **Core:** Map the question to a tool: local listen → `ss`/`lsof`

## Technical Details
```txt
Listen?  ss -lntup / lsof -i
Reach?   nc -zv host port
Route?   ip route get 1.1.1.1
Name?    dig +short / resolvectl
Packets? tcpdump -ni eth0 port 443
```

```bash
ss -lntup
ss -tnp | head
sudo lsof -iTCP:443 -sTCP:LISTEN

ip route get 1.1.1.1
nc -zv -w 3 host 443
dig +short example.com
resolvectl query example.com

sudo tcpdump -ni eth0 port 443
sudo ufw status verbose
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `ss -lntup` | Start service; fix bind |
| Timeout | `nc -zv`; route; SG/ufw | Open path both sides |
| Wrong IP used | `dig` vs `getent hosts` | Fix DNS/nsswitch/search |
| netstat missing | package | Use `ss` |

## Mistakes to Avoid
- **Mistake:** Testing with `ping` when the app is TCP/TLS-only
- **Mistake:** Ignoring cloud firewall when host ufw looks open
- **Mistake:** Leaving debug listeners or aggressive scans on shared hosts

## Pros/Cons or Trade-offs
- **Pro:** Fast layered diagnosis without an APM.
- **Con:** Easy to over-scan (`nc`/`nmap`) and trip IDS.
- **Trade-off:** Quick `nc` vs scoped [[nmap]] audits.

## Comparison
- vs [[ip]]: L3 objects


### Use cases
- “Port open in cloud console but app times out” triage, confirming nginx liste…
