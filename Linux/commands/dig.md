```bash
dig +short google.com;
dig @8.8.8.8 google.com;
```
 
 > [!INFO]
 > If `dig <domain>` shows no "ANSWER SECTION", it usually means the queried name didn't return any authoritative or resolved data.
 common reasons
1. No DNS record exists
	 - The domain or specific record type (A, AAA, CNAME) is missing.
	 - Example: querying an `A` record for a subdomain that hasn't been created.
2. NXDOMAIN (Non-Existent Domain)
	- The domain itself does not exist.
	- In `dig` output, you'll see

```bash
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

```bash
dig +trace <domain>; # Follows the DNS chain to authoritative server.
dig @8.8.8.8 <domain>; # check using public resolver.
```


```bash
resolvectl status; # check which dns server is used by current config.
```

- `dig` expects a hostname only - on schema `https://` no path `/`, no port `443`.

```bash
dig google.com; # correct
dig https://google.com; # wrong

```

- `NOERROR` -> means DNS resolution was successful (no errors like `NXDOMAIN`).
- ANSWER SECTION -> subdomain resolves to n number of IPv4 addresses (A records).
- TTL -> will be cached that long unless manually flushed.

> [!INFO]
> public resolvers -> DNS servers operated by third parties, open for anyone to use instead of your ISP's DNS. They translate domain names -> IP addresses.

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
