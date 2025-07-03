### Git permission denied error

> [!NOTE]
> - Local Directory Permissions -> if you attempt to clone into a directory where your user does not have write permissions (for example /var/www/html) git cannot create the working directory or files, resulting in a "Permission denied" error.

`drwxr-xr-x  2 root  root   4096 Jul  3 18:35 test/`
```bash
cd test;
gh repo clone Raksyak-MST/backend

fatal: could not create work tree dir 'backend': Permission denied
exit status 128
```

> [!NOTE]
> - Remote repository Access Rights -> if you do not have the required permissions to access the remote repository (such as trying to clone a private repository without being a collaborator or team member) Git will deny access.

> [!NOTE]
> - Mixing `sudo` and non-sudo commands -> using sudo with git command can cause permission mismatch, especially if your SSH keys are not available to the root user.