### reset the credential manager

```bash
git config --global --unset credentila.*; # remove the set credential helper
git clone <https remote repo url>;
git pull; # git will ask the username and auth token.

```
- create auth token from [GitHub personal access token](https://github.com/settings/tokens)
- paste the auth token password.

```bash
git config --global credential.helper cache;

```
- the `cache` helper stores credentials in memory only, not on disk.
- Git spawn the credentials cache daemon in the background.
- it keeps the credentials in RAM for 15 minutes by default.
- no file is written.
- once expired or system restarts -> the data is gone.

```bash
# After login, run to view the saved credentials
printf "protocol=https\nhost=github.com\n\n" | git credential fill;

```

> [!INFO]
> When accessing `https://github.com`, ask the GitHub CLI (gh) to provide credentials.

> [!INFO]
> credential.helper -> controls how Git remembers (or not) those credentials.
> `store` -> stores them permanently in `~/.git-credentials` in plain text.
> `gpt` -> Encrypts credentials with GPG (custom setup).

> [!NOTE]
> git doesn't allow direct removal of just one value from a __multi-value section__ like this

```ini
[credential "https://github.com"]
helper = 
helper = !/usr/bin/gh auth git-credential
```

- remove the full section
```bash
git config --global --remove-section credential."https://github.com";

```

- Re-add only the correct value
```bash
git config --global credential."https://github.com".helper '!/usr/bin/gh auth git-credential'

```

### Pre-host credential control 

- only affects `https://github.com`. All other Git Hosts (e.g., GitLab, Bitbucket) still use default helper (like `cache` or `store`).

```bash
# 1. When git runs a command like `git push` it internally calls.
git credential fill;

```
- and because of your config, Git delegates that to `credential.helper`

```bash
/usr/bin/gh auth git-credential;

```