```bash
gh auth login;
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