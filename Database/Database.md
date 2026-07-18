- you risk data loss in crashes during an update. The resource can end up half written, truncated, or even missing. That is why you need Atomicity and Durability in a database
**Atomicity** means that data is either updated or not, not in between.
**Durability** means that data is guaranteed to exist after certain point.

## When updating time entry in table

> [!NOTE]
> **Server-Side Time Drift** -> if is expiry check runs on a distributed system (multiple servers), and their internal clocks are not synced via NTP, one server might expire a resource while another considers it valid.

Time Zone mismatch -> The `new Date()` constructor use the local system time of the environment (server or browser). if your database stores UTC but your server runs on EST, the "end of the day" calculation will be off by several hours, causing premature or delayed expiration.

> [!WARNING]
> Client side Manipulations -> if `new Date()` runs in the browser to gate content, a user can simply change their system clock to "extend" the expiration. Never rely on this for security-sensitive logic (like session or subscription validation) without a server-side check.
