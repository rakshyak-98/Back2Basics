
| Feature                 | **Stored Procedure**                                            | **Function**                                        |
| ----------------------- | --------------------------------------------------------------- | --------------------------------------------------- |
| **Purpose**             | Perform actions (insert, update, delete, complex logic)         | Compute and return a single value                   |
| **Return type**         | No mandatory return; can use OUT params                         | Must return exactly one value (`RETURNS data_type`) |
| **Usage context**       | Called via `CALL proc_name(...)`                                | Used inside SQL (e.g., `SELECT func_name(...)`)     |
| **Allowed operations**  | Can use DML: `INSERT`, `UPDATE`, `DELETE`, `COMMIT`, `ROLLBACK` | Cannot modify data (only read/select)               |
| **Transaction control** | Allowed (`START TRANSACTION`, `COMMIT`, `ROLLBACK`)             | Not allowed                                         |
| **Return mechanism**    | OUT/INOUT parameters or result sets                             | Single scalar return via `RETURN`                   |
| **Determinism**         | Not required                                                    | Must be deterministic for index usage               |
| **Performance usage**   | Used for business logic workflows                               | Used for computed columns or expressions in queries |

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

sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
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

### Numeric Conversion
```mysql
SELECT CONV('1010', 2, 10);  -- binary 1010 → decimal 10
```

## Procedure
```sql
SHOW PROCEDURE STATUS WHERE Db = 'your_database_name';

SELECT ROUTINE_NAME
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_TYPE = 'PROCEDURE'
  AND ROUTINE_SCHEMA = 'your_database_name';
```

```mysql
CREATE PROCEDURE AddHotel(IN name VARCHAR(100))
BEGIN
  INSERT INTO Hotels (hotel_name) VALUES (name);
END;
```

```mysql
CALL AddHotel('Hilton');
```

```sql
DELIMITER $$

CREATE PROCEDURE GetHotelSectionsByPage(
  IN p_hotel_id INT,
  IN p_page_name VARCHAR(255)
)
BEGIN
  SELECT 
    hs.id AS hotel_section_id,
    ts.section_name,
    ts.type AS section_type,
    hs.is_active
  FROM Hotels AS h
  JOIN HotelPages AS hp 
    ON hp.hotel_id = h.id
  JOIN TemplatePages AS tp 
    ON tp.id = hp.template_page_id
  JOIN HotelSections AS hs 
    ON hs.hotel_page_id = hp.id
  JOIN TemplateSections AS ts 
    ON ts.id = hs.template_section_id
  WHERE h.id = p_hotel_id
    AND tp.page_name = p_page_name
    AND tp.template_id = h.current_template_id;
END$$

DELIMITER ;
```