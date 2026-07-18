|Path|Purpose|
|---|---|
|`/etc/apt/apt.conf.d/`|Main directory for APT global configuration snippets (most settings go here)|
|`/etc/apt/apt.conf`|Old-style single config file (rarely used now, usually empty)|
|`/etc/apt/sources.list`|Primary repository list (the most important file for a fresh install)|
|`/etc/apt/sources.list.d/`|Directory for additional `.list` files (used by PPAs, third-party repos)|
|`/etc/apt/preferences.d/`|Pinning files (control package versions and repository priority)|
|`/etc/apt/auth.conf.d/`|Credentials for private repositories|
|`/etc/apt/trusted.gpg.d/`|Additional GPG keys in separate files (modern way)|
|`/etc/apt/keyrings/`|Debsign-style GPG keys (used with `signed-by=` in sources, recommended now)|
|`/var/lib/apt/lists/`|Cached repository metadata (auto-generated)|
|`/var/cache/apt/archives/`|Downloaded `.deb` packages (can be cleaned)|


|Prefix|Meaning|Is it bad?|
|---|---|---|
|Hit:|The cached copy on your computer is still current. Nothing was downloaded.|Good / normal|
|Get:|A newer list was found on the server → APT is downloading it now.|Good / normal|
|Ign:|“Ignore” → APT contacted the repository but decided there is nothing new or nothing to do (very common for *-updates or *-backports when they are empty at the moment).|Usually harmless|
|Err:|Real error → could not reach the repository or the file is missing (404, connection timeout, etc.)|Bad – needs fixing|
|W:|Warning → something is not ideal but APT can continue (e.g. unsigned repo, hash mismatch)|Usually needs attention)|
|E:|Fatal error → APT stops. You will not be able to install/upgrade packages until it is fixed|Must be fixed|