[[mysql]] [[mysql columns]] [[key Constraint]] [[Alter table]] [[mysql index]]

# mysql table

> InnoDB tables store rows in clustered primary-key order—DDL defines columns, constraints, and indexes that shape every [[mysql query]] plan.

## Create example

```sql
CREATE TABLE orders (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id    BIGINT UNSIGNED NOT NULL,
  total      DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_orders_user (user_id),
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## InnoDB clustered index

The **primary key** is the table—secondary indexes leaf nodes point to primary key values. Choose narrow, monotonic PKs (`BIGINT AUTO_INCREMENT`) for insert performance.

## Alter safely

See [[Alter table]] — large `ALTER` may rebuild the whole table. Use online DDL options when available.

## Sources

- MySQL Reference Manual — [CREATE TABLE](https://dev.mysql.com/doc/refman/en/create-table.html)
- MySQL Reference Manual — [Clustered and Secondary Indexes](https://dev.mysql.com/doc/refman/en/innodb-index-types.html)
