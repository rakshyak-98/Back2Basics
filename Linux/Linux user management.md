user, user with elevated privileges, root.
```bash
visudo; # configure elevated privileges
```

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

## user creating

```bash
useradd -d -m -s /bin/sh -c "SDE team";
## it is good practice to append.
usermod -aG user;
userdel -rf user; # delete home directory also otherwise not deleted.
```