[[NodeJS]] [[Packages/npm packages]] [[HTTP module]] [[expressjs]]

# ngrok

> Tunnel localhost to a public HTTPS URL — demo webhooks and mobile clients without deploying.

## Interview Relevance

Interviewers use **ngrok** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Authtoken**, **http 3000**, **Ephemeral URL**.

## Sources

- [ngrok — Docs](https://ngrok.com/docs) — deep-dive
- [Wikipedia — ngrok](https://en.wikipedia.org/wiki/ngrok) — overview

## Key Concepts

- **Authtoken:** Account credential — Required for modern agents.
- **http 3000:** Local target — Forwards to your Node server.
- **Ephemeral URL:** Changes each free session — Update webhook config.

## Technical Details

```txt
Internet → ngrok edge → agent → http://127.0.0.1:3000
```

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
|------|----------------|
| Authtoken | Auth to your account |
| Region | Latency to you / peers |
| Reserved domain | Stable URL (paid) |

## Real-World Applications

In production APIs and tooling, **ngrok** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Public = attack surface** — don’t expose admin UIs without auth; **URL changes** — free tunnels aren’t stable; pin a domain for demos that matter.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Tunnel localhost to a public HTTPS URL — demo webhooks and mobile clients withou…).
- **Con / when not:** **Production ingress** — real DNS + LB/CDN.
- **Con / when not:** **Private corporate networks only** — VPN / Tailscale may fit better.

## Comparison

vs [[Packages/npm packages]]: know when each applies — do not treat them as interchangeable. vs [[HTTP module]]: know when each applies — do not treat them as interchangeable. vs [[expressjs]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Public = attack surface** — don’t expose admin UIs without auth.
- **URL changes** — free tunnels aren’t stable; pin a domain for demos that matter.
- **Auth errors:** check Missing token; fix: `config add-authtoken`
- **502 from edge:** check Local app down; fix: Start server on that port
- **Webhook signature fail:** check Wrong URL / body; fix: Use current URL; raw body
- **Browser interstitial:** check Free tier warning page; fix: Header bypass or paid plan
