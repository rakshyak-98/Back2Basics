`visudo` -> safely edit the system's `sudoers` file `/etc/sudoers`. 

```bash
sudo -lU <user>; 
sudo -u developer sudo nginx -t;
```

> [!WARNING]
> sudo reads /etc/sudoers.d/* in lexical order (alphabetical).

- Located at `/etc/sudoers` 

> [!NOTE]
> - Controls the privileges and permissions for users and groups to execute administrative commands.
> - The `sudo` command is used to execute `visudo` with superuser (root) privileges since editing the `sudoers` file requires administrative access.

```bash
# template of sudoers fiel : 
# <user/group>  <host>=(<run as user>:<run as group>) <sepecial>: <commands to allow>
# %group_name - syntax to define group permission
john   ALL=(root)   /usr/bin/apt-get
```

```text
who   where   =   (as_whom : as_which_group)   what
```

|Position|Value|Meaning|
|---|---|---|
|1. Who (User_List)|ALL|**Any user** (including root, normal users, system users, etc.)|
|2. Where (Host_List)|ALL|On **any host** (this rule applies no matter what machine name is)|
|3. As whom (Runas_List – user part)|ALL|Can run commands **as any user** (root, any other account, etc.)|
|4. As which group (Runas_List – group part)|ALL|Can run commands **as any group** (using `-g` option)|
|5. What (Cmnd_List)|ALL|Can run **any command** (with or without arguments)|

When you see just ALL ALL=(ALL) ALL (without the second :ALL), it means:

> Can run as any **user**, but **not** as any arbitrary group (the group stays the original user's primary group unless -g is explicitly used).

## Extending sudoers file to include user specific sudoers config files

> [!WARNING]
> Allowing per-user sudoers files in home directories would be a **major security risk**:
> - Users could edit their own files to grant themselves unlimited privileges.
> - Malicious scripts or compromised accounts could modify these files undetected

1. `user_or_group`: user or group to whom the rule applies. It can be a specific user (e.g., "john"), a group name (e.g., "%developers"), or the keyword "ALL," representing all users.
2. `host`: This field defines the system or host-names where the rule is valid. It can be the name of a specific host (e.g., "localhost") or the keyword "ALL," indicating the rule applies to all hosts.
3. `(runas_user)`: This optional field specifies the user as whom the command should be run. If omitted, the command is executed as the root user. For example, if you want to allow a user to run a specific command as another user (e.g., "www-data"), you would include "(www-data)" in this field.
4. `commands`: This field contains the commands or command patterns that the user or group is allowed to run. It can be a specific command (e.g., `/usr/bin/apt-get`), a command with wildcard patterns (e.g., `/usr/bin/*`), or the keyword `ALL` allowing the user or group to run any command.

> [!NOTE]
> - the `/etc/sudoers` file should only be edited using the `visudo` command which ensures the file is edited by one user at a time and performs syntax checks.

> [!WARNING]
> - Errors or bad syntax in the `/etc/sudoers` may result in locking out all users.

```bash
<username> <hostname>(user:group) command
# username - specifies the user the rule applies to
# hostname - the machine the rule applies to
# user:group - user and group the rule applies to usually ALL
# command - the command user is allow to run
# NOPASSWD - allow the user to run the specified command without a password

# to allow user john to run the /usr/bin/foo and /usr/bin/bar commands as root witthout a password
john ALL=NOPASSWD: /usr/bin/foo /usr/bin/bar
%sudo	ALL=(ALL:ALL) NOPASSWD:ALL # allow sudo command to run without password
```

### Sudoers file naming

> [!NOTE]
> Use `zz-` prefix for your temporary/test rule so they win precedence.

|Prefix|Purpose|Example filename|
|---|---|---|
|`00-`|Very early overrides / defaults|`00-defaults`|
|`10-`|Group definitions / aliases|`10-groups`, `10-cmnd-aliases`|
|`20-`|Service accounts / automation users|`20-deployer-nopasswd`|
|`50-`|Per-team / per-role rules|`50-dev-team`, `50-monitoring`|
|`90-` / `zz-`|Last-resort overrides / catch-all|`zz-emergency-root`, `zz-nginx-reload`|

### Sudoers file pattern

```text
# /etc/sudoers.d/50-dev-team
User_Alias DEV_TEAM = alice,bob,charlie

Cmnd_Alias LOGS_AND_STATUS = /usr/bin/journalctl *, \
                             /usr/bin/tail -f /var/log/*

Cmnd_Alias SERVICE_CONTROL = /bin/systemctl status *, \
                             /bin/systemctl restart myapp.service

DEV_TEAM ALL=(ALL) NOPASSWD: LOGS_AND_STATUS
DEV_TEAM ALL=(ALL)         PASSWD: SERVICE_CONTROL   # password for restarts
```
