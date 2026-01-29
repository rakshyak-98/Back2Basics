```shell
gpg --full-generate-key; # generate gpg key
gpg --list-secret-keys --keyid-format=long;
gpg --armor --export <your email>; # export your public key
```

```shell
git config --get commit.gpgsign;
git log --show-signature;
```

#### Configure git to use GPG key

```shell
git config user.signingkey <gpg key>;
git config commit.gpgsign true; # enable auto-sign
git config tag.gpgsign; # enable auto sign for tags
```

```shell
git commit -S -m <commit message>; # if auto-sign is not eanble
```

#### SSH

```shell
git conifg gpg.format ssh;
git config user.signingkey <path to ssh .pub file>;
```

## Git clone

```bash
git clone -b <branch> --single-branch --depth 1 <repo-url>;
```

## Configure git refs

```ini
[branch "your-current-branch"]
    remote = origin
    merge = refs/heads/main
```
- this tells Git: "When I do `git pull` (`git merge` without argument) while on this branch, fetch from `origin` and merge the branch called `main` from the remote"

> [!INFO]
> - if the remote main branch name changed (`master` -> `main` or you renamed it)

```bash
git branch --set-upstream-to=origin/main; # safest & cleanest (set tracking to remote main)
```
- This automatically sets `remote = origin` `merge = refs/heads/main`

Manually with config

```bash
git config branch.<your branch name>.remote origin;
git config branch.<your branch name>.merge refs/heads/main;
```

```bash
git config --get-branch.$(git branch --show-current).merge;
```

Want `git pull` command to `rebase` instead of merge

```bash
git config branch.<your-branch-name>.rebase true;
git config --global pull.rebase true; # merges / interactive / false
```

(When things are messy) Full reset 

```bash
git branch --unset-upstream;
git branch --set-upstream-to=origin/main
```

```bash
git fetch --prune origin; # clean up deleted remote branches
git branch --set-upstream-to=origin/main;
git pull;
```