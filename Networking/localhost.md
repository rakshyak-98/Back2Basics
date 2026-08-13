[[Networking]] [[loopback]] [[non-Routable address]]

# localhost

> `localhost` always means “this device” — the machine running the code, not your laptop by magic.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#What localhost means on each device]]
- [[#HTTPS on localhost (mkcert)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Name resolves to loopback (`127.0.0.1` / `::1`). On a phone or container, that is *their* loopback — not your host.

```txt
Browser on laptop  →  http://localhost:3000  →  laptop
App on phone       →  http://localhost:3000  →  phone (empty)
Phone → laptop API →  http://192.168.1.50:3000
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **localhost** | Hostname for loopback | “Always the local OS network stack.” |
| **127.0.0.1 / ::1** | IPv4 / IPv6 loopback | “Never leaves the host.” |
| **0.0.0.0 listen** | Accept on all interfaces | “Needed so LAN devices can connect.” |
| **Host LAN IP** | Address on Wi‑Fi/Ethernet | “Phones and VMs use this, not localhost.” |
| **10.0.2.2** | Android emulator → host | “Special alias to the development machine.” |

---

## Standard config / commands

```bash
# Your LAN IP (phone / other device should use this)
hostname -I | awk '{print $1}'
ip -4 route get 1.1.1.1 | awk '{print $7; exit}'

# Listen on all interfaces for LAN access
# e.g. vite --host 0.0.0.0   or   listen(3000, '0.0.0.0')
ss -tlnp | grep 3000
```

| Knob | Why it matters |
|------|----------------|
| Bind host | `127.0.0.1` = local only; `0.0.0.0` = LAN-reachable |
| Firewall | UFW/security group must allow the port from LAN |
| `/etc/hosts` | `localhost` → 127.0.0.1; don’t point it at a remote IP |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Phone “unable to connect” | URL is `localhost` | Use laptop LAN IP; bind `0.0.0.0` |
| Works in browser, not emulator | Used `127.0.0.1` in Android | Use `10.0.2.2` |
| CORS / mixed content | HTTP page → HTTPS API | Serve both HTTPS via mkcert |
| Container can’t reach host API | `localhost` inside container | Host gateway / `extra_hosts` |
| Only IPv6 or only IPv4 fails | `localhost` → `::1` vs `127.0.0.1` | Pin family or listen on both |

---

## What localhost means on each device

| Where the app runs | What `http://localhost:3000` hits |
|--------------------|-----------------------------------|
| Your Linux desktop | Your desktop |
| Android emulator | Emulator itself — use `10.0.2.2` for the host |
| Physical phone | The phone — use the PC’s LAN IP instead |
| Docker container | The container — use `host.docker.internal` or host gateway IP |

---

## HTTPS on localhost (mkcert)

```bash
sudo apt install mkcert libnss3-tools
mkcert -install
mkdir -p cert && cd cert
mkcert localhost 127.0.0.1 ::1
# → localhost+2.pem + localhost+2-key.pem
```

```js
// Express
import https from 'https'
import fs from 'fs'
https.createServer({
  key: fs.readFileSync('./cert/localhost+2-key.pem'),
  cert: fs.readFileSync('./cert/localhost+2.pem'),
}, app).listen(3000)
```

```js
// Vite
server: {
  https: {
    key: fs.readFileSync('localhost+2-key.pem'),
    cert: fs.readFileSync('localhost+2.pem'),
  },
  port: 3000,
  host: '0.0.0.0', // if phones need access (still need LAN IP + trust)
}
```

---

## Gotchas

> [!WARNING]
> **localhost is not “the backend server”** — each process namespace has its own loopback.

> [!WARNING]
> **mkcert on phone** — LAN HTTPS needs the phone to trust your local CA (or use HTTP on LAN for rough tests).

> [!WARNING]
> **Binding `127.0.0.1` hides the service** — health checks from other hosts will fail.

---

## When NOT to use

- **Production service URLs** — use real DNS names, not localhost.
- **Cross-device demos with only localhost** — use LAN IP, Tailscale, or a tunnel.
- **Assuming `localhost` bypasses authentication** — still authenticate; loopback is not a security boundary for multi-user hosts.

---

## Related

[[Networking]] [[loopback]] [[non-Routable address]] [[address port]] [[Internal routing]]
