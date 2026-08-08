[[DNS]]

# DNS server

> DNS server — answers name lookups so clients find IP addresses for a host.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

(Domain Name System server) is like the internet's phone book.
When you type a website name such a google.com your computer doesn't actually use that name to find the website. It needs the website's numerical IP address, such as `142.250.xxx.xxx`
- Instead of running an HTTP server, it runs DNS server software.
- Instead of listening on port 80 or 443, it listen on 53
A DNS server store DNS records
```txt
example.com
A Record
---------
example.com → 203.0.113.5
AAAA Record
------------
example.com → 2001:db8::1
MX Record
----------
example.com → mail.example.com
CNAME
-------
www.example.com → example.com
```
- Usually these records are stored in, Zone files, Database (for management DNS providers)
- In memory cache
What software is inside ?
Popular DNS server software
> [!INFO]
> ## Can one machine do both?
>

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
