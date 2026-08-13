[[useradd]] [[usermod]] [[userdel]] [[passwd]] [[Authentication command]] [[fresh system sudo setup]]

# user management

> User management covers accounts, groups, passwords, and sudo policy — the identity layer every multi-user Linux host depends on.

Linux stores account metadata in `/etc/passwd`, password hashes in `/etc/shadow` (root-readable), and group membership in `/etc/group`. **PAM** handles authentication for login, `su`, and `sudo`. **NSS** (`getent`) merges local files with LDAP/SSSD when configured.

## Common operations

```bash
# Create user with home directory
sudo useradd -m -s /bin/bash alice
sudo passwd alice

# Add to supplementary groups
sudo usermod -aG docker,sudo alice

# Verify
id alice
getent passwd alice
groups alice

# Remove (keep home: omit -r)
sudo userdel -r bob
```

## Lock / unlock without deleting

```bash
sudo passwd -l alice      # lock password
sudo usermod -L alice       # lock account (shadow !)
sudo passwd -u alice        # unlock
```

## sudo policy

Edit with `visudo` — never raw `vi /etc/sudoers`.

```
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

See [[fresh system sudo setup]].

## Debugging login failures

| Symptom | Check |
|---------|-------|
| Permission denied (publickey) | `~/.ssh/authorized_keys` perms (700 `~/.ssh`, 600 file) |
| Account locked | `passwd -S user`; `/etc/shadow` `!` prefix |
| Group not applied | User must re-login after `usermod -aG` |
| LDAP user missing | `getent passwd user`; SSSD logs |

## Related

[[useradd]] · [[usermod]] · [[linux groups]] · [[login shell]] · [[management/keyrings]]

## Sources

- `man 5 passwd`, `man 5 shadow`, `man 8 useradd`
- [Red Hat — Managing users](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/)
