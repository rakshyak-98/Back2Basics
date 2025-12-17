user, user with elevated privileges, root.
```bash
visudo; # configure elevated privileges
```

|Group name|Typical GID|Purpose|Typical members|
|---|---|---|---|
|wheel or sudo|10|Allow sudo access|Admins|
|docker|~998|Allow use of Docker without root|Developers|
|adm||Read logs in /var/log|Monitoring users|
|audio, video||Access sound card, webcam|Desktop users|
|users|100|Legacy “all normal users” group|Everyone|

> NOTE: we can limit the functionality of the elevated user.

```bash
whoami;
id;

# category
# UID 0; reserved for root.
# 1- 99; reserved for predefined accrounts (games, mail, www-data, sys, bin).
# 100-999; reserved for system and administrative accounts.
# 1000+ are reserved for users.
```

- group : abstract combines many users in similar entity (for the same privileges, purpose, actions etc.).

```bash
## GID
# 1-99; reserved for system and application
# 100+; are for users.
```

## Configuration 

- To differentiate `user` and `group`, we user `%` for specify the group.
- `pos1` - applies to all hosts
- `post2` - user can use all commands as all users
- `post2` - user can use commands as all groups
- `pos4` - user can use all commands
4 files involved in configuration of users.

### `passwd`

```bash
# username; name of the user
# password; x means pasword encrypted and stored in different file.
# description; can have real first and last name. Role in organization.
# homedir; home directory of the user, where logs and data store.
# shell; find all the available shells /etc/shells
## /sbin/nologin; user no need to have login. No actoin perform intrectively.
## /usr/sbin/nogin;
```

### `shadow`

```bash
## the other file or magic file
## sensitive information about the user, like passwrd, other configuration.
## * no password set.
## ! password never set.
```

### `group`

there is possibility to have password set for groups.

- **adm**: Allows reading many system log files in /var/log/ (e.g., for monitoring and troubleshooting). Historically tied to old log directories like /var/adm.
- **cdrom**: Grants access to optical drives (CD/DVD/Blu-ray) for mounting and using them without root privileges.
- **sudo**: Permits full administrative access via the sudo command (run commands as root after entering your password). This is the primary group for system administration on modern Ubuntu.
- **dip** (Dial-Up Internet Protocol): Historically allowed access to modem/PPP connections and related config files for dial-up internet. Less relevant today but still included for compatibility.
- **plugdev**: Allows mounting and unmounting removable/external storage devices (e.g., USB drives, external hard disks) via tools like udisks/polkit, often without needing a password prompt.
- **lpadmin**: Enables full management of printers via CUPS (add/remove printers, configure queues, manage print jobs—including those from other users).
- **sambashare**: Facilitates sharing files/folders over the local network using Samba (e.g., easier setup for Windows-compatible file sharing).

## user creating

```bash
useradd -d -m -s /bin/sh -c "SDE team";
## it is good practice to append.
usermod -aG user;
userdel -rf user; # delete home directory also otherwise not deleted.
```

## How to manage Permissions

|Category|Meaning|Who it applies to|
|---|---|---|
|**u** (user/owner)|The user who owns the file|Usually the creator of the file|
|**g** (group)|The group that owns the file|All users who are members of that group|
|**o** (others)|Everyone else on the system|Users not owner and not in the owning group|