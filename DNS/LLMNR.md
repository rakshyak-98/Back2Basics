[[DNS]] · [[mDNS]] · [[UDP]] · [[localhost]]

# LLMNR

> Link-Local Multicast Name Resolution lets Windows hosts resolve single-label names on the local subnet without DNS — convenient on LANs, dangerous on coffee-shop Wi-Fi because any peer can answer.

---

## Protocol summary

LLMNR ([RFC 4795](https://datatracker.ietf.org/doc/html/rfc4795), obsoleted by [RFC 9363](https://datatracker.ietf.org/doc/html/rfc9363) updates) uses multicast **224.0.0.252:5355** (IPv4) and **ff02::1:3** (IPv6). Queries look like DNS but stay on the link.

```
Workstation: "FILESERVER" (single label)
Multicast query → another host claims the name
```

Used when DNS fails for non-FQDN names and NetBIOS is unavailable.

## Windows behavior

Enabled by default on many Windows versions for **private** network profiles. Corporate hardening often disables LLMNR via Group Policy because it enables **credential relay** and **name spoofing** attacks (Responder, mitm6).

## Disable (enterprise)

Group Policy:

```
Computer Configuration → Administrative Templates → Network → DNS Client
→ Turn off multicast name resolution = Enabled
```

PowerShell (verify policy precedence):

```powershell
Get-ItemProperty HKLM:\Software\Policies\Microsoft\Windows NT\DNSClient
```

## vs [[mDNS]] and [[DNS]]

| Mechanism | Name shape | Typical environment |
|-----------|------------|---------------------|
| **DNS** | FQDN `host.example.com` | Global, server-based |
| **mDNS** | `host.local` | Apple/Linux LAN |
| **LLMNR** | `HOSTNAME` single label | Windows LAN fallback |

## Defense

- Disable LLMNR/NetBIOS on servers that do not need it
- Require **SMB signing**, **LDAP signing**, **Kerberos** with SPN validation
- Segment sensitive VLANs; treat workstation subnets as hostile

## Recall

- Why do penetration testers love LLMNR on flat networks?
- When does Windows choose LLMNR over [[DNS]]?

## Sources

- [RFC 4795 — LLMNR](https://datatracker.ietf.org/doc/html/rfc4795)
- [Microsoft — LLMNR overview](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-llmnr/)
