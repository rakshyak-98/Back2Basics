[[UDP]] [[dnsmasq]] [[ftp]] [[SCP (Secure Copy Protocol)]]

# TFTP

> Trivial File Transfer Protocol moves small files over UDP without authentication — common for PXE boot loaders and embedded firmware because the stack fits in kilobytes of code.

## Interview Relevance

Interviewers ask why PXE uses TFTP, how stop-and-wait limits throughput, and why TFTP must never face the public Internet.

## Sources

- [RFC 1350 — TFTP](https://datatracker.ietf.org/doc/html/rfc1350) — deep-dive
- [RFC 2347 — TFTP Option Extension](https://datatracker.ietf.org/doc/html/rfc2347) — overview

## Key Concepts

- **UDP port 69:** server listens; transfers move to ephemeral ports.
- **No login:** file ACLs are OS-level on the server directory.
- **Stop-and-wait:** one block per round trip — slow on high latency.
- **OACK:** negotiates larger blocks than the 512-byte default.

## Technical Details

| Opcode | Meaning |
|--------|---------|
| 1 | RRQ (read request) |
| 2 | WRQ (write request) |
| 3 | DATA |
| 4 | ACK |
| 5 | ERROR |

PXE boot chain:

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

```bash
# /etc/default/tftpd-hpa
TFTP_DIRECTORY="/var/lib/tftpboot"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure"
```

`--secure` restricts paths to `TFTP_DIRECTORY`.

```bash
tftp 192.168.1.1 -c get firmware.bin
```

## Real-World Applications

PXE network boot, router/firmware updates on isolated management networks, and lab appliance imaging.

**Example:** DHCP hands out next-server and boot filename; the NIC’s PXE ROM pulls `pxelinux.0` via TFTP before the kernel loads.

## Pros/Cons or Trade-offs

- **Pro:** Tiny client implementation — works in ROM and constrained devices.
- **Con:** No authentication; anyone on the L2 segment can often read/write unless isolated.
- **Con:** Stop-and-wait throughput is poor versus [[ftp]]/HTTP/SCP on WAN links.

## Comparison

- vs [[ftp]]: FTP is TCP with auth options; TFTP wins for PXE ROM size.
- vs [[SCP (Secure Copy Protocol)]] / HTTPS: prefer those for authenticated transfers outside isolated VLANs.

## Mistakes to Avoid

- Exposing TFTP to the public Internet.
- Omitting `--secure` / chroot so clients can read arbitrary server paths.
- Using TFTP for large authenticated file distribution — wrong tool.
