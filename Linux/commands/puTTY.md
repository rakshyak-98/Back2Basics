[[SSH]] [[Linux terminal]] [[terminal emulator]] [[telnet]] [[nc]] [[rsync]]

# PuTTY

> Windows GUI SSH (and serial/telnet) client with saved sessions — not a shell; keys use `.ppk`, not OpenSSH by default.

## Interview Relevance

Checks Windows remote-access literacy: host-key verification, Pageant, `.ppk` vs OpenSSH, and when to prefer WSL/`ssh` instead.

## Sources

- [PuTTY documentation](https://www.chiark.greenend.org.uk/~sgtatham/putty/docs.html) — deep-dive
- [Wikipedia — PuTTY](https://en.wikipedia.org/wiki/PuTTY) — overview

## Core Definition

PuTTY is a GUI terminal and connection manager. It speaks SSH, telnet, serial, and raw TCP. Sessions store host, port, terminal type, and optionally credentials — treat saved sessions as secrets on shared PCs.

## Key Concepts

- **Not a shell:** it opens a terminal to a remote shell or serial device.
- **`.ppk` keys:** PuTTY-specific; convert with PuTTYgen for OpenSSH/WSL.
- **Pageant:** agent so you unlock the key once per session.
- **Plink / PSCP:** CLI cousins for scripts; prefer OpenSSH on modern Windows/WSL when possible.
- **Host key (TOFU):** verify fingerprint out-of-band before Accept.

## Technical Details

```
PuTTY.exe → TCP 22 → sshd → shell
Pageant → SSH key agent → PuTTY auth without passphrase each time
Plink → CLI equivalent for scripts on Windows
```

| Component | Use |
|-----------|-----|
| PuTTY | Interactive SSH |
| PuTTYgen | Generate/convert keys (`.ppk` ↔ OpenSSH) |
| Pageant | Key agent |
| Plink | Non-interactive SSH |
| PSCP / PSFTP | File copy (legacy; prefer `scp`/`sftp` via OpenSSH) |

Key setup: PuTTYgen → Generate → save private `.ppk` → append public key to `~/.ssh/authorized_keys` → point session at the private key → set auto-login username → Save session.

```bash
puttygen key.ppk -O private-openssh -o id_ed25519
puttygen key.ppk -O public-openssh -o id_ed25519.pub
```

Local forward: Connection → SSH → Tunnels → Source `15432`, Destination `db.internal:5432` → Local.

```cmd
plink -batch -i key.ppk user@host "systemctl is-active nginx"
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Server refused our key | `sshd` logs; `authorized_keys` | Permissions; correct user; `.ppk` linked |
| Host key changed | Fingerprint vs known good | Verify with ops before Accept |
| Garbled terminal | Translation / UTF-8 | Set UTF-8; fix `LANG` on server |
| Idle disconnect | Keepalives | 30–60s; match `ClientAliveInterval` |

## Real-World Applications

Bastion access from locked-down Windows desktops, serial console to appliances, and local port forwards to internal databases.

**Example:** Convert `.ppk` once, then use the same key from WSL OpenSSH so runbooks stay Linux-shaped ([[SSH]]).

## Pros/Cons or Trade-offs

- **Pro:** Familiar GUI session store for Windows fleets without WSL.
- **Con:** Format/crypto drift vs OpenSSH; saved passwords in registry are a shared-PC risk.

## Comparison

- vs OpenSSH `ssh`: same protocol; OpenSSH matches Linux operations docs and automation.
- vs [[rsync]]/PSCP: use rsync for real sync; PSCP is one-off copy.

## Mistakes to Avoid

- Blindly accepting changed host keys.
- Storing passwords in saved sessions on shared machines — prefer keys + Pageant.
- Assuming `.ppk` works with Linux `ssh` without conversion.
- Using ancient PuTTY builds that still negotiate weak ciphers.
