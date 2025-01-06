```bash
git clean; # removes untracked files from working directory (not staged, committed, ignored)
git reflog; # view git logs (not commit)
git push origin --tags; # push local tag to remote
git branch --unset-upstream; # unset remote tracking branch
git remote -v;
git show-ref;
git branch -vv;
```
### Without merge how to validate two branch have merge conflict
```shell
git checkout <target-branch>;
git merge <source-branch> --no-commit --no-ff; # dry-run merge

git diff target-branch...source-branch;

git merge-tree $(git merge-base target-branch source-branch) target-branch source-branch;

```
#### Starter config
```bash
git config user.name <commit author name>;
git config user.email <commit author email>;
git config init.branch main; # main instead of master;
```
### Commands
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
git config --global --unset credential.helper; # clear Git Credential Cache
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