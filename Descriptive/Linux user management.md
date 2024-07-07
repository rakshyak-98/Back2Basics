user, user with elevated privileges, root.

> NOTE: we can limit the functionality of the elevated user.

```bash
whoami; # 
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
-d; # create home directory in specified location, if we want to change.
-m; # create the home directory;
-p; # passowrd
-s; # shell
-c; # commnets, or description of the account
usermod -aG <user>; # a- append
## it is good practice to append.
userdel -rf <user>; # delete home directory also otherwise not deleted.
```