[[Database]] [[memory engine]] [[mysql engine]] [[WiredTiger storage engine]] [[SQL/postgres]]

# Browser engine

> Not a database topic—this note clarifies the naming collision between **browser rendering engines** (Blink, Gecko, WebKit) and **database storage engines** ([[mysql engine]], [[WiredTiger storage engine]]).





## Interview Relevance
Rare as a standalone question; useful when candidates confuse “engine” vocabulary across web and databases. Shows you can disambiguate rendering engines from storage engines that own [[ACID]], buffer pools, and recovery.

## Sources
- [MDN Web Docs — Browser engine](https://developer.mozilla.org/en-US/docs/Glossary/Engine) — overview
- [MySQL Reference Manual — Storage Engines](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — overview

## Key Concepts
- **Browser engine (web):** interprets HTML/CSS/JavaScript and paints pixels → Blink, Gecko, WebKit.
- **Database storage engine:** manages on-disk structures, transactions, buffer pools, recovery → InnoDB, PostgreSQL access methods, WiredTiger.
- **Shared word, different layers:** “engine” alone is ambiguous in staff conversations → always qualify.

## Technical Details
Browser engines (web):

- Chromium Blink, Firefox Gecko, Safari WebKit
- Job: parse markup, layout, paint, run JS

Database engines (storage):

- Manage pages, indexes, [[ACID]], crash recovery
- Examples: InnoDB ([[mysql engine]]), PostgreSQL heap/index AMs ([[SQL/postgres]]), WiredTiger ([[WiredTiger storage engine]]), MySQL [[memory engine]]

If you landed here looking for MySQL or PostgreSQL internals, see [[mysql engine]] or [[SQL/postgres]].

## Real-World Applications
Onboarding docs and interviews where “switch the engine” could mean Chromium vs Firefox *or* InnoDB vs MEMORY. Example: a ticket titled “engine OOM” needs one clarifying question before you look at browser tabs or InnoDB buffer pool.

## Comparison
vs [[mysql engine]] / [[memory engine]]: those notes cover real storage engines; this note only maps the naming collision so you route to the right leaf.

## Mistakes to Avoid
- Assuming “browser engine” in a database folder means a storage engine — it does not.
- Using bare “engine” in design docs without saying storage vs rendering.
