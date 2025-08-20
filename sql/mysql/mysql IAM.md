## Permission
```mysql
SHOW GRANTS FROM 'username'@'host';
SHOW PRIVILEGES;
```

```mysql
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'host';

REVOKE ALL PRIVILEGES ON db_name.* FROM 'user'@'host';
REVOKE GRANT OPTION ON *.* FROM 'user'@'%';
```

#### Grant specific privileges
```mysql
GRANT SELECT, INSERT, UPDATE, DELETE ON db_name.* TO 'user'@'host';
```
