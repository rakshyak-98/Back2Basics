```bash
sudo chown root:root /etc/<service>/env;
sudo chmod 600 /etc/<service>/env; # only root readable.
```

```text
EnvironmentFile=/etc/my-node-app/env # You can still add/override individual vars Environment= OVERRIDE_VAR=something-else
```

- You can have multiple `EnvironemntFile=` lines if needed (they are read in order, later ones override earlier).

```text
EnvironmentFile=/etc/my-node-app/common.env
EnvironmentFile=/etc/my-node-app/sercrets.env
```

```bash
sudo systemctl daemon-reload;
sudo systemctl restart my-node-app;
```

### Unit file

```text
[Unit]
Description=My Node.js Application
After=network.target

[Service]
User=nodeuser
Group=nodeuser
WorkingDirectory=/path/to/your/app-directory
ExecStart=/usr/bin/node /path/to/your/app.js

# ← Add your env vars here
Environment= NODE_ENV=production
Environment= PORT=3000
Environment= DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
Environment= API_KEY=sk_live_abc123xyz
Environment= LOG_LEVEL=debug
Environment= ANOTHER_VAR=value with spaces is ok

Restart=always

[Install]
WantedBy=multi-user.target
```

### Service file Anatomy

- **Unit** section metadata and dependencies
- **Service** runtime behavior configuration
- **Install** boot time integration

```toml
[Unit]
Description=My Awesome Service
Documentation=https://example.com/docs
After=network.target
Requires=postgresql.service
Wants=redis.service

[Service]
Type=simple
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/myservice --config /etc/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
TimeoutStartSec=30s
Environment="NODE_ENV=production" "PORT+3000" "DEBUG=false"
Environemnt=/etc/myapp/env

CPUQuota=50%
MemoryLimit=512M
LimitNPROC=100 # limit number of processes/threads

# set disk IO priority
IOSchedulingClass=best-effort
IOSchedulinPriority=5
Nice=10

[Install]
WantedBy=multi-user.target
```

- `Description` -> human readable service description.
- `Documentation` -> URLs on man pages with service documentation.
- `After` -> defines start order (but doesn't create a dependency).
- `Requires` -> hard dependency - if this fails, the service won't start.
- `Wants` -> soft dependency - service will start even if this fails.

#### Service section

- `Type` -> how `systemd` determines if service started successfully.
	- `simple` -> default -> main process is the service.
	- `forking` -> service forks, parents exits.
	- `oneshot` -> service exists after completing task.
	- `notify` -> service signals when ready.
	- `dbus` -> service registers on D-Bus.
- `User/Group` -> run service as this `User/group` instead of root.
- `WorkingDirectory` -> working directory for the service.
- `ExecStart` -> Command to start the service.
- `ExecReload` -> Command to reload configuration.
- `Restart` -> When to restart the service automatically.
	- Options: `no` `on-success` `on-failure` `on-abnormal` `on-watchdog` `on-abort` `always`
- `RestartSec` -> how long to wait before restarting.
- `Environment` -> Environment variables for the service.

### Install section 

- `WantedBy` -> which target wants this service.
	- `multi-user.target` -> normal multi-user system.
	- `graphical.target` -> graphical interface.
	- `network-online.target` -> when network is fully up.
