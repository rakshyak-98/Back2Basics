```bash
git log --pretty=format:"%h - %an (%ar): %s";
git log --pretty=format:"%h %ad %s" --date=short;

git log --graph --oneline --decorate --all;

```

|Placeholder|Description|
|---|---|
|`%h`|Short commit hash|
|`%H`|Full commit hash|
|`%s`|Commit message|
|`%an`|Author name|
|`%ae`|Author email|
|`%ar`|Relative commit time|
|`%ad`|Author date|
|`%cn`|Committer name|
|`%ce`|Committer email|
|`%d`|Refs (branches/tags)|
