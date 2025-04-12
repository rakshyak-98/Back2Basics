> [!INFO] linux Service Manager
> - `systemctl` is the control center for [[systemd]] and service manager that's become standard in most Linux distributions.

```sh
# analyze and debug system manager
systemd-analyze; # check how long your system took to boost.
```
- services start sequentially, causing slow boot times. With `systemctl` services can start in parallel when possible


```sh
systemctl status <service name>; # service state and stats
```
- current state
- process ID
- resource usage
- the control group hierarchy