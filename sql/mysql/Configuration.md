```ini
[client]
user=myuser
password=mypassword
host=127.0.0.1

[mysql]
pager=less -S
prompt="\u@\h> "

[mysqldump]
quick=TRUE
single-transaction=TRUE

```

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


## Dump configuration
```bash
mysqldump --routine <database name> > dump.sql;
mysqldump --routine --triggers <database name> > dump.sql;
```

> [!NOTE]
> By default `mysqldump` does not include stored routines (functions + procedures)
> Must add the flag.