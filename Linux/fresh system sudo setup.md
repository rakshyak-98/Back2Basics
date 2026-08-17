[[user management]] [[commands/visudo]] [[Authentication command]] [[visudo]] [[passwd]]

# fresh system sudo setup

> On a fresh Linux system, configure sudo so administrators can elevate safely — group membership, `visudo` edits, and optional narrow passwordless rules for automation.

```txt
        fresh system sudo  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Security/ops hybrid: grant least privilege, use `visudo`, prefer `sudoers.d` …

## Sources
- `man 5 sudoers` — deep-dive
- [sudo.ws documentation](https://www.sudo.ws/docs/) — overview

## Key Concepts
- **Core:** sudo lets permitted users run commands as another user (usually root) after p…

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

- Hardening: avoid `NOPASSWD: ALL` in production without break-glass policy

## Mistakes to Avoid
- **Mistake:** Editing `/etc/sudoers` without `visudo` and locking yourself out…
- **Mistake:** Granting `NOPASSWD: ALL` “just for CI” on bastion hosts
- **Mistake:** Forgetting that group changes need a new login session before `i…

## Pros/Cons or Trade-offs
- **Pro:** Auditable elevation with fine-grained commands beats sharing the root password.
- **Con:** Over-broad NOPASSWD or group grants become a lateral-movement gift.

## Comparison
- vs root SSH login: sudo keeps shared accounts out and logs who elevated. vs P…


### Use cases
- Bootstrap a cloud image: add the admin user to `sudo`, drop a `sudoers.d/depl…
