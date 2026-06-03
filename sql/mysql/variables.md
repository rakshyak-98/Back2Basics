> [!WARNING]
> You cannot explicitly delete a mysql user variable definition. Once created, exists for the lifetime of the session.
> - Disconnect/reconnect to MySQL server which removes all session variables. Declare is not allowed outside a stored-program `BEGIN ... END` block.
> - Instead stored procedure, use `DECLARE x INT` the variable lifetime is controlled by the block

```sql
```

## User-defined session variable

```mysql
SET @my_var = 42;
SELECT @my_var;
```

```sql
SELECT * FROM users WHERE id = @user_id;
```
## local variable (inside stored routines)

```mysql
DECLARE my_var INT;
SET my_var = 100;
```

```mysql
SET sql_safe_updates=1;
SET GLOBAL sql_safe_updates=1; -- restart server or reconnect client for effect
SET GLOBAL general_log=1;
```

> [!NOTE] 
> - `@var` persists across queries in same session
> - `DECLARE` only works inside `BEGIN...END`