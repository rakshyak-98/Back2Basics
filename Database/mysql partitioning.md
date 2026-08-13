[[partitioning]] [[mysql data partition]] [[mysql/mysql partitioning]] [[mysql table]]

# mysql partitioning

> Routing note for MySQL table partitioning—when to split tables by RANGE/LIST/HASH and where to find detailed syntax in [[mysql/mysql partitioning]].

## Why partition

- Fast retention (`DROP PARTITION` vs `DELETE` millions of rows)
- Partition pruning when queries filter on the partition key
- Manageable maintenance windows per time slice

## Start here

| Depth | Note |
|-------|------|
| Concepts | [[partitioning]] |
| DDL examples | [[mysql data partition]] |
| MySQL rules | [[mysql/mysql partitioning]] |

## Sources

- MySQL Reference Manual — [Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html)
