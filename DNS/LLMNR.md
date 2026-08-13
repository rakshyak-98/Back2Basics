<!-- note-strategy: operational -->
[[DNS]] [[mDNS]] [[DNS server]]

# LLMNR

> LLMNR (Link-Local Multicast Name Resolution) — Windows-style LAN name lookup over multicast when unicast DNS fails — spoofable; usually turn it off.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** If DNS can’t answer a short hostname, a Windows host may multicast an LLMNR query on the LAN; whoever answers wins — including an attacker.

```txt
Host A: "where's FILESERVER?"
   │  LLMNR multicast (UDP 5355)
   ▼
Any LAN host can reply with an IP  ← trust boundary problem
```

Sibling of [[mDNS]] (`.local` / Bonjour). LLMNR is the Microsoft-oriented path; both are link-local and unauthenticated.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Link-local** | Same L2 segment only | “Doesn’t cross routers without helpers.” |
| **Fallback** | Used after DNS miss | “Typos and missing suffixes trigger it.” |
| **Spoofing / Responder** | Fake answers steal hashes | “LLMNR/NBT-NS poisoning is a classic AD attack.” |
| **Disable** | Prefer real DNS | “Hardening guide: turn LLMNR off.” |
| **vs mDNS** | Different stacks, same class of risk | “Mac/Linux lean mDNS; Windows lean LLMNR.” |

### Docker / DNS aside

Containers inherit `/etc/resolv.conf` unless you set daemon or network DNS. LLMNR on the host does **not** fix container resolution — fix [[DNS server]] / Docker DNS configuration instead.

---

## Standard config / commands

```powershell
# Windows: disable via policy / registry (sketch)
# HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient
# EnableMulticast = 0
```

```bash
# Linux: systemd-resolved — LLMNR mode
resolvectl status | grep -i llmnr
# /etc/systemd/resolved.conf
# LLMNR=no
sudo systemctl restart systemd-resolved
```

```bash
# Confirm unicast DNS works so you don't need fallbacks
dig +short myserver.example.com
getent hosts myserver
```

| Knob | Why it matters |
|------|----------------|
| `LLMNR=no` | Removes multicast fallback attack surface |
| Search domains in resolv.conf | Stops short-name DNS misses that trigger LLMNR |
| Firewall UDP/5355 | Block cross-VLAN if you can’t disable endpoints |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Random hosts resolve on LAN only | LLMNR/mDNS answering | Publish real DNS A/AAAA; disable LLMNR |
| Auth prompts / weird SMB targets | Responder-style spoof | Disable LLMNR/NBT-NS; network detection |
| Docker can’t resolve public names | Container DNS, not LLMNR | Fix Docker `dns` / host `resolv.conf` |
| Short name works on Win, not Linux | LLMNR vs search domain | Add DNS search suffix / FQDN records |
| After disable, names break | Relied on multicast | Create proper [[DNS zone]] records |

---

## Gotchas

> [!WARNING]
> **Unauthenticated answers** — any local device can claim `payroll`. Never treat LLMNR as identity.

> [!WARNING]
> **Disabling without DNS** — users will say “network is broken”; ship internal zone records first.

> [!WARNING]
> **NBT-NS often sits beside LLMNR** — harden both on Windows fleets.

---

## When NOT to use

- **Any managed network with a real [[DNS server]]** — disable LLMNR.
- **Cross-subnet service discovery** — use DNS-SD via unicast DNS or a service registry.
- **Security-sensitive name → IP binding** — DNSSEC/internal CA + unicast DNS only.

---

## Related

[[mDNS]] [[DNS]] [[DNS server]] [[DNS zone]] [[name server]] [[DNS rebinding]]
