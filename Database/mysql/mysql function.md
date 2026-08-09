[[mysql]] [[mysql Programmable SQL]] [[mysql query]]

# mysql function

> Stored functions return one value for use in SQL expressions; procedures run action batches via `CALL`. Also: CAST/CONVERT helpers.

---

## Index

- [[#Mental model]]
- [[#Interview map (words you can say)]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Functions are for computing a scalar inside `SELECT`; procedures are for multi-statement work with optional OUT params — functions must not do arbitrary DML/txn control the way procedures can.

```txt
SELECT tax(price) FROM items;     ── function
CALL AddHotel('Name');            ── procedure
CAST / CONVERT / DATE_FORMAT      ── built-in conversion
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Function** | Returns one value | “Usable in expressions.” |
| **Procedure** | Actions / result sets | “CALL; can COMMIT in older patterns.” |
| **DETERMINISTIC** | Same in → same out | “Needed for some optimizations.” |
| **DELIMITER** | Client statement end | “Change to define bodies with `;`.” |
| **CAST/CONVERT** | Type coercion | “Fix comparisons and joins.” |

---

## Standard config / commands

```sql
DELIMITER //
CREATE FUNCTION add_tax(p DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  RETURN p * 1.18;
END //
DELIMITER ;

DROP FUNCTION IF EXISTS add_tax;

CREATE PROCEDURE AddHotel(IN name VARCHAR(100))
BEGIN
  INSERT INTO Hotels (hotel_name) VALUES (name);
END;

SHOW FUNCTION STATUS WHERE Db = 'mydb';
SELECT ROUTINE_NAME FROM information_schema.ROUTINES
WHERE ROUTINE_TYPE = 'FUNCTION' AND ROUTINE_SCHEMA = 'mydb';

SELECT CAST('123' AS UNSIGNED);
SELECT STR_TO_DATE('27-05-2025', '%d-%m-%Y');
SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s');
```

| Knob | Why it matters |
|------|----------------|
| DETERMINISTIC / NO SQL | Optimizer + binary logging rules |
| DEFINER | Runs as definer privileges — security |
| Built-ins | Prefer CAST over UDFs when enough |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t use function in SQL | Created as procedure? | CREATE FUNCTION + RETURNS |
| Binary logging errors | Non-deterministic UDF | Mark correctly; adjust binlog settings |
| DELIMITER issues in clients | GUI eats `;` | Set delimiter; or use migration tools |
| Wrong date parse | Format mismatch | Match `STR_TO_DATE` format string |

---

## Gotchas

> [!WARNING]
> **DEFINER rights** — a function can run with elevated privileges; audit who owns it.

> [!WARNING]
> **UDFs in hot WHERE clauses** — often kill index use; prefer expressions/generated columns.

---

## When NOT to use

- **Business workflows with side effects** — app service + transaction.
- **Replacing simple CAST** — don’t write a UDF for `CAST(x AS UNSIGNED)`.

---

## Related

[[mysql Programmable SQL]] [[mysql triggers]] [[mysql query]] [[variables]]
