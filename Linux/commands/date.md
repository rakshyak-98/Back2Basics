
```bash

date -d "+7 days" +%s;
date -d "+30 minutes" +%s

date -u -d "2026-12-31 23:59:59" +%s; # UTC timestamp
```
- `-d` → parse date string (GNU/Linux)
- `+7 days`, `+1 year` → relative future date
- `+%s` → Unix timestamp (seconds)
- `-u` → UTC timezone