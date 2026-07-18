```bash
AUTH <password>
KEYS *; # get list of keys
SCAN 0;
```

```bash
redis-cli
PING
SELECT 2
DBSIZE
FLUSHDB
FLUSHALL
```

```bash
SET user:1001:nam "Sarah"
GET user:1001:name

INCR visits
INCRBY visits 10
DESCRBY visits 5

SETNX lock:payment:123 true
EXPIRE lock:payment:123 30

MSET a 1 b 2 c 3
MGET a b c
```

```bash

```