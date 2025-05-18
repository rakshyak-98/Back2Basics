#### User-defined session variable
```mysql
SET @my_var = 42;
SELECT @my_var;

```

### local variable (inside stored routines)
```mysql
DECLARE my_var INT;
SET my_var = 100;

```

> [!NOTE] 
> - `@var` persists across queries in same session
> - `DECLARE` only works inside `BEGIN...END`