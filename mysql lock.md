`LOCK TABLES` -> manually locks entire tables to control concurrency.

```txt
LOCK TABLES table_name [READ | WRITE];
```

**Read lock**
- others can read
- others cannot write
- you also cannot write to the table
- used for consistent reads

**Write lock**
- others cannot read or write
- you can read & write
- Ensures exclusive write access