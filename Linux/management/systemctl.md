> [!INFO] linux Service Manager
> - `systemctl` is the control center for [[systemd]] and service manager that's become standard in most Linux distributions.

```sh
systemctl --failed; # show all failed services.
systemctl reset-failed; # attemt to restart all failed service.
systemctl is-system-running; # system is fully booted and operational
```

```sh
systemctl list-units --type=service;
systemctl list-units --type=service --all;

systemctl list-units --type=service --state=running;
```

```sh
systemctl list-units --type=target;
systemctl list-units --type=socket;
```

```sh
# analyze and debug system manager
systemd-analyze; # check how long your system took to boost.
systemd-analyze blame; # see which service took time to start.
systemd-analyze critical-chain; # critical chain of services that delayed boot.

systemctl list-dependencies <service name>;
systemctl list-dependencies --reverse <service name>;
```
- services start sequentially, causing slow boot times. With `systemctl` services can start in parallel when possible


```sh
systemctl status <service name>; # service state and stats
```
- current state
- process ID
- resource usage
- the control group hierarchy

```sh
systemctl is-active <servie name>;
systemctl is-enable <service name>; 
```

```sh
systemctl start <service name>;
systemctl stop <service name>;
systemctl restart <service name>;
systemctl reload <service name>;
systemctl reload-or-restart <service name>;
```

```sh
sudo systemctl daemon-reload; # reload systemd to recognize the new services.
```

> [!INFO] Systemd defines services
> - they're defined in *unit files* that tell `systemctl` how to manage them.

System Service files live in these directories.
`etc/systemd/system/` -> custom or modified service files.
`/run/systemd/system/` -> runtime service files.
`/usr/lib/systemd/system/` -> package provided service files.

> [!INFO] when you run a `systemctl` command, it looks for the service file in this order.

```sh
systemctl show -p FragmentPath ssh.service; # find where ssh service file is located
```

```sh
systemctl mkdir -p /etc/systemd/system/ssh.service.d/
systemctl mkdir -p /etc/systemd/system/ssh.service.d/override.conf

# [ Apply the changes ]
sudo systemctl daemon-reload
sudo systemctl restart ssh
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


### Unit file manipulation
```sh
systemctl cat <service name>;
systemctl edit --full <service name>;
```

```sh
systemctl get-default; # view current target
systemctl set-default graphical.target; # change default target
systemctl isolate multi-user.target; # this will kill the graphical environment
```