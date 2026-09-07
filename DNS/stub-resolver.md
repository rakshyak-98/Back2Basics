is small DNS client component (OS/library component) running on machine that handles DNS lookup on behalf of applications.
**Application -> Stub resolver -> DNS resolver -> Authoritative DNS server**

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
