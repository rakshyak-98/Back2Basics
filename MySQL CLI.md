
```bash
mysqlcheck -u root -p mydb mytable; # check db table status.
```

```bash
mysqld --verbose --help | grep -A1 "Default options"
```

### Dump database
```bash
mysqldump --no-create-info <database> > only-data.sql
```

> [!NOTE]
> for bulk append imports, temporarily disable FK check.
```mysql
SET FOREIGN_KEY_CHECKS = 0;
SOURCE safe_dump.sql;
```
