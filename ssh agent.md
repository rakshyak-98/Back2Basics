- acts as a key manager for [[SSH]] authenticatoin.
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