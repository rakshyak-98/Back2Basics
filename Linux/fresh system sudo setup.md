[[user management]] [[commands/visudo]] [[Authentication command]] [[visudo]] [[passwd]]

# fresh system sudo setup

> On a fresh Linux system, configure sudo so administrators can elevate safely — group membership, `visudo` edits, and optional narrow passwordless rules for automation.

## Interview Relevance
Security/ops hybrid: grant least privilege, use `visudo`, prefer `sudoers.d` drop-ins, and reject blanket `NOPASSWD: ALL` without a break-glass story.

## Sources
- `man 5 sudoers` — deep-dive
- [sudo.ws documentation](https://www.sudo.ws/docs/) — overview

## Core Definition
sudo lets permitted users run commands as another user (usually root) after policy checks. On Debian/Ubuntu, membership in the **`sudo`** group typically grants full sudo with a password prompt.

## Key Concepts
- **Group grant:** `usermod -aG sudo` then re-login for group membership.
- **visudo:** Locked, syntax-checked edits of sudoers policy.
- **drop-ins:** `/etc/sudoers.d/` fragments with mode `0440`.
- **Command restriction:** Prefer explicit binaries/args over `ALL`.
- **NOPASSWD:** Convenience for automation; high risk if scoped too wide.

## Technical Details

```bash
sudo usermod -aG sudo alice
id alice    # must re-login
```

```bash
sudo visudo
# NEVER edit /etc/sudoers with plain vim without lock
```

```
deploy ALL=(ALL) NOPASSWD: /bin/systemctl restart myapp.service
```

```bash
sudo -l -U alice
sudo -k && sudo true
```

Hardening: avoid `NOPASSWD: ALL` in production without break-glass policy; log via `/var/log/auth.log` or `journalctl _COMM=sudo`.

## Real-World Applications
Bootstrap a cloud image: add the admin user to `sudo`, drop a `sudoers.d/deploy` file allowing only specific `systemctl` unit restarts for the deploy role.

## Pros/Cons or Trade-offs
- **Pro:** Auditable elevation with fine-grained commands beats sharing the root password.
- **Con:** Over-broad NOPASSWD or group grants become a lateral-movement gift.

## Comparison
vs root SSH login: sudo keeps shared accounts out and logs who elevated. vs Polkit: polkit governs desktop/session privileged actions; sudo is the classic CLI elevation path. vs [[user management]]: creating users/groups vs authorizing elevation.

## Mistakes to Avoid
- Editing `/etc/sudoers` without `visudo` and locking yourself out with a syntax error.
- Granting `NOPASSWD: ALL` “just for CI” on bastion hosts.
- Forgetting that group changes need a new login session before `id` shows `sudo`.
