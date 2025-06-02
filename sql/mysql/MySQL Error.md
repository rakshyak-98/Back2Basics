```txt
ERROR 145 (HY000): Table './mydb/mytable' is marked as crashed
```
- table fails to query

> [!WARNING]
> backup the `.MYD` and `.MYI` files before running repair.
> Does not fix `.ibd` corruption, use physical recovery tools for that.