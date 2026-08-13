[[user management]] [[commands/visudo]] [[Authentication command]]

# fresh system sudo setup

> On a fresh Linux system, configure sudo so administrators can elevate safely — group membership, `visudo` edits, and optional passwordless rules for automation.

## Debian/Ubuntu default

Users in **`sudo`** group get full sudo (password prompt):

```bash
sudo usermod -aG sudo alice
id alice    # must re-login
```

## Edit sudoers safely

```bash
sudo visudo
# NEVER edit /etc/sudoers with plain vim without lock
```

Example — allow service restart only:

```
deploy ALL=(ALL) NOPASSWD: /bin/systemctl restart myapp.service
```

## Validate

```bash
sudo -l -U alice
sudo -k && sudo true    # test password path
```

## Hardening

- No `NOPASSWD: ALL` in production without break-glass policy.
- Use `/etc/sudoers.d/` drop-in files with mode `0440`.
- Log: `/var/log/auth.log` or `journalctl _COMM=sudo`.

## Related

[[user management]] · [[visudo]] · [[passwd]]

## Sources

- `man 5 sudoers`
- [sudo.ws documentation](https://www.sudo.ws/docs/)
