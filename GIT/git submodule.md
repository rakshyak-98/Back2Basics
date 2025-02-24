- adding git repository inside another git repository

```shell
git clone --recurse-submodules <repository url>;
```

- if you already cloned the repository without `--recursive-submodule`
```shell
git submodule update --init --recursive; # fetches the submodules and checks the referenced commits.
git submodule update --remote --merge; # update all submodules at once
git submodule status; # check submodule status
```

- remove the sub-module reference and cleans up related git files.
```shell
git submodule deinit -f -- <path>; # remove submodule
git rm -f <path>;
rm -rf .git/modules/<path>;

```
### Convert git repo to sub module
```shell
git submodule add <repository-url> <repo name>;
```