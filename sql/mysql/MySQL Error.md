```txt
ERROR 145 (HY000): Table './mydb/mytable' is marked as crashed
```
- table fails to query

> [!WARNING]
> backup the `.MYD` and `.MYI` files before running repair.
> Does not fix `.ibd` corruption, use physical recovery tools for that.

```text
ERROR 1045 (28000): Access denied for user 'root'@'_gateway' (using password: YES)
```
- because there is no user account that matches


> Why "\_gateway" appears ?
> Most cloud providers put a NAT gateway or proxy in front of your connection. From MySQL server's point of view the connection is comming from a host literally called  `_gateway`

> Solution
> - create a user that is allowed from anywhere

### Bonus: If this is AWS RDS / Aurora

> [!NOTE]
> RDS does **not** allow real root remote login at all for security reasons. You must:

1. Create a new DB user in the RDS console or with SQL
2. Make sure the RDS security group allows your IP (or 0.0.0.0/0 if public)
3. Connect with that new user, not root