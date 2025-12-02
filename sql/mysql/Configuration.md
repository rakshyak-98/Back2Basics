```ini
[client]
user=myuser
password=mypassword
host=127.0.0.1

[mysql]
pager=less -S
prompt="\u@\h> "

[mysqldump]
quick=TRUE
single-transaction=TRUE

```

	
## Constraint safe update

**in `.my.cnf`** file
```ini
[mysqld]
sql_safe_update=1
```


## Dump configuration
```bash
mysqldump --routine <database name> > dump.sql;
mysqldump --routine --triggers <database name> > dump.sql;
```

> [!NOTE]
> By default `mysqldump` does not include stored routines (functions + procedures)
> Must add the flag.