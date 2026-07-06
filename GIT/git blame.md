[[git]]
## Git blame

- shows line-by-line annotations of a file, identifying the commit and author responsible for each line of code.

```shell
git blame <file>;

# Displays blame annotations based on the file state in a specific commit.
git blame <commit hash> -- <file>;
git blame --date=short <file>;
git blame -C <file>; # Tracks code change even if the fiel was renamed.
```


```bash
# Detect moved/renamed lines within file
git blame -M src/app.js

# Detect lines moved from other files
git blame -C src/app.js

# More aggressive copy detection
git blame -C -C -C src/app.js

# Ignore whitespace changes
git blame -w src/app.js

# Combine: ignore whitespace, detect moves/copies
git blame -w -M -C src/app.js
```