is small DNS OS component (OS/library client component) running on machine that handles DNS lookup on behalf of applications.
**Application -> Stub resolver -> DNS resolver -> Authoritative DNS server**

```bash
resolvectl status; # see details about the uplink DNS servers currently in use.
```
- you need to inspect to discover **which upstream DNS server `systemd-resolved` is actually using.** 

look for `resolv.conf mode: stub` if you see, you applications are talking to the local `systemd-resolved`  stub resolver.

The browser asks the **OS stub resolver** to resolve the name. Then the stub resolver sends a DNS query to a configured **recursive DNS resolver**

```txt
Your application
      ↓
Stub Resolver
      ↓
Recursive DNS Resolver
      ↓
Root DNS
      ↓
.com DNS
      ↓
google.com Authoritative DNS
      ↓
IP address
```

The stub resolver usually **doesn't perform the entire DNS resolution process itself.** instead, it knows:
- the domain name it needs resolved
- which DNS server to ask
- sometimes a local DNS cache
- how to send/receive DNS queries `/etc/resolv.conf`

```txt
The stub resolver can send

A www.google.com?

to 8.8.8.8 which performs the recursive resolution.
```

> "A DNS resolver is the client-side DNS component that receives hostname resolution requests from applications and forwards them to a recursive DNS resolver."

`systemd-resolved` provide a local DNS stub listener (commonly `127.0.0.1`) while itself handling caching and forwarding.

`/etc/resolve.conf` it is the configuration file that tells programs **where to send DNS queries and how to perform name resolution.**

```txt
nameserver 127.0.0.53
options edns0 trust-ad
search .
```
`nameserver 127.0.0.53` local stub resolver **local address**. The application talks to the local `systemd-resolved` stub.

multiple nameserver entries, you can have upstream DNS servers that applications can query directly.

```txt
8.8.8.8       → Google DNS
1.1.1.1       → Cloudflare DNS
9.9.9.9       → Quad9 DNS
192.168.1.1   → typically your router
```
The resolver configuration supports multiple `nameserver` lines, with resolver behavior determining how they are tried.

`search` This defines a **search domain.** if you type `ssh server1` the resolver can try `server1.example.com` instead of requiring you to type the full hostname. **This is common in corporate/internal networks.**
