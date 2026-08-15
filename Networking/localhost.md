[[Networking]] [[loopback]] [[non-Routable address]] [[address port]] [[Internal routing]]

# localhost

> `localhost` always means “this device” — the machine running the code, not your laptop by magic.

## Interview Relevance

Interviewers use localhost to catch bind/listen mistakes: phones and containers each have their own loopback — “works on my machine” often means the client hit the wrong host’s `127.0.0.1`.

## Sources

- [RFC 1122 — Requirements for Internet Hosts (loopback)](https://www.rfc-editor.org/rfc/rfc1122) — deep-dive
- [RFC 4291 — IPv6 Addressing Architecture (`::1`)](https://www.rfc-editor.org/rfc/rfc4291) — overview
- [Wikipedia — localhost](https://en.wikipedia.org/wiki/Localhost) — overview

## Core Definition

`localhost` is the conventional hostname for the loopback interface (`127.0.0.1` / `::1`); traffic never leaves the host that resolves and connects to it.

## Key Concepts

- **localhost:** hostname for loopback → always the local OS network stack.
- **127.0.0.1 / ::1:** IPv4 / IPv6 loopback → never leaves the host.
- **0.0.0.0 listen:** accept on all interfaces → needed so LAN devices can connect.
- **Host LAN IP:** address on Wi‑Fi/Ethernet → phones and VMs use this, not localhost.
- **10.0.2.2:** Android emulator → host → special alias to the development machine.

## Technical Details

```txt
Browser on laptop  →  http://localhost:3000  →  laptop
App on phone       →  http://localhost:3000  →  phone (empty)
Phone → laptop API →  http://192.168.1.50:3000
```

| Where the app runs | What `http://localhost:3000` hits |
|--------------------|-----------------------------------|
| Your Linux desktop | Your desktop |
| Android emulator | Emulator itself — use `10.0.2.2` for the host |
| Physical phone | The phone — use the PC’s LAN IP instead |
| Docker container | The container — use `host.docker.internal` or host gateway IP |

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

### HTTPS on localhost (mkcert)

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

| Symptom | Check | Fix |
|---------|-------|-----|
| Phone “unable to connect” | URL is `localhost` | Use laptop LAN IP; bind `0.0.0.0` |
| Works in browser, not emulator | Used `127.0.0.1` in Android | Use `10.0.2.2` |
| CORS / mixed content | HTTP page → HTTPS API | Serve both HTTPS via mkcert |
| Container can’t reach host API | `localhost` inside container | Host gateway / `extra_hosts` |
| Only IPv6 or only IPv4 fails | `localhost` → `::1` vs `127.0.0.1` | Pin family or listen on both |

## Real-World Applications

Local development servers, health checks bound to loopback, and mkcert HTTPS for browser APIs that require secure contexts.

**Example:** A phone can’t open the Vite app at `http://localhost:3000` — use the laptop’s LAN IP and bind `0.0.0.0`.

## Pros/Cons or Trade-offs

- **Pro:** Safe default for local-only services — no LAN exposure when bound to `127.0.0.1`.
- **Con:** Confuses cross-device demos — each device’s localhost is itself.
- **Con:** IPv4 vs IPv6 resolution order can make `localhost` hit the wrong family.

## Comparison

- vs [[loopback]]: localhost is the hostname convention; loopback is the interface/address family.
- vs LAN IP / `0.0.0.0`: required when other devices must connect.
- vs production DNS names: never ship “localhost” as a service URL.

## Mistakes to Avoid

- Treating localhost as “the backend server” — each process namespace has its own loopback.
- Binding `127.0.0.1` then wondering why remote health checks fail.
- Assuming localhost bypasses authentication on multi-user hosts.
- Forgetting phone CA trust when testing HTTPS on the LAN with mkcert.
