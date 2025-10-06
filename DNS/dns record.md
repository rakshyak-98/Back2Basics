## Dignosis

```bash

```

> [!NOTE]
> The TTL (time to live) of that DNS record tells how long resolvers cache your DNS entry before rechecking

```bash
# check current TTL
dig yourdomain.com cname;
```
- before deleting or changing records, lower TTL to 300, wait for old TTL to expire, then make the change -> almost instant reflection next time.
