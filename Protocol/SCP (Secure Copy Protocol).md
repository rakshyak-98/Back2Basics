[[ssh/ssh allow local system with key]] [[SSH authentication]] [[ssh agent]] [[ftp]] [[TLS (Transport Layer Security)]] [[Linux/CLI]]

# SCP (Secure Copy Protocol)

> SCP copies files over SSH using the same authentication and encryption as an interactive shell — prefer `sftp` or `rsync` for new automation, but SCP remains common for one-off secure copies.

```txt
        SCP (Secure Copy P ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check that SCP is SSH (not a separate daemon), host-key verifica…

## Sources
- [OpenSSH scp man page](https://man.openbsd.org/scp) — deep-dive
- [RFC 4251 — SSH Protocol Architecture](https://datatracker.ietf.org/doc/html/rfc4251) — overview
- [OpenSSH release notes](https://www.openssh.com/releasenotes.html) — overview

## Key Concepts
- **Runs over SSH:** default port 22 — same keys, agent, and ProxyJump as shell access.
- **Legacy remote `scp`:** classic mode invokes remote `scp`
- **Auth:** [[SSH authentication]] via keys ([[ssh agent]]) or passwords (disable passwor…

## Technical Details
```bash
# Local → remote
scp ./build.tar.gz user@host:/var/tmp/

# Remote → local
scp user@host:/var/log/syslog ./

# Recursive directory
scp -r ./dist/ user@host:/var/www/

# Through bastion
scp -o ProxyJump=bastion.example.com file user@internal:/tmp/

scp -i ~/.ssh/deploy_key artifact.zip deploy@prod:/releases/
```

| Tool | Strength |
|------|----------|
| **SCP** | Simple one-shot copy |
| **SFTP** | Interactive, resume, remote listing |
| **rsync** | Delta sync, `--delete`, bandwidth limits |
| **[[ftp]]** | Cleartext — avoid |

## Mistakes to Avoid
- **Mistake:** Quoting mistakes that expand globs locally instead of remotely
- **Mistake:** Ignoring trailing-slash meaning on directories
- **Mistake:** Using SCP for repeated full-tree syncs instead of rsync
- **Mistake:** Disabling host-key checks “to make CI pass.”

## Pros/Cons or Trade-offs
- **Pro:** Zero extra infrastructure if SSH already works.
- **Con:** Large trees without `rsync` re-copy everything on retry.
- **Con:** Globbing and trailing-slash semantics surprise operators.

## Comparison
- vs SFTP: better for interactive listing/resume; OpenSSH recommends it for new scripts.
- vs `rsync -e ssh`: delta sync and `--delete` for mirrors.
- vs [[ftp]]: SCP is encrypted; FTP is cleartext unless FTPS.


### Use cases
- Shipping a build artifact to a bastion-reachable host, pulling a log for inci…

- **Example:** `scp -o ProxyJump=bastion.example.com artifact.tgz deploy@intern…
