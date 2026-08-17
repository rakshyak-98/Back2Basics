[[Database]] [[memory engine]] [[mysql engine]] [[WiredTiger storage engine]] [[SQL/postgres]]

# Browser engine

> Not a database topic—this note clarifies the naming collision between **browser rendering engines** (Blink, Gecko, WebKit) and **database storage engines** ([[mysql engine]], [[WiredTiger storage engine]]).

```txt
        Browser engine ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Rare as a standalone question

## Sources
- [MDN Web Docs — Browser engine](https://developer.mozilla.org/en-US/docs/Glossary/Engine) — overview
- [MySQL Reference Manual — Storage Engines](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — overview

## Key Concepts
- **Browser engine (web):** interprets HTML/CSS/JavaScript and paints pixels → Blink, Gecko, WebKit.
- **Database storage engine:** manages on-disk structures, transactions, buffer pools, recovery → InnoDB, Po…
- **Shared word, different layers:** “engine” alone is ambiguous in staff conversations → always qualify.

## Technical Details
- Browser engines (web):

- Chromium Blink, Firefox Gecko, Safari WebKit
- Job: parse markup, layout, paint, run JS

- Database engines (storage):

- Manage pages, indexes, [[ACID]], crash recovery
- Examples: InnoDB ([[mysql engine]]), PostgreSQL heap/index AMs ([[SQL/postgre…

- If you landed here looking for MySQL or PostgreSQL internals, see [[mysql eng…

## Mistakes to Avoid
- **Mistake:** Assuming “browser engine” in a database folder means a storage e…
- **Mistake:** Using bare “engine” in design docs without saying storage vs ren…

## Comparison
- vs [[mysql engine]] / [[memory engine]]: those notes cover real storage engin…


### Use cases
- Onboarding docs and interviews where “switch the engine” could mean Chromium …
