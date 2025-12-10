
```bash
mysqldump -u root -p --no-data --skip-add-drop-table --skit-set-charset your_database > schema.sql
mysqldump -u root -p --no-data your_database table_name > table.sql
```

> Include triggers, routines, events (DDL only)

```bash
mysqldump -u root -p --no-data --routines --events --triggers your_database > schema.sql
```

> Dump all user definitions + grants

```bash
mysql -u root -p -e "SELECT * FROM mysql.user\G" > user_and_auth.txt;
```