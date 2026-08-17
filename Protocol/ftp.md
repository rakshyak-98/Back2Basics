[[TCP]] [[TLS (Transport Layer Security)]] [[HTTP module]] [[SCP (Secure Copy Protocol)]] [[TFTP]]

# ftp

> FTP transfers files over TCP with separate control (21) and data channels — NAT and firewalls make passive mode common, and SFTP/HTTPS replace FTP for most new designs.

```txt
        ftp ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers test active versus passive mode, FTPS versus SFTP (not the same)…

## Sources
- [RFC 959 — FTP](https://datatracker.ietf.org/doc/html/rfc959) — deep-dive
- [RFC 4217 — Securing FTP with TLS](https://datatracker.ietf.org/doc/html/rfc4217) — overview

## Key Concepts
- **Two channels:** control on 21; data on a second connection (active or passive).
- **Active vs passive:** active needs inbound to the client; passive has the client dial a high server…
- **FTPS ≠ SFTP:** FTPS is FTP+TLS

## Technical Details
| Mode | Control | Data | Firewall note |
|------|---------|------|---------------|
| **Active** | Client:ephemeral → Server:21 | Server:20 → Client:ephemeral | Client must accept inbound — rarely works |
| **Passive (PASV)** | Client → Server:21 | Client → Server:high port | Server advertises IP/port in PASV response |

```
Client → Server:21  (control)
USER anonymous
PASS guest@
PASV
227 Entering Passive Mode (203,0,113,10,195,50)
Client → Server:50000  (data connection for LIST/RETR/STOR)
```

| Protocol | Encryption |
|----------|------------|
| **FTP** | Cleartext credentials and data |
| **FTPS** | FTP + TLS (explicit or implicit) |
| **SFTP** | SSH subsystem — not FTP |
| **HTTPS** | Object storage APIs replace many file-drop use cases |

```bash
ftp ftp.example.com
lftp ftp.example.com    # scripting friendly
curl -u user:pass ftp://ftp.example.com/file.txt -O
```

## Mistakes to Avoid
- **Mistake:** Exposing anonymous write FTP on sensitive networks
- **Mistake:** Confusing SFTP with FTPS in security reviews
- **Mistake:** Using active mode through client-side NAT without understanding …
- **Mistake:** Advertising a private IP in PASV responses behind NAT

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous legacy support and simple anonymous read mirrors.
- **Con:** Cleartext by default; firewall/NAT complexity.
- **Con:** Prefer SFTP, S3, or rsync-over-SSH for new designs.

## Comparison
- vs [[SCP (Secure Copy Protocol)]] / SFTP: encrypted, single-channel over SSH — usually better.
- vs [[TFTP]]: TFTP is UDP/no-auth for PXE; FTP is TCP with optional auth.
- vs HTTPS object storage: better for scale and CDN.


### Use cases
- Legacy mainframe/batch partner drops, declining anonymous mirrors, and embedd…

- **Example:** A partner still requires FTP
