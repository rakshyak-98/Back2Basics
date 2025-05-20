```bash
gh auth login;
gh api user; # account informations
```

```bash
gh secret set <secret name>;
gh secret set --env <environment name> <secret name>;
gh secret list --env <environment name>
```

```bash
gh label create <label name> --description <description>;
gh issue edit <issue id> --add-label <label name>;
gh pr create --base <base_branch> --head <head_branch> --title <title> --body <body>:
gh pr view;
```

``` bash
gh repo delete owner/repo-name;
gh repo delete owner/repo-name --confirm;
gh repo delete --confirm; # delete current repo
```
- required sudo permission

```bash
gh repo view Raksyak-MST/backend --json sshUrl
```