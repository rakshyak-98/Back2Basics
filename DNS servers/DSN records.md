DNS records are entries in a DNS database that tell the internet how to route traffic for a domain.

```txt
example.com
├── A      -> 192.168.1.10
├── AAAA   -> 2001:db8::1
├── MX     -> mail.example.com
├── NS     -> ns1.example.com
├── TXT    -> "v=spf1 ..."
├── CNAME  -> example.com
└── SRV    -> server.example.com:8080
```

## Records

A Record (Address) -> Map a domain to an IPv4 address. Used for APIs Any IPv4 service
AAA (IPv6 address) -> Map domain to IPv6
CNAME (Canonical Name) -> Create an alias to another hostname. Used for `www` CDN endpoints, Aliases
MX (Mail Exchange) -> tells the internet which mail server is responsible for receiving emails for a domain. Without an MX record, other mail servers don't know where to deliver email.
NS (Name Server) -> Specify which DNS servers are authoritative for the domain. Without NS records, the DNS hierarchy cannot find who is responsible for the domain.
TXT -> Store arbitrary text, commonly used for verification and email security. Used for domain ownership verification, email authentication, configuration metadata.
CAA (Certification Authority Authorization) -> Specify which certificate authorities may issue TLS certificates for the domain. If another CA tries to issue a certificate, it should refuse.

## MX

- MX does not contain an IP address, it points to a hostname

```
alice@example.com; # When someone sends

The sender's mail server asks DNS: "Which mail server accepts emails for `example.com`"
```

```txt
Sender
   |
Send email to alice@example.com
   |
Sender Mail Server
   |
DNS Query
MX example.com
   |
DNS Response
mail.example.com
   |
DNS Query
A mail.example.com
   |
203.0.113.50
   |
SMTP Connection
   |
Mail Server
```