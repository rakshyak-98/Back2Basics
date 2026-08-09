[[Protocol]] [[UDP]] [[ftp]] [[dnsmasq]]

# TFTP

> TFTP (Trivial File Transfer Protocol) — tiny UDP file transfer with block ACKs for boot images and appliance configs.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Client asks for a file (RRQ) or to write one (WRQ) on UDP/69; server switches to a new port and sends fixed-size blocks that the client ACKs — no login, no encryption, almost no code.

```txt
Client                    TFTP server
  │  RRQ/WRQ (UDP :69)         │
  │───────────────────────────►│
  │  DATA/ACK on ephemeral     │
  │◄──────────────────────────►│
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **RRQ / WRQ** | Read / write request | “PXE does RRQ for the boot file.” |
| **Block + ACK** | Stop-and-wait reliability | “Each block waits for ACK — simple, slow.” |
| **Port 69** | Well-known listen port | “Only the first packet hits 69; transfer moves.” |
| **octet mode** | Binary transfer | “Use octet for images; netascii mangles binaries.” |
| **blksize** | Option for larger blocks | “Default 512 B is painful on modern links.” |

### Why it exists

Routers, phones, PXE clients: little RAM, no full [[ftp]]/TLS stack — they only need “give me `boot.img`.”

### How the story goes

1. Client sends RRQ/WRQ to `:69`.
2. Server answers from a new UDP port (firewall must allow that return path).
3. DATA blocks numbered; client ACKs; last short block ends transfer.
4. Timeout → retransmit the last block.

---

## Standard config / commands

```bash
# Client
tftp 192.0.2.10
> mode binary
> get boot.img
> quit

# Or one-shot
curl tftp://192.0.2.10/boot.img -o boot.img

# Server examples: tftpd-hpa, atftpd, or [[dnsmasq]] enable-tftp
# /etc/default/tftpd-hpa
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure"
```

| Knob | Why it matters |
|------|----------------|
| `--secure` / chroot dir | Stops path traversal outside the TFTP root |
| firewall UDP 69 + ephemeral | Stateful firewalls need RELATED or wide UDP allow |
| blksize option | Speeds transfers; both ends must support |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| RRQ timeout | UDP/69 blocked; wrong server IP | Open 69/udp; verify listen with `ss -ulnp \| grep 69` |
| Starts then stalls | Ephemeral port blocked mid-transfer | Allow return UDP from server; fix conntrack |
| “Access violation” | Path outside root / perms | Put file in TFTP dir; fix ownership |
| Corrupt image | netascii mode | Force binary/octet |
| PXE gets wrong file | DHCP option 66/67 mismatch | Align next-server and boot filename with TFTP tree |
| Slow on LAN | 512-byte blocks | Enable blksize (e.g. 1428) if client supports |

---

## Gotchas

> [!WARNING]
> **No auth, no TLS** — anyone who can reach UDP/69 can often read your boot/config tree. Bind to management VLAN only.

> [!WARNING]
> **Firewall “port 69 only” is wrong** — transfer uses a *different* server port after the first packet.

> [!WARNING]
> **Writable TFTP is a malware drop box** — disable WRQ unless you truly need device uploads.

---

## When NOT to use

- **User file sharing or secrets** — use [[SCP (Secure Copy Protocol)]], [[SSH]], or HTTPS.
- **WAN / untrusted networks** — encryption and auth are mandatory elsewhere.
- **Large modern payloads when you control the client** — HTTP(S) or full [[ftp]]/SFTP is faster and safer.

---

## Related

[[ftp]] [[UDP]] [[dnsmasq]] [[SCP (Secure Copy Protocol)]] [[SSH]] [[Protocol]]
