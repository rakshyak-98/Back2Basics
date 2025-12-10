user enters a subdomain in browser

## DNS record

| Type    | Name               | Purpose                                                        |
| ------- | ------------------ | -------------------------------------------------------------- |
| `A`     | Address            | Maps hostname → **IPv4** address                               |
| `AAAA`  | IPv6 Address       | Maps hostname → **IPv6** address                               |
| `CNAME` | Canonical Name     | Points a domain → another domain (alias).                      |
| `MX`    | Mail Exchange      | specifies **mail server(s)** responsible for receiving emails. |
| `NS`    | Name Server        | Points to authoritative DNS servers for the domain.           |
| `SOA`   | Start of Authority | Metadata: primary NS, admin email, serial, refresh TTLs        |
Authoritative DNS server -> An **authoritative DNS server** is a DNS server that **has the final, official answer** for a domain’s DNS records (A, MX, CNAME, etc).

It holds the **zone file** — the actual record set configured by the domain owner.