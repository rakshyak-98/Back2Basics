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

```mysql
SHOW FUNCTION STATUS WHERE Db = 'mysql';
```

## Data conversion
### Type conversion
```mysql
SELECT CAST('123' AS UNSIGNED);
SELECT CONVERT('2024-01-01', DATE);
```

### Date/Time Conversion
```mysql
SELECT STR_TO_DATE('27-05-2025', '%d-%m-%Y');
SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s');
```