[[ssh/ssh allow local system with key]] [[Security/TLS (Transport Layer Security)]] [[ftp]]

# SCP (Secure Copy Protocol)

> One-line: file copy over SSH — reuses sshd auth and encryption; prefer `rsync -e ssh` or SFTP for large/recursive transfers with resume.

## Mental model

SCP wraps **SSH** transport: authenticate like `ssh`, then copy files over encrypted channel. Syntax mirrors `cp` with remote `user@host:path`. Not a separate daemon — **sshd** on port 22 (or custom).

```
local scp ──SSH session──► sshd ──► read/write remote files
```

Legacy SCP protocol is old; OpenSSH uses SFTP subsystem for transfers internally in modern versions. Still ubiquitous for one-off copies in runbooks.

## Standard config / commands

### Copy to remote

```bash
scp file.txt user@remote_host:/path/to/destination/
scp -r ./local_dir user@remote_host:/remote/path/
```

### Copy from remote

```bash
scp user@remote_host:/path/to/file.txt ./local/
scp -r user@remote_host:/remote/dir ./local/
```

### Remote to remote (through your machine)

```bash
scp -3 user1@host1:/file user2@host2:/path
```

### Options (production)

```bash
scp -i ~/.ssh/deploy_key -P 2222 file.txt user@host:/app/
scp -o StrictHostKeyChecking=accept-new file.txt user@host:/app/  # first connect automation
scp -C file.txt user@host:/app/   # compression on slow links
```

### rsync over SSH (preferred for dirs)

```bash
rsync -avz -e "ssh -i key.pem" ./dist/ user@host:/var/www/app/
# resume partial, delta transfer
```

### SFTP interactive

```bash
sftp user@host
sftp> put local.txt /remote/path/
sftp> get /remote/log.txt .
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied (publickey) | SSH key agent | `ssh-add -l`; correct `-i` key; `authorized_keys` |
| Host key verification failed | Known_hosts mismatch | Verify fingerprint; update known_hosts carefully |
| Stalled mid-transfer | Network drop | Use rsync; `ServerAliveInterval` in ssh config |
| `scp: not found` | Remote no scp binary | Use sftp/rsync; install openssh-clients on remote |
| Wrong owner on remote | Remote umask | `scp` preserves modes; fix with ssh `chmod` after |
| Slow many small files | Per-file overhead | tar+scp one archive, or rsync |

## Gotchas

> [!WARNING]
> **Glob expansion is local** — `scp *.log host:` expands on local shell; quote remote globs: `host:'/logs/*.log'`.

> [!WARNING]
> **Trailing slash semantics** — `dir/` vs `dir` affects whether contents or directory itself copied (rsync clearer).

> [!WARNING]
> **Root login disabled** — copy to user home then sudo move.

## When NOT to use

- **Large dataset sync with resume** — `rsync` over SSH.
- **Public anonymous download** — HTTPS/S3, not SCP.
- **Windows ↔ Linux path quirks** — verify OpenSSH build; consider SFTP GUI clients.

## Related

[[ssh/ssh allow local system with key]] [[ftp]] [[Security/TLS (Transport Layer Security)]] [[Linux/CLI]]
