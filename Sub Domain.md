user enters a subdomain in browser

## DNS record

| Type    | Name               | Purpose                                                 |
| ------- | ------------------ | ------------------------------------------------------- |
| `A`     | Address            | Maps domain → **IPv4** address                          |
| `AAAA`  | IPv6 Address       | Maps domain → **IPv6** address                          |
| `CNAME` | Canonical Name     | Points a domain → another domain (alias)                |
| `MX`    | Mail Exchange      | Routes email → mail servers                             |
| `NS`    | Name Server        | Delegates DNS → authoritative name servers              |
| `SOA`   | Start of Authority | Metadata: primary NS, admin email, serial, refresh TTLs |
