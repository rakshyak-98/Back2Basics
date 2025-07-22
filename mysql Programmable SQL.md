
```mysql
PROCEDURE stmt FROM 'UPDATE table_name set column_name = ? where id = 1';
SET @json = '[]';
EXECUTE stmt USING @json;
DEALLOCATE PROCEDURE stmt;
```

|Name|MySQL Term / Category|Description|
|---|---|---|
|`PREPARE`, `EXECUTE`|**Prepared Statements**|Runtime dynamic SQL with placeholders|
|`Stored Procedure`|**Stored Routine**|Reusable block of SQL with input/output params|
|`Function`|**Stored Function**|Returns a single value; used in SQL expressions|
|`Trigger`|**Trigger**|Auto-run SQL on table events (`INSERT`, etc.)|
|`Event`|**Event Scheduler / Event**|Scheduled SQL tasks|
|`View`|**View (Virtual Table)**|Query abstraction; read-only or updatable|
|`User-defined Variable`|**Session Variable**|Temporary scoped variable prefixed with `@`|
|`Control Flow` (`IF`, etc.)|**Flow Control Constructs**|Logic inside procedures/functions|
|`EXECUTE IMMEDIATE`|Not in SQL; MySQL Shell only|Used in `mysqlsh`, not standard MySQL SQL|