[[ssh/ssh allow local system with key]] · [[ftp]] · [[TLS (Transport Layer Security)]] · [[Linux/CLI]]

# SCP (Secure Copy Protocol)

> SCP copies files over SSH using the same authentication and encryption as interactive shell sessions — prefer `sftp` or `rsync` for new automation, but SCP remains ubiquitous for one-off secure copies.

---

## Usage

Runs over **SSH** (default port 22), not a separate protocol server.

```bash
# Local → remote
scp ./build.tar.gz user@host:/var/tmp/

# Remote → local
scp user@host:/var/log/syslog ./

# Recursive directory
scp -r ./dist/ user@host:/var/www/

# Through bastion
scp -o ProxyJump=bastion.example.com file user@internal:/tmp/
```

## How it works

Legacy `scp` invokes `scp` binary on remote side over SSH channel; data stream is encrypted like any SSH session. OpenSSH 9+ recommends **`sftp`** for new scripts ([OpenSSH release notes](https://www.openssh.com/releasenotes.html)).

## vs alternatives

| Tool | Strength |
|------|----------|
| **SCP** | Simple one-shot copy |
| **SFTP** | Interactive, resume, remote listing |
| **rsync** | Delta sync, `--delete`, bandwidth limits |
| **[[ftp]]** | Cleartext — avoid |

## Authentication

Uses [[SSH authentication]] — keys via [[ssh agent]] or passwords (disable password auth in production).

```bash
scp -i ~/.ssh/deploy_key artifact.zip deploy@prod:/releases/
```

## Pitfalls

- **Globbing** happens locally vs remotely depending on quoting
- **Trailing slash** on directory paths changes meaning
- Large trees without `rsync` re-copy everything on retry

## Recall

- Why does SCP inherit SSH host key verification?
- When is `rsync -e ssh` preferable to SCP?

## Sources

- [OpenSSH scp man page](https://man.openbsd.org/scp)
- [RFC 4251 — SSH Protocol Architecture](https://datatracker.ietf.org/doc/html/rfc4251)
