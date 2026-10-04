```sql
SHOW VARIABLES LIKE 'repl%'; -- view the replication configurations
```

### Create replication
```sql
CREATE REPLICATION SOURCE TO 
SOURCE_HOST=
SOURCE_USER=
SOURCE_PASSWOR=
SOURCE_AUTO_POSITION=
```

```sql
START REPLICA;
STOP REPLICA;
SHOW REPLICA STATUS\G
```

> [!NOTE]
> On follower database the there should not be already existing database. A `server_id` on each server is required. Binary logging enabled on the source. A dedicated user shold exist on the leader.

```sql
SHOW BINARY LOGS STATUS;
SHOW VARIABLES LIKE 'log_bin';
SHOW VARIABLES LIKE 'binlog_format';
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'enforce_gtid_consistency';
```