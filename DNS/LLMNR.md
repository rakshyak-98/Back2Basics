[[DNS]] [[mDNS]] [[UDP]] [[localhost]]

# LLMNR

> Link-Local Multicast Name Resolution lets Windows hosts resolve single-label names on the local subnet without DNS — convenient on LANs, dangerous on coffee-shop Wi-Fi because any peer can answer.

## Interview Relevance

Windows / security interviews ask why LLMNR is disabled in enterprises — spoofing and credential relay (Responder) are the expected story.

## Sources

- [RFC 4795 — LLMNR](https://datatracker.ietf.org/doc/html/rfc4795) — deep-dive
- [RFC 9363](https://datatracker.ietf.org/doc/html/rfc9363) — deep-dive
- [Microsoft — LLMNR overview](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-llmnr/) — overview

## Key Concepts

- **Link-local multicast:** queries never leave the subnet — no central [[name server]].
- **Single-label names:** fallback when DNS fails for non-FQDN names and NetBIOS is unavailable.
- **Anyone can answer:** on untrusted Wi-Fi, peers can claim `FILESERVER` and steal hashes.
- **Enterprise hardening:** disable via Group Policy; require signing and Kerberos hygiene.

## Technical Details

LLMNR ([RFC 4795](https://datatracker.ietf.org/doc/html/rfc4795), updates in [RFC 9363](https://datatracker.ietf.org/doc/html/rfc9363)) uses multicast **224.0.0.252:5355** (IPv4) and **ff02::1:3** (IPv6). Queries look like DNS but stay on the link.

```
Workstation: "FILESERVER" (single label)
Multicast query → another host claims the name
```

Enabled by default on many Windows versions for **private** network profiles. Corporate hardening often disables LLMNR via Group Policy because it enables **credential relay** and **name spoofing** attacks (Responder, mitm6).

**Disable (enterprise)** — Group Policy:

```
Computer Configuration → Administrative Templates → Network → DNS Client
→ Turn off multicast name resolution = Enabled
```

```powershell
Get-ItemProperty HKLM:\Software\Policies\Microsoft\Windows NT\DNSClient
```

| Mechanism | Name shape | Typical environment |
|-----------|------------|---------------------|
| **DNS** | FQDN `host.example.com` | Global, server-based |
| **mDNS** | `host.local` | Apple/Linux LAN |
| **LLMNR** | `HOSTNAME` single label | Windows LAN fallback |

**Defense:** disable LLMNR/NetBIOS on servers that do not need it; require **SMB signing**, **LDAP signing**, **Kerberos** with SPN validation; segment sensitive VLANs; treat workstation subnets as hostile.

## Real-World Applications

Home/workgroup name resolution without a domain DNS; AD environments usually prefer proper DNS and turn LLMNR off.

**Example:** On a flat office VLAN, Responder answers LLMNR for a mistyped share name and captures NTLMv2 — later relayed if signing is off.

## Pros/Cons or Trade-offs

- **Pro:** Works without deploying a DNS server for simple LAN names.
- **Con:** No authentication of responders — spoofable by design on the link.
- **Con:** Attack surface often outweighs convenience on corporate networks.

## Comparison

- vs [[mDNS]]: mDNS uses `.local` and 224.0.0.251; LLMNR uses single-label names and 224.0.0.252, mainly Windows.
- vs [[DNS]]: DNS is server-based FQDNs with TTL/caching; LLMNR is multicast fallback.

## Mistakes to Avoid

- Leaving LLMNR enabled on domain-joined fleets without compensating controls.
- Assuming “private network profile” means trusted peers.
- Fixing only LLMNR while leaving NetBIOS name resolution equally spoofable.
