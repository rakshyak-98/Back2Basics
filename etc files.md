
- Edit `/etc/ssh/sshd_config`. Disable root login and password authentication via SSH
```bash
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```