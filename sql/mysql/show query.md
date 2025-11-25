```mysql
SHOW DATABASES;
SHOW CREATE DATABASE dbname;
```

```mysql
SHOW TABLES:
SHOW FULL TABLES; -- list with tabel tyep (BASE Table / VIEW)
SHOW CREATE TABLE tablename;
SHOW TABLE STATUS LIKE 'table%'; -- detailed info (engine, rows size, collation)
```

```mysql
SHOW COLUMNS FROM tablename;
SHOW FULL COLUMNS FROM tablename; -- with collaction & privileges
SHOW INDEX FROM tablename;
```

```mysql
SHOW GRANTS FROM 'user'@'host';
```

```mysql
SHOW PROCESSLIST; -- currently running queries
SHOW VARIABLES; -- server/system variables
SHOW GLOBAL VARIABLES LIKE 'innodb%'; -- Filtered system vars
SHOW STATUS; -- server status counters
SHOW GLOBAL STATUS LIKE 'Threads%'; -- filtered status
```

```mysql
SHOW ENGINES; -- available storage engines
SHOW PLUGINS; -- installed plugins
```

```mysql
SHOW BINARY LOGS; -- binary logs on server
SHOW MASTER STATUS; -- current binary log file & position
SHOW EVENTS; -- scheduled events
```

**Show view table for current database**
```mysql
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = DATABASE();
```
