[[Database]] [[memory engine]]

# Browser engine

> Not a database topic—this note clarifies the naming collision between **browser rendering engines** (Blink, Gecko, WebKit) and **database storage engines** ([[mysql engine]], [[WiredTiger storage engine]]).

## Browser engines (web)

Interpret HTML/CSS/JavaScript and paint pixels. Examples: Chromium Blink, Firefox Gecko, Safari WebKit.

## Database engines (storage)

Manage on-disk structures, [[ACID]], buffer pools, and recovery. Examples: InnoDB, PostgreSQL heap access methods, WiredTiger.

If you landed here looking for MySQL or PostgreSQL internals, see [[mysql engine]] or [[SQL/postgres]].

## Sources

- MDN Web Docs — [Web browser engine](https://developer.mozilla.org/en-US/docs/Glossary/Engine)
- MySQL Reference Manual — [Storage Engines](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html)
