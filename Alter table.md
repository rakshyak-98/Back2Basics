## Tables

```mysql
ALTER TABLE Hotels COMMENT = 'Table storing hotel information';
```

## Columns

```mysql
ALTER TABLE Hotels 
MODIFY COLUMN phone VARCHAR(10) COMMENT 'Hotel contact phone number',
MODIFY COLUMN address VARCHAR(200) COMMENT 'Hotel physical address';
```