`dig` reads system configuration DNS server (often from `/etc/resolve.conf`) and sends the DNS query directly to it.

```sh
dig +short google.com; # out ip only
dig @8.8.8.8 google.com; # DNS
```
- you can control the DNS query **what is actually happening in DNS,** because you can control the query and see the response directly.

## Basic: Does DNS resolve the name?
```bash
dig google.com
```

```txt
;; QUESTION SECTION:
;google.com.        IN      A

;; ANSWER SECTION:
google.com.  300   IN      A   142.250.x.x
```

A -> IPv4 address
AAAA -> Ipv6 address
ANSWER SECTION -> DNS actually returned an answer
300 -> TTL, in seconds

if you get an answer, basic DNS resolution is working.

 > [!INFO]
 > no "ANSWER SECTION": In `dig <domain>`, it usually means the queried name didn't return any authoritative or resolved data.
 
 Common reasons
1. No DNS record exists
	 - The domain or specific record type (A, AAA, CNAME) is missing.
	 - Example: querying an `A` record for a subdomain that hasn't been created.
2. NXDOMAIN (Non-Existent Domain)
	- The domain itself does not exist.
	- In `dig` output, you'll see

```text
status: NXDOMAIN
```

3. Query type mismatch

- You requested a type that isn't present.
```bash
dig <domain> MX;
```
- if no `MX` record exists, Answer section is empty.

4. Propagation/Caching issues
- DNS changes not propagated yet.
- Local resolver may not have the record cached.

## Get only the IP address
```bash
dig +short google.com
dig +short AAAA google.com
```
- quick connectivity checks.

```bash
dig +trace <domain>; # Follows the DNS chain to authoritative server.
dig @8.8.8.8 <domain>; # you can choose the DNS server. Query goes directly to Google public DNS resolver.
```

Compare
```bash
dig @8.8.8.8 google.com
dig @1.1.1.1 google.com
```
if one works and another doesn't, you've isolated the problem to the resolver/path rather than the domain itself.

```txt
> dig google.com

; <<>> DiG 9.18.39-0ubuntu0.24.04.7-Ubuntu <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41958
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             13      IN      A       142.251.43.238

;; Query time: 34 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Mon Sep 07 11:53:16 IST 2026
;; MSG SIZE  rcvd: 55

```

`;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)` The DNS server the `dig` sent the query to.

```bash
resolvectl status; # check which dns server is used by current config.
```

- `dig` expects a hostname only - on schema `https://` no path `/`, no port `443`.

```bash
dig google.com; # correct
dig https://google.com; # wrong

```

## Diagnostics (trace)

```bash
dig +trace google.com
```
- this makes `dig` perform iterative resolution starting from the DNS root. You will see the delegation chain.

## Check whether DNS is returning an error

| Status     | Meaning                              |
| ---------- | ------------------------------------ |
| `NOERROR`  | Query succeeded                      |
| `NXDOMAIN` | Domain name does not exist           |
| `SERVFAIL` | DNS server failed to resolve it      |
| `REFUSED`  | Server refused the query             |
| `FORMERR`  | Malformed query                      |
| `NOTIMP`   | Query type/operation not implemented |

- `NOERROR` -> means DNS resolution was successful (no errors like `NXDOMAIN`).
- ANSWER SECTION -> subdomain resolves to n number of IPv4 addresses (A records).
- TTL -> will be cached that long unless manually flushed.

> [!INFO]
> public resolvers -> DNS servers operated by third parties, open for anyone to use instead of your ISP's DNS. They translate domain names -> IP addresses.

```txt
;; flags: qr rd ra;
```

rd = Recursion Desired "Please recursively resolve this for me."
ra = Recursion Available "I support recursion."

**Check DNS response time**
```txt
;; Query time: 24 msec
```

## Diagnose why domain doesn't show an ANSWER SECTION

```bash
dig <domain>;
```
- if `status: NXDOMAIN` -> domain does not exist.
- if no NXDOMAIN but empty answer -> record type may be missing.

**Specify record type**
```bash
dig <domain> A # IPV4
dig <domain> AAAA # IPV6
dig <domain> CNAME # CNAME
dig <domain> MX # mail server
```
- some time the domain exists, but the type you asked doesn't.

**Check authoritative server**

```bash
dns NS <domain>;
```
- list authoritative `nameservers`.
- if missing -> DNS misconfigured at registrar.

**Query authoritative server directly**

```bash
dig @ns1.example-NS.com yourdomain.com A
```
- bypass local resolver caching.
- Shows whether authoritative server actually has the record.

**Check propagation/caching**
```bash
dig @8.8.8.8 <domain>;
dig @1.1.1.1 <domain>;
```
- check public resolvers to see if record is propagated globally

**Optional: Check zone file / hosting panel**
- if you control the domain, verify
	- A/CNAME records exist for requested hostname.
	- No typos in subdomain names.
	- TTL isn't too high (causing stale cache).

## DNS caching

"A recursive DNS resolver normally checks its cache before going out to the DNS hierarchy."

if you run the query repeatedly against the **same recursive resolver**, you may observe, the decreasing value is evidence that the resolver is serving a cached record whose TTL is counting down. Once the TTL expires, the resolver need to obtain a fresh answer.

The cache belongs to the **recursive resolver**, not the `dig`

```txt
1. Does DNS answer?
       ↓
   dig example.com

2. Which resolver answered?
       ↓
   SERVER: ...

3. Is the resolver returning a cached answer?
       ↓
   Check TTL / compare repeated queries

4. Try another recursive resolver
       ↓
   dig @8.8.8.8 example.com

5. Query authoritative DNS
       ↓
   dig example.com NS
   dig @authoritative-server example.com

6. Trace delegation
       ↓
   dig +trace example.com
```

```txt
                 DNS Resolution
                       │
                       ▼
                 Stub Resolver
                       │
                       ▼
              Recursive Resolver
                       │
                 ┌─────┴─────┐
                 │           │
              CACHE       Cache Miss
                 │           │
                 │           ▼
                 │       Root DNS
                 │           ↓
                 │       TLD DNS
                 │           ↓
                 │   Authoritative DNS
                 │           │
                 └─────┬─────┘
                       ▼
                    Answer
```