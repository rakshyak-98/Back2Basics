[[SSH]] [[Linux terminal]] [[terminal emulator]]

# PuTTY

> One-line: **Windows SSH/telnet client** — quick remote shell and tunnel setup when OpenSSH isn't available locally. Know its limits: key format, host keys, and saved-session security.

## Mental model

PuTTY is a **GUI terminal + connection manager** (not a shell). It implements SSH, telnet, serial, and raw TCP. Sessions store host, port, terminal type, and optionally credentials — treat saved sessions as secrets on shared PCs.

```
PuTTY.exe → TCP 22 → sshd → shell
Pageant → SSH key agent → PuTTY auth without passphrase each time
Plink → CLI equivalent for scripts/cron on Windows
```

| Component | Use |
|-----------|-----|
| PuTTY | Interactive SSH |
| PuTTYgen | Generate/convert keys (`.ppk` ↔ OpenSSH) |
| Pageant | Key agent |
| Plink | Non-interactive SSH (`plink user@host command`) |
| PSCP / PSFTP | File copy (legacy; prefer `scp`/`sftp` via OpenSSH on WSL) |

## Standard config / commands

**First-time connect:** verify host key fingerprint out-of-band (don't blindly "Accept"). Save session only after confirming fingerprint matches ops runbook.

**SSH key auth (production path):**

1. PuTTYgen → Generate → save private `.ppk` (password-protect).
2. Copy public key text → append to server `~/.ssh/authorized_keys`.
3. PuTTY → Connection → SSH → Auth → Credentials → Private key file.
4. Connection → Data → Auto-login username.
5. Save session.

**Convert `.ppk` to OpenSSH (WSL/Linux):**

```bash
puttygen key.ppk -O private-openssh -o id_ed25519
puttygen key.ppk -O public-openssh -o id_ed25519.pub
```

**Local port forward (reach DB behind bastion):**

- PuTTY → Connection → SSH → Tunnels → Source `15432`, Destination `db.internal:5432` → Local.
- Connect to bastion; `psql -h 127.0.0.1 -p 15432` on Windows.

**Plink one-liner:**

```cmd
plink -batch -i key.ppk user@host "systemctl is-active nginx"
```

`-batch` — fail instead of interactive host-key prompt (required for automation).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Server refused our key" | Server `sshd` logs; key in `authorized_keys` | Permissions 600 on key; correct user; `.ppk` linked in session |
| Host key changed warning | Compare new vs known good fingerprint | Possible MITM or rebuild — verify with ops before Accept |
| Garbled terminal | Window → Translation / UTF-8 | Set UTF-8; fix `LANG` on server |
| Disconnect idle | Connection → Seconds between keepalives | Set 30–60s keepalive; match `ClientAliveInterval` on server |
| Can't paste long command | PuTTY line limit | Use heredoc on server or Plink with script file |

## Gotchas

> [!WARNING]
> **Saved sessions with password** — PuTTY can store passwords in registry; avoid on shared machines. Prefer keys + Pageant.

> [!WARNING]
> **Default SSH protocol settings** — old PuTTY versions may negotiate weak ciphers. Update PuTTY; disable legacy if policy requires.

- **`.ppk` is PuTTY-specific** — Linux `ssh` needs OpenSSH format unless using `puttygen -O private-openssh`.
- **Copy/paste** — right-click paste (not Ctrl+V) in classic PuTTY window.
- **WSL vs PuTTY** — on Windows 10+, `ssh` in WSL is often simpler and matches Linux ops docs ([[SSH]]).

## When NOT to use

- **Production automation from Linux** — use OpenSSH `ssh`/`scp`, not Plink.
- **Modern crypto policy enforcement** — verify PuTTY version against org baseline; may need `ssh` from MS OpenSSH.
- **File sync at scale** — use [[rsync]], not PSCP loops.

## Related

[[SSH]] [[Linux terminal]] [[terminal emulator]] [[telnet]] [[nc]]
