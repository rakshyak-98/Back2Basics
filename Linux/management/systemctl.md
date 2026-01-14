> [!INFO] linux Service Manager
> - `systemctl` is the control center for [[systemd]] and service manager that's become standard in most Linux distributions.

```bash
sudo systemctl edit <service file>;
sudo systemctl show <service file>;
```

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