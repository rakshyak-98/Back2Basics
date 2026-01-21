```txt
ERROR 145 (HY000): Table './mydb/mytable' is marked as crashed
```
- table fails to query

> [!WARNING]
> backup the `.MYD` and `.MYI` files before running repair.
> Does not fix `.ibd` corruption, use physical recovery tools for that.

```text
ERROR 1045 (28000): Access denied for user 'root'@'_gateway' (using password: YES)
```
- because there is no user account that matches


> Why "\_gateway" appears ?
> Most cloud providers put a NAT gateway or proxy in front of your connection. From MySQL server's point of view the connection is comming from a host literally called  `_gateway`

> Solution
> - create a user that is allowed from anywhere

### Bonus: If this is AWS RDS / Aurora

> [!NOTE]
> RDS does **not** allow real root remote login at all for security reasons. You must:

1. Create a new DB user in the RDS console or with SQL
2. Make sure the RDS security group allows your IP (or 0.0.0.0/0 if public)
3. Connect with that new user, not root

---

```text
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (13)

```

- means the MySQL client is trying to connect via the Unix socket file, but it cannot access it — specifically error code 13 = Permission denied.

> [!NOTE]
> Here the socket file exists, but your user mst does not have permission to read/write to it or to the parent directory.

---

```text
* Starting MySQL database server mysqld                                                                      su: warning: cannot change directory to /nonexistent: No such file or directory

```

- The mysql server process (`mysqld`) is started as the dedicated system user `mysql` (a non-login service account).
- In a clean Ubuntu installation, the `mysql` user is intentionally created without a real home directory
	- Home dir in `/etc/passwd` is set to `/nonexistent`
	- Shell is usually `/usr/sbin/nologin` or `/bin/false`

> [!INFO]
> - When the startup script (via `systemd` or `SysV` init) uses su (or sudo -u mysql) to switch to the mysql user and start `mysqld`, `su` tries to `cd` to the user's home directory first.
> - Since /nonexistent does not exist → you get the warning.

How to remove this warning

```bash
sudo systemctl stop mysql    # or sudo service mysql stop

# Set a valid home directory that already exists and is owned by mysql
sudo usermod -d /var/lib/mysql mysql

# Optional: make sure the mysql user can't log in interactively anyway
sudo usermod -s /usr/sbin/nologin mysql   # or /bin/false

sudo systemctl start mysql
# or sudo service mysql start
```