[[TCP]] · [[TLS (Transport Layer Security)]] · [[HTTP module]] · [[SCP (Secure Copy Protocol)]] · [[TFTP]]

# ftp

> FTP transfers files over TCP with separate control (21) and data channels — NAT and firewall traversal make passive mode and SFTP/HTTPS replacements preferable on modern networks.

---

## Modes

| Mode | Control | Data | Firewall note |
|------|---------|------|---------------|
| **Active** | Client:ephemeral → Server:21 | Server:20 → Client:ephemeral | Client must accept inbound — rarely works |
| **Passive (PASV)** | Client → Server:21 | Client → Server:high port | Server advertises IP/port in PASV response |

[RFC 959](https://datatracker.ietf.org/doc/html/rfc959) defines classic FTP; extensions add TLS ([RFC 4217](https://datatracker.ietf.org/doc/html/rfc4217) FTPS).

## Session sketch

```
Client → Server:21  (control)
USER anonymous
PASS guest@
PASV
227 Entering Passive Mode (203,0,113,10,195,50)
Client → Server:50000  (data connection for LIST/RETR/STOR)
```

## Security

| Protocol | Encryption |
|----------|------------|
| **FTP** | Cleartext credentials and data |
| **FTPS** | FTP + TLS (explicit or implicit) |
| **SFTP** | SSH subsystem — not FTP; see [[SCP (Secure Copy Protocol)]] |
| **HTTPS** | Object storage APIs replace many file-drop use cases |

Never expose anonymous FTP with write access to sensitive networks.

## CLI

```bash
ftp ftp.example.com
lftp ftp.example.com    # scripting friendly
curl -u user:pass ftp://ftp.example.com/file.txt -O
```

## When still used

- Legacy mainframe/batch partners
- Anonymous software mirrors (declining)
- Embedded devices with tiny stacks

Prefer **SFTP**, **S3**, or **rsync over SSH** for new designs.

## Recall

- Why does passive mode work better through client-side NAT?
- How is SFTP different from FTPS?

## Sources

- [RFC 959 — FTP](https://datatracker.ietf.org/doc/html/rfc959)
- [RFC 4217 — FTP over TLS](https://datatracker.ietf.org/doc/html/rfc4217)
