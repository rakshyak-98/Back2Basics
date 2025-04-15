Primary -> handles writes, strong consistency
Secondaries -> read-only replicate from primary
Arbiter -> votes in elections, no data
Oplog -> operation log for syncing
Failover -> auto-election on primary failure
Heartbeat -> members monitor each other


```js
rs.initiate() // initialize replica set
rs.add('host:port') // add secondary
rs.status() // check replica set status
```