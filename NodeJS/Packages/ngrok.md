[[NodeJS]] [[Packages/npm packages]] [[HTTP module]] [[expressjs]]

# ngrok

> Tunnel localhost to a public HTTPS URL — demo webhooks and mobile clients without deploying.

```txt
        ngrok ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **ngrok** to check whether you can explain the mechanism in …

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

## Mistakes to Avoid
- **Mistake:** **Public = attack surface** — don’t expose admin UIs without auth
- **Mistake:** **URL changes**
- **Mistake:** **Auth errors:** check Missing token; fix: `config add-authtoken`
- **Mistake:** **502 from edge:** check Local app down
- **Mistake:** **Webhook signature fail:** check Wrong URL / body
- **Mistake:** **Browser interstitial:** check Free tier warning page

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Tunnel localhost to a public HTTPS URL — demo webhooks and mobile clients withou…).
- **Con / when not:** **Production ingress** — real DNS + LB/CDN.
- **Con / when not:** **Private corporate networks only**

## Comparison
- vs [[Packages/npm packages]]: know when each applies


### Use cases
- In production APIs and tooling, **ngrok** shows up whenever teams ship Node/J…
