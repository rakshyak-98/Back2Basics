## Allow local private IP to connect to local mysql server

```mysql
CREATE USER '<user>'@'<private ip>' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON database_name.* TO 'nodeuser'@'<private ip>';
SHOW GRANTS FOR '<user>'@'<private ip>';
FLUSH PRIVILEGES;
```

```mysql
GRANT ALL PRIVILEGES ON hotel_cms.* TO 'nodeuser'@'192.168.3.106' IDENTIFIED BY 'password123';
FLUSH PRIVILEGES;
```
	
## Constraint safe update

**in `.my.cnf`** file
```ini
[mysqld]
sql_safe_update=1
```

```mysql
SET sql_safe_updates=1;
SET GLOBAL sql_safe_updates=1; -- restart server or reconnect client for effect
SET GLOBAL general_log=1;
```

## Dump configuration
```bash
mysqldump --routine <database name> > dump.sql;
mysqldump --routine --triggers <database name> > dump.sql;
```

> [!NOTE]
> By default `mysqldump` does not include stored routines (functions + procedures)
> Must add the flag.