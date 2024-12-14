- you risk data loss in crashes during an update. The resource can end up half written, truncated, or even missing. That is why you need Atomicity and Durability in a database
**Atomicity** means that data is either updated or not, not in between.
**Durability** means that data is guaranteed to exist after certain point.