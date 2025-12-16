
## Run NodeJS with different user

```bash
sudo -u myuser node /path/to/app.js; # switch user
```

> [!NOTE]
> If using tools like nvm (Node Version Manager), load the environment properly

```bash
sudo -u myuser -H bash -c 'cd /path/to/app && source ~/.nvm/nvm.sh && node app.js'
```

> [!WARNING]
> Running node with system user can cause permission error, or command not found errors.
> also gives error for the environment variables.