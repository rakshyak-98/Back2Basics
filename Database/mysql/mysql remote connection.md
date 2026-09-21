> Troubleshoot from the outside inward. Don't change MySQL users or passwords when the TCP port isn't reachable yet.

**Identify the server IP**
```bash
hostname -I;
ping <host ip>;
```
- if ping fails, investigate the network before touching MySQL

> Ping can be disabled by firewall rules, so a failed ping does not by itself prove the host is unreachable.

**Check MySQL is running**
```bash
sudo systemctl status mysql;
sudo systemctl start mysql;
sudo systemctl is-active mysql;
```

```bash
ss -tlnp | grep 3306;
```

```txt
LISTEN 0 151 127.0.0.1:3306 0.0.0.0:*
```
- This means MySQL is listening from localhost only. A remote machine cannot connect.

```txt
LISTEN 0 151 0.0.0.0:3306 0.0.0.0:*
```
- This means MySQL is listening on all IPv4 interfaces.

```txt
LISTEN 0 151 192.168.1.12:3306 0.0.0.0:*
```
- means MySQL is listening specifically on that interface.

## MySQL bind address

```bash
sudo grep -R "bind-address" / etc/mysql/ 2>/devnull
```

```txt
[mysqld]
bind-address = 127.0.0.1 -> 0.0.0.0
```
```bash
sudo systemctl restart mysql;
```

> Changing `ufw` alone solve a MySQL process that isn't listening on the network interface.

```bash
sudo ufw status
sudo ufw allow 3306/tcp
sudo ufw allow from 192.168.1.12 to any port 3306 proto tcp
```

```bash
sudo ufw status numbered
```

**Test tcp connection**

```bash
nc -zv 192.168.1.12 3306
```
```txt
Connection to 192.168.1.12 3306 port [tcp/mysql] succeeded!
```

**Create a user for the LAN**

```sql
CREATE USER 'app'@'192.168.1.%'
IDENTIFIED BY 'password'

-- Grant access
GRANT ALL PRIVILEGES
ON mydatabase.*
TO 'app'@'192.168.1.%';

-- refresh privileges
FLUSH PRIVILEGES;

-- check user exist
SELECT user, host
FROM mysql.user
WHERE user = 'app';
```