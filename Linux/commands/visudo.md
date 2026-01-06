`visudo` is a command-line utility used to safely edit the system's sudoers file `/etc/sudoers`. 

- The sudoers file, typically located at `/etc/sudoers` 
- controls the privileges and permissions for users and groups to execute administrative commands.
- The `sudo` command is used to execute "visudo" with superuser (root) privileges since editing the `sudoers` file requires administrative access.

```bash
# template of sudoers fiel : 
# <user/group>  <host>=(<run as user>:<run as group>) <sepecial>: <commands to allow>
# %group_name - syntax to define group permission
john   ALL=(root)   /usr/bin/apt-get
```

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
