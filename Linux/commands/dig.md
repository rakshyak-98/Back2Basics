- `dig` expects a hostname only - on schema `https://` no path `/`, no port `443`.

```bash
dig google.com; # correct
dig https://google.com; # wrong
```

- `NOERROR` -> means DNS resolution was successful (no errors like `NXDOMAIN`).
- ANSWER SECTION -> subdomain resolves to n number of IPv4 addresses (A records).
- TTL -> will be cached that long unless manually flushed.