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