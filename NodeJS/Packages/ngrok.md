[[NodeJS]] [[Packages/npm packages]] [[HTTP module]]

# ngrok

> Tunnel localhost to a public HTTPS URL — demo webhooks and mobile clients without deploying.

## Mental model

**Say it in one breath:** ngrok agent opens an outbound tunnel to ngrok’s edge; the edge gives you `https://….ngrok…` that forwards to `localhost:PORT`.

```txt
Internet → ngrok edge → agent → http://127.0.0.1:3000
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Authtoken** | Account credential | “Required for modern agents.” |
| --- | --- | --- |
| **http 3000** | Local target | “Forwards to your Node server.” |
| **Ephemeral URL** | Changes each free session | “Update webhook config.” |

## Standard config / commands

```bash
ngrok config add-authtoken <TOKEN>
ngrok http 3000
# https://xxxx.ngrok-free.app → http://localhost:3000
export EDITOR=vim   # then: ngrok config edit
```

```bash
npm install -g ngrok   # or apt package from ngrok’s repo
```

| Knob | Why it matters |

| Authtoken | Auth to your account |
| --- | --- |
| Region | Latency to you / peers |
| Reserved domain | Stable URL (paid) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Auth errors | Missing token | `config add-authtoken` |
| 502 from edge | Local app down | Start server on that port |
| Webhook signature fail | Wrong URL / body | Use current URL; raw body |
| Browser interstitial | Free tier warning page | Header bypass or paid plan |

## Gotchas

> [!WARNING]
> **Public = attack surface** — don’t expose admin UIs without auth.

> [!WARNING]
> **URL changes** — free tunnels aren’t stable; pin a domain for demos that matter.

## When NOT to use

- **Production ingress** — real DNS + LB/CDN.
- **Private corporate networks only** — VPN / Tailscale may fit better.

## Related

[[HTTP module]] [[expressjs]] [[Packages/npm packages]]
