[[useradd]] [[usermod]] [[userdel]] [[passwd]] [[Authentication command]] [[fresh system sudo setup]] [[linux groups]] [[login shell]] [[management/keyrings]] [[visudo]]

# user management

> Accounts, groups, passwords, and sudo policy — the identity layer every multi-user Linux host depends on.

## Interview Relevance

Expect passwd vs shadow, `-aG` append, lock vs delete, PAM/NSS/`getent`, and visudo for sudo policy.

## Sources

- `man 5 passwd`, `man 5 shadow`, `man 8 useradd` — deep-dive
- [Red Hat — Managing user accounts](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-user-accounts_configuring-basic-system-settings) — overview

## Core Definition

Linux stores account metadata in `/etc/passwd`, password hashes in `/etc/shadow` (root-readable), and groups in `/etc/group`. PAM handles authentication for login, `su`, and `sudo`. NSS (`getent`) merges local files with LDAP/SSSD when configured.

## Key Concepts

- **passwd / shadow / group:** identity, secrets, membership.
- **PAM vs NSS:** how auth happens vs where names resolve.
- **Lock vs delete:** temporary disable without removing home/UID.
- **sudo policy:** least privilege via [[visudo]] / `sudoers.d`.

## Technical Details

```bash
sudo useradd -m -s /bin/bash alice
sudo passwd alice
sudo usermod -aG docker,sudo alice
id alice
getent passwd alice
groups alice
sudo userdel -r bob
sudo passwd -l alice
sudo usermod -L alice
sudo passwd -u alice
```

```
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

| Symptom | Check |
|---------|-------|
| Permission denied (publickey) | `~/.ssh` 700, `authorized_keys` 600 |
| Account locked | `passwd -S`; shadow `!` prefix |
| Group not applied | Re-login after `usermod -aG` |
| LDAP user missing | `getent passwd`; SSSD logs |

## Real-World Applications

Onboard an engineer: create home, set shell, append sudo/docker groups, verify with `id` after re-login, grant a narrow sudoers drop-in.

## Pros/Cons or Trade-offs

- **Pro:** Simple local model for bastions and appliances.
- **Con:** Does not scale alone — directory/IdP needed for fleets.

## Comparison

- vs leaf tools ([[useradd]], [[passwd]]): this note is the workflow hub.
- vs cloud IAM: host accounts are still needed for SSH break-glass even when SSO exists.

## Mistakes to Avoid

- `usermod -G` without `-a` wiping supplementary groups.
- Editing `/etc/sudoers` without visudo.
- Deleting accounts without handling UID reuse / orphaned files.
