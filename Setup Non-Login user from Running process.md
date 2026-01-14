## Using pm2

```bash
sudo pm2 start /path/to/your/app.js --name myapp --user nodeuser;
sudo pm2 save;
sudo pm2 startup;
```

> [!NOTE] 
> - Need root or sudo access to perform these steps.

**Create new user (with Login Disable)**
- system-like user (e.g, named `nodeuser`) -> prevents SSH/shell access while still allowing the user to run processes.
- Create user **without home directory**
- Set the shell to `/usr/sbin/nologin` or `/bin/false`

```bash
sudo useradd -r -s /usr/sbin/nologin nodeuser;
```
- `-r` create a system user (UID below 1000)

If you need a home directory for NodeJS files/logs

```bash
sudo useradd -m -r -s /usr/sbin/nologin nodeuser;
```

Verify the user

```bash
id nodeuser;
```

Test login prevention

```bash
su - nodeuser;
```

**Run node process as the user**

Run NodeJS with user (Temporary, for Testing)

```bash
sudo su -s /bin/bash - nodeuser -c "node /path/to/your/app.js"
```

- `su` -> `nodeuser`: Switches to the user.
- `-s` -> `/bin/bash`: Temporarily overrides the nologin shell to allow command execution (but still no interactive login).
- `-c` -> "node ...": Runs the command as the user.

## Persistent Run (using system service)

- create `systemd` service file to run the Node process as `nodeuser` automatically on boot.

```bash
sudo touch /etc/systemd/system/my-node-app.service;
```

```text
[Unit]
Description=My Node.js Application
After=network.target

[Service]
User=nodeuser
Group=nodeuser
WorkingDirectory=/path/to/your/app-directory
ExecStart=/usr/bin/node /path/to/your/app.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

## Grant Passwordless `sudo` for specific commands

find full path

```bash
which nginx;
which systemctl;
```

Edit sudoers safely with `visudo` 
- create file at `/etc/sudoers.d/<file>`;

```bash
nodeuser ALL=(ALL) NOPASSWD: /usr/sbin/nginx -t
nodeuser ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

- save and exit. Test as `nodeuser` (using `su`)

```bash
sudo su -s /bin/bash - nodeuser -c "sudo nginx -t"
```
- should run without password.


## Additional Security passwrod (optional)

```bash
sudo passwd -l nodeuser; # Locks any password (though none was set).
```

Permissions for Node app. Ensure file/directories are owned by `nodeuser`

```bash
sudo chown -R nodeuser:nodeuser /path/to/your/app-directory;
```

> [!INFO]
> Why this setup?: The user runs processes (like Node) but can't log in or escalate beyond the allowed commands. Ideal for automated scripts or services needing limited privileged actions (e.g., a Node app reloading Nginx).