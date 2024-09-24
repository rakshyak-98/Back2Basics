```bash
git reflog; # view git logs (not commit)
git push origin --tags; # push local tag to remote
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
### How to use tags to track different versions of code
- use annotated tags to mark important milestones like releases.
- store extra metadata like the author, date and message.
[manage different versions of your code with branching and tagging](https://www.linkedin.com/advice/3/how-can-you-manage-different-versions-your-code-branching)

## Worktree
- allow you to have multiple working trees associated with a single Git repository.
### Create Separate working trees
- create work-tree for each branch or commit you're working on.
- this keeps your changes isolated and makes it easy to switch between different parts of your project.
- fast branch switching, git only need to update the index of the working directory. No need to wait for a full clone or checkout.
### Shared Object Database
- each git work-tree shares the same object database, so you don't waste disk space with duplicate repository.
- the `.git` file in each work-tree points to the shared configurations.
- you can `rebase`, `merge`, `push`  changes independently for each work-tree.

```bash
git worktree add <destination> <branch ref>; # branch ref can be local or remote
```