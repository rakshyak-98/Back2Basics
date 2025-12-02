## Permission
```mysql
SHOW GRANTS FROM 'username'@'host';
SHOW PRIVILEGES;
```

> [!NOTE]
> `GRANT USAGE ON *.*` user exists but has no actual privileges.
> `USAGE` zero privileges placeholder
> `ON *.*` global scope
> MySQL shows this when the user has no rights beyond login
> User can authenticate but cannot read/write anything

```mysql
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'host';

REVOKE ALL PRIVILEGES ON db_name.* FROM 'user'@'host';
REVOKE GRANT OPTION ON *.* FROM 'user'@'%';
```

#### Grant specific privileges
```mysql
GRANT SELECT, INSERT, UPDATE, DELETE ON db_name.* TO 'user'@'host';
```
