[[UDP]] · [[dnsmasq]] · [[ftp]] · [[SCP (Secure Copy Protocol)]]

# TFTP

> Trivial File Transfer Protocol moves small files over UDP without authentication — common for PXE boot loaders and embedded firmware because the implementation fits in kilobytes of code.

---

## Characteristics

[RFC 1350](https://datatracker.ietf.org/doc/html/rfc1350) defines TFTP:

- **UDP port 69** (server); transfers use ephemeral ports
- **No login** — file ACLs are OS-level on server directory
- **Stop-and-wait** — one block per round trip (slow on high latency)
- **Block size** 512 bytes default; **OACK** negotiates larger blocks ([RFC 2347](https://datatracker.ietf.org/doc/html/rfc2347))

## Opcodes

| Opcode | Meaning |
|--------|---------|
| 1 | RRQ (read request) |
| 2 | WRQ (write request) |
| 3 | DATA |
| 4 | ACK |
| 5 | ERROR |

## PXE boot chain

```
DHCP option 66/67 or UEFI HTTP boot
        │
        ▼
TFTP fetch pxelinux.0 / grub / iPXE
        │
        ▼
Kernel + initrd → full OS install
```

Often paired with [[dnsmasq]] DHCP on lab networks.

## Server setup (example)

```bash
# /etc/default/tftpd-hpa
TFTP_DIRECTORY="/var/lib/tftpboot"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure"
```

`--secure` restricts paths to `TFTP_DIRECTORY`.

## Client

```bash
tftp 192.168.1.1 -c get firmware.bin
```

## Security

Assume **anyone on the L2 network can read/write** unless isolated VLAN. Never expose TFTP to the public Internet. For authenticated transfers use [[SCP (Secure Copy Protocol)]] or HTTPS.

## Recall

- Why is TFTP used instead of [[ftp]] for PXE?
- What stops a TFTP client from reading arbitrary server paths when `--secure` is set?

## Sources

- [RFC 1350 — TFTP](https://datatracker.ietf.org/doc/html/rfc1350)
- [RFC 2347 — TFTP Option Extension](https://datatracker.ietf.org/doc/html/rfc2347)
