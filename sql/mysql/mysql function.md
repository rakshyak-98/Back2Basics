```mysql
DELIMITER //

CREATE FUNCTION function_name (param1 TYPE, param2 TYPE, ...)
RETURNS return_type
DETERMINISTIC -- or NONDETERMINISTIC
BEGIN
  -- Logic here
  RETURN some_value;
END //

DELIMITER ;

```

```mysql
DROP FUNCTION IF EXISTS add_tax;
```

```mysql
SELECT ROUTINE_NAME
FROM information_schema.ROUTINES
WHERE ROUTINE_TYPE = 'FUNCTION'
  AND ROUTINE_SCHEMA = 'your_database_name';

```