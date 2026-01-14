> [!NOTE] 
> - Need root or sudo access to perform these steps.

**Create new user (with Login Disable)**
- system-like user (e.g, named `nodeuser`) -> prevents SSH/shell access while still allowing the user to run processes.
- Create user **without home directory**
- Set the shell to `/usr/sbin/nologin` or `/bin/false`

```bash
sudo useradd -r -s /usr/sbin/login nodeuser;
```