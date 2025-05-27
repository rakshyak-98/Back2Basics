#### Starter config
```bash
git config user.name <commit author name>;
git config user.email <commit author email>;
git config init.branch main; # main instead of master;
git config --global --unset credential.helper; # clear Git Credential Cache
```

```bash
git clean; # removes untracked files from working directory (not staged, committed, ignored)
git reflog; # view git logs (not commit)
git push origin --tags; # push local tag to remote
git remote -v;
git show-ref;
git branch -vv;
```

## Tags
```sh
git tag -a <tag_name> -m "your message"; # -a annotate tag
git push origin <tag name>;

git branch --contains <tab name>; # find branch containing the tag

git rev-list -n 1 <tag_name>; # find commit has for the tag

```
### Move tag to different commit
```sh
git tag -a <new_tag_name> <new_commit_hash> -m "updated tag"
git push origin <new_tag_name>

```

#### transfer tag from one commit to another
```bash
# 1. Delete local tag (if exists)
git tag -d <tag_name>

# 2. Recreate tag on new commit
git tag <tag_name> <new_commit_hash>

# 3. Delete remote tag (if pushed before)
git push origin :refs/tags/<tag_name>

# 4. Push new tag
git push origin <tag_name>

```

## Branch
```shell
git branch -vv; # view with remote references
git branch --set-upstream-to=origin/<branch> <local branch>;
git branch --unset-upstream <branch-name>; # detach the upstream reference from a local branch
```

### Without merge how to validate two branch have merge conflict
```shell
git checkout <target-branch>;
git merge <source-branch> --no-commit --no-ff; # dry-run merge

git diff target-branch...source-branch;

git merge-tree $(git merge-base target-branch source-branch) target-branch source-branch;

```

```bash
git tag -l "v1.*"; # filter tag based on pattern
git tag -a <tagname> -m <message>; # annotate tag with name, email, message
git show <tagname>; # see detailed information about a tag
git tag -d <tagname>; # delete a tag
git push --delete origin <tagname>; # delete remote tag
git push origin --tags; # push all tags
git checkout <tagname>; # go to specific tag
```
### Conflicts
```bash
git ls-files -u; # list files with conflicts and show details
git diff --name-only --diff-filter=U; # show conflicting files names
git rebase --continue; # git will print conflicted files directly
```
## remote
```bash
git remote remote origin;
git remote prune;
git fetch --prune;
```
## reference

| **Feature**          | **`git show-ref`**                          | **`git reflog`**                     |
| -------------------- | ------------------------------------------- | ------------------------------------ |
| **Purpose**          | Lists all refs (branches, tags) with hashes | Shows the history of changes in refs |
| **Scope**            | All branches and tags                       | Local changes (HEAD, branches)       |
| **Usage**            | Verify branch/tag refs                      | Track changes, recover lost commits  |
| **Output**           | Commit hash + ref name                      | Hash, action, date, user, message    |
| **Example Command**  | `git show-ref`                              | `git reflog`                         |
| **Typical Use Case** | View refs or check ref integrity            | Undo changes, find lost commits      |
```shell
git branch --unset-upstream; # remove reference from the remote branch
```
### Example:

**`git show-ref` Output:**
```bash
abc1234 refs/heads/main
def5678 refs/tags/v1.0
```

**`git reflog` Output:**
```bash
abc1234 HEAD@{0}: checkout: moving from feature to main
def5678 HEAD@{1}: commit: Fixed bug in API
```

**Summary:**
- Use **`git show-ref`** to see where refs (branches/tags) currently point.
- Use **`git reflog`** to view the history of changes to refs for recovery or debugging. 

### How to use tags to track different versions of code
- use annotated tags to mark important milestones like releases.
- store extra metadata like the author, date and message.
[manage different versions of your code with branching and tagging](https://www.linkedin.com/advice/3/how-can-you-manage-different-versions-your-code-branching)


## Git blame
- shows line-by-line annotations of a file, identifying the commit and author responsible for each line of code.

```shell
git blame <file>;

# Displays blame annotations based on the file state in a specific commit.
git blame <commit hash> -- <file>;
git blame --date=short <file>;
git blame -C <file>; # Tracks code change even if the fiel was renamed.
```

### Stash
```shell
git stash show -p stash@{<index>}
```

### Cross Repository migration

```txt
fatal: refusing to merge unrelated histories
```
- this happen when your local repository and the remote repository have no shared commit history. - often occurs when a new repository is created locally and then connected to an existing remote repository.
##### Solution 
- Allow merging unrelated histories.
- use this command to `rebase` unrelated changes if the initial commit history mismatch
```shell
git pull origin main --allow-unrelated-histories
```
- this forces git to merge the different commit histories.
##### Rest local repository with remote repository
```shell
git fetch origin
git reset --hard origin/main
```
> [!WARNING]
> if you want to discard local changes and fully replace them with the remote repository

### Tracking file changes
```shell
git ls-tree -r HEAD --name-only; # view last commit tracked files
```

| Command                               | Purpose                                   |
| ------------------------------------- | ----------------------------------------- |
| `git ls-files`                        | Lists all tracked files                   |
| `git status --short`                  | Shows tracked/untracked files with status |
| `git ls-tree -r HEAD --name-only`     | Lists tracked files in the last commit    |
| `git ls-tree -r <commit> --name-only` | Lists tracked files in a specific commit  |
| `git ls-tree -r <branch> --name-only` | Lists tracked files in a branch           |
## Git find command
```shell
git ls-files --deleted;
git diff --cached --name-only --diff-filter=D;
git log --diff-filter=D --summary;
```

### Git diff check
```bash
git diff --diff-filter=D <to compare branch name>;
man git diff; # view diff manual
```
