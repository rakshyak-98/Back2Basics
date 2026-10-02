# DNS Explained Simply: What Really Happens When You Type a Domain Name

You type `example.com` into your browser and a page appears. It feels instant, almost boring. But between your keypress and the first byte of the page, a small chain of servers has quietly answered one question: **where is this thing?**

That question is what DNS answers. This post walks through how, in the order you'd actually meet the pieces. There's no jargon dump, just one idea building on the last.

---

## 1. DNS is the internet's phone book

Computers talk to each other with numbers (IP addresses like `203.0.113.5`). People remember names. DNS is the translation layer between the two.

A DNS server is just a normal server with one job. Instead of serving web pages on port 80 or 443, it listens on **port 53** and answers questions like "what's the IP for `example.com`?"

And yes, one machine can do many jobs at once: DNS on 53, a website on 443, SSH on 22, a database on 5432. Each is a separate process listening on its own port.

## 2. Why isn't there just one giant phone book?

It sounds like the obvious design: one central server that knows every domain. But no single organisation could run it, and one outage would take the whole internet down with it.

So DNS is **hierarchical and distributed**. Each group manages only its own slice, and each level knows who to ask next.

```
.  (root)
└── .com  (TLD)
    └── example.com  (your domain)
        └── www.example.com
```

Read a domain name right to left and you're walking down the tree.

## 3. The journey of one lookup

When your browser needs `example.com`, this is what happens:

```
Your app
   ↓
Stub resolver        (small helper built into your OS)
   ↓
Recursive resolver   (your ISP, 8.8.8.8, 1.1.1.1 ...)
   ↓
Root server          "Who handles .com?"
   ↓
.com TLD server      "Who handles example.com?"
   ↓
Authoritative server "example.com is 203.0.113.5"
```

The cast:

- **Stub resolver:** a tiny client on your machine. It doesn't do the hard work, it just forwards your question to someone who does. On many Linux systems it's `systemd-resolved` listening on `127.0.0.53`.
- **Recursive resolver:** the one that does the legwork. It walks the chain above and hands you the final answer.
- **Authoritative server:** the source of truth for the domain. It doesn't guess or remember, it *owns* the records.

The recursive resolver also **caches** every answer. The next person to ask gets it instantly, without repeating the whole chain.

## 4. Records: what's actually stored

A DNS server stores **records**, small entries that say "for this name, here's a fact." These are the ones you'll use most:

| Record | What it does |
|---|---|
| **A** | Name → IPv4 address |
| **AAAA** | Name → IPv6 address |
| **CNAME** | Alias to another name |
| **MX** | Which mail server accepts email for the domain |
| **NS** | Which nameservers are in charge of the domain |
| **TXT** | Free text, used for SPF/DKIM/DMARC and ownership verification |
| **CAA** | Which certificate authorities may issue TLS certs for you |

Two things that trip people up:

- **A CNAME is not a redirect.** Pointing `www` at `example.com` doesn't send the browser anywhere. DNS just resolves the name, and the browser still asks for `www.example.com`.
- **An MX record points to a hostname, not an IP.** The sender's mail server first looks up the MX, then looks up that hostname's A record, then connects.

## 5. Zones and delegation

This is the part that confuses most people, and it's simple once you see it.

A **domain** is a piece of the naming tree. A **zone** is the piece of that tree that a particular set of nameservers is actually responsible for.

Here's the surprise: creating `api.example.com`, `stage.example.com` and `prod.example.com` does **not** create new zones. They're just names *inside* the `example.com` zone. They can point to the same IP or completely different ones, and it doesn't matter.

A subdomain becomes its own zone only through **delegation**. That means telling the world:

> "For `dev.example.com` and everything below it, ask *these other* nameservers."

```
example.com.       NS   ns1.example-dns.com.
dev.example.com.   NS   ns1.dev-dns.com.     ← now a separate zone
```

This is how big organisations let different teams run their own DNS without stepping on each other.

It's also why you always run **more than one nameserver**. If all the parent's nameservers go down, a resolver that has never seen your delegation before can't find your child zone. Cached resolvers keep working, but new ones struggle. Redundancy at every level is built into DNS on purpose.

## 6. TTL, caching, and the myth of "propagation"

Every record carries a **TTL** (time to live), a number of seconds that says "you may cache this answer for this long."

That's the whole story behind "DNS propagation." Nothing is really being pushed around the world. Different resolvers simply hold old answers until their timers expire.

That's why you sometimes see this:

```
nslookup mysite.com 8.8.8.8   →  NXDOMAIN
nslookup mysite.com 1.1.1.1   →  203.0.113.5
```

Nothing is broken. Google's resolver cached the "doesn't exist" answer before you added the record (or hasn't asked yet), while Cloudflare's already picked up the new one.

**Practical tip:** lower your TTL a day or two *before* a migration, then raise it again afterwards. Even non-existent names get cached, based on the zone's SOA timer.

## 7. One thing DNS does *not* do: ports

A very common misunderstanding: DNS gives you an IP address, **not a port**.

An A record says `example.com → 203.0.113.5`. That's it. The port comes from the protocol (`https://` means 443) or from you typing it (`:3000`).

So if your app runs on port 3000, users won't magically reach it via DNS. You put a reverse proxy like Nginx on ports 80/443 and let it forward to your app.

## 8. Debugging DNS with `dig`

When something's off, `dig` is your best friend. These few commands cover most situations:

```bash
# Simple lookups
dig example.com A +short
dig example.com MX +short

# Ask a specific resolver (bypass your local one)
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Who's authoritative for this domain?
dig +short NS example.com

# Walk the whole chain from the root
dig +trace example.com

# Ask the authoritative server directly (no cache)
dig example.com @ns1.example.com +norecurse

# Reverse lookup (IP → name)
dig -x 93.184.216.34 +short
```

**`dig +trace` is the one to remember.** It shows each hop:

1. **Root** points you to the `.com` servers.
2. **TLD** points you to your domain's nameservers.
3. **Authoritative** gives the final answer.

Wherever the trace stops is where your problem lives. If the chain breaks at the TLD step, look at your NS settings at the registrar. If it reaches the authoritative server and the record isn't there, fix your zone.

## 9. Quick troubleshooting cheatsheet

| Symptom | Likely cause |
|---|---|
| Works on `1.1.1.1`, fails on `8.8.8.8` | Caching or timing, wait for TTL to expire |
| `NXDOMAIN` for a name that should exist | Missing record, or wrong NS at the registrar |
| `SERVFAIL` | Often a broken DNSSEC setup (DS record mismatch) |
| Intermittent wrong IP | Several records or geo-DNS, check every authoritative server |
| Site works by IP but not by name | DNS problem, not a server problem |
| Old IP after migration | Old TTL still cached, wait it out |

## 10. Gotchas worth knowing

- **No CNAME at the root domain.** A CNAME can't coexist with other records like MX and TXT, and your apex has those. Use an A record, or your provider's ALIAS/ANAME feature.
- **Your registrar and your DNS host can be different companies.** If the domain expires at the registrar, your DNS zone stops working even though it still exists at your DNS host.
- **The `search` domain can surprise you.** On some networks, `curl api` might try `api.internal` first. In scripts, use the full name.
- **Sanity-check `resolv.conf`.** If it says `nameserver 127.0.0.53`, your machine is using the local `systemd-resolved` stub. Run `resolvectl status` to see the real upstream.
- **Managed DNS beats self-hosting for most teams.** Route 53 or Cloudflare will save you from running BIND yourself, unless you have a specific reason to.

## Wrapping up

Here's the whole picture in a few lines:

- DNS turns names into IP addresses, and nothing more.
- It's a **tree**, and each level knows who to ask next.
- **Resolvers** look things up for you and **cache** the results.
- **Authoritative servers** own the truth for their zone.
- **Delegation** is what creates zones, not subdomains.
- **TTL** explains nearly every "DNS is slow to update" story.
- When stuck, run **`dig +trace`** and find where the chain breaks.

Next time a site "isn't loading," you'll have a good idea of which link in the chain to check first.

*Got a DNS horror story or a question I didn't cover? Drop it in the comments.*
