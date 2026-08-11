[[Protocol]] [[TCP]] [[TLS (Transport Layer Security)]] [[TFTP]] [[SCP (Secure Copy Protocol)]]

# ftp

> FTP (File Transfer Protocol) — control channel plus a second data connection; active (server dials you) vs passive (you dial the server).

---

## Mental model

**Say it in one breath:** FTP uses one TCP session for commands (usually :21) and another for the file bytes — that second connection is why NATs and firewalls hate FTP unless you pick the right mode.

```txt
Active (PORT):  Client:21ctrl ◄── data ── Server (server connects to client)
Passive (PASV): Client:21ctrl ── data ──► Server (client connects to server port)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Control vs data** | Commands on one socket; bytes on another | “FTP is two connections, not one.” |
| **Active** | Server connects back to client | “Breaks when the client is behind NAT.” |
| **Passive** | Client opens data to server | “Firewall-friendlier for clients.” |
| **FTPS** | FTP + TLS | “Encrypt control and data; still two channels.” |
| **Virtual user** | Login not in `/etc/passwd` | “Compromise stays inside FTP, not shell.” |

### vsftpd (common Linux server)

vsftpd (Very Secure FTP Daemon) is the usual Ubuntu default: chroot, TLS, PAM/virtual users.

---

## Standard config / commands

```bash
# Client — prefer passive
lftp -u user,pass -e 'set ftp:passive-mode true; ls; bye' ftp://ftp.example.com

# Explicit FTPS (STARTTLS on 21)
lftp -e 'set ftp:ssl-force true; set ssl:verify-certificate yes' ftps://ftp.example.com
```

```ini
# /etc/vsftpd.conf (sketch — production-safe defaults)
listen=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
pasv_min_port=40000
pasv_max_port=40100
pasv_address=203.0.113.10
rsa_cert_file=/etc/ssl/certs/ftp.pem
rsa_private_key_file=/etc/ssl/private/ftp.key
ssl_enable=YES
force_local_data_ssl=YES
force_local_logins_ssl=YES
```

| Knob | Why it matters |
|------|----------------|
| `pasv_min/max_port` + firewall | Passive needs a fixed high-port range open inbound |
| `pasv_address` | Behind NAT, advertise the public IP or PASV lies |
| Virtual users (PAM) | No system shell accounts for FTP-only people |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Login OK, LIST hangs | Active mode + client NAT | Force passive; open PASV port range |
| PASV connect fails | Firewall missing data ports | Allow `pasv_min_port`–`pasv_max_port` |
| Works internally, fails outside | Wrong `pasv_address` | Set public IP / correct LB mapping |
| TLS handshake fails | Cert / broken FTPS mode | Fix cert chain; explicit vs implicit (990) |
| 530 login incorrect | PAM / virtual user map | Check `/etc/passwd` vs virtual DB; logs |
| Writable chroot refused | vsftpd safety check | `allow_writeable_chroot` or non-writable root |

---

## Gotchas

> [!WARNING]
> **Cleartext FTP still ships passwords** — never use plain FTP on the internet; prefer FTPS or abandon for SFTP.

> [!WARNING]
> **SFTP is not FTPS** — SFTP is SSH file transfer; FTPS is FTP+TLS. Different ports, different daemons.

> [!WARNING]
> **ALG “FTP helpers” on firewalls** — conntrack helpers rewrite PORT/PASV; they break with TLS. Prefer explicit PASV ranges.

---

## When NOT to use

- **Any greenfield file drop** — use [[SCP (Secure Copy Protocol)]] / SFTP over [[SSH]], or HTTPS object storage.
- **Simple boot/firmware** on tiny devices — [[TFTP]] (with network isolation).
- **Browser uploads** — HTTP multipart; users do not have FTP clients.

---

## Related

[[TFTP]] [[SCP (Secure Copy Protocol)]] [[SSH]] [[TLS (Transport Layer Security)]] [[SMTP]] [[WebDAV]] [[NAT (Network Address Translation)]]
