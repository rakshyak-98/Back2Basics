> [!INFO]
> `ssh-agent` is a background program that holds your decrypted private SSH keys in memory so you don't have to type your passphrase (or password) every single time you `git push` `ssh` `scp` etc.

- acts as a key manager for [[SSH]] authentication.
- stores private keys in memory
- provide a form of [[single-sign-on (SSO)]] experience, where you can connect to multiple servers using the same authentication session

### Key features

- **Key Storage**: It holds private keys and their associated passphrases, enabling seamless authentication without manual entry each time
- **Background Process**: Typically runs in the background, initiated when you first use SSH after logging into your system [ssh-agent](https://smallstep.com/blog/ssh-agent-explained/)
- **Security**: Private keys are stored unencrypted in memory but are not written to disk, reducing the risk of exposure

### How to use ssh-agent

```bash
eval "$(ssh-agent -s)"
```
- this command initializes the agent and sets necessary environment variables like `SSH_AUTH_SOCK`, which points to the socket used of communication with the agent.

```bash
ssh-add <path to priavte key>; 
```

### Agent forwarding

- allows you to use your local ssh-agent on remote servers. When enabled, it lets you authenticate to further remote servers without needing to store your private key on those machines.
- this is useful when accessing services like Git repositories from bastion host or intermediate server.

```bash
ssh -A user@remote-server;
```
- this command allows the remote server to communicate back with your local ssh-agent simplifies and secures your workflow by managing SSH keys effectively, reducing repetitive tasks while maintaining strong security practices.

### Automatically start ssh-agent on system boot

`~/.config/systemd/$USER/`

```
[Unit]
Description=SSH key agent

[Service]
Type=simple
Environment=SSH_AUTH_SOCK=%t/ssh-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a $SSH_AUTH_SOCK
ExecStartPost=/usr/bin/ssh-add ~/.ssh/id_rsa
ExecStop=kill -15 $MAINPID

[Install]
WantedBy=default.target
```

```bash
systemctl --user enable ssh-agent.service
```

### How does ssh-agent know which key to use with which server

when you run `ssh git@github.com` or `git push` and you have 5 keys loaded in `ssh-agent`, OpenSSH tries them in this exact priority order until one works.

|Priority|Where it looks|What it tries|Usually decides here?|
|---|---|---|---|
|1|`-i /path/to/specific_key` command-line flag|If you explicitly said `ssh -i ~/.ssh/work_key git@…` → uses that exact key|Rarely|
|2|`IdentityFile` inside `~/.ssh/config`|Per-host (or wildcard) configuration|Very common|
|3|`IdentitiesOnly yes` + `IdentityFile` in config|Forces only the keys you listed in the config block||
|4|`AddKeysToAgent` + files in `~/.ssh/`|Tries keys in this order: `id_ed25519`, `id_rsa`, `id_ecdsa`, `id_dsa`, etc. (alphabetical)|Most people land here|
|5|Keys that are already loaded in `ssh-agent`|Offers them one by one to the server until the server says “yes, this public key is allowed”|Final fallback|

#### Tell git which key to use permanently

```bash
# For a specific repo
git remote set-url origin git@github.com:username/repo.git
# Then create a Host alias in ~/.ssh/config as above

# Or use SSH URL with alias
git remote set-url origin git@github-personal:username/repo.git
# and define "github-personal" in ~/.ssh/config with the right IdentityFile
```
