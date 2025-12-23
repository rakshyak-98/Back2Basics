```bash
sudo journalctl --vacuum-time=1s -u <unit file>;

# keeps only the most recent logs, retaining up to 500 megabytes of data
sudo journalctl --vacuum-size=500m; 

sudo journalctl --vacuum-time=1week;
journalctl --disk-usage;
```

```bash
journalctl -u <local.service>; # view logs for perticular service.
```

### Filter by service

```bash
journalctl --since "2024-03-01" --until "2024-03-18"; # logs between
journalctl -u nginx.service; # show logs for a specific service
journalctl -u sshd.service --since "1 day ago";
```

```bash
journalctl -p err; # show logs of level error or higher 
```

### Filter by process user or group

```bash
journalctl _EXE=/usr/bin/nginx; # Show logs from a specific executable.
journalctl _SYSTEMD_CGROUP=/system.slice/ssh.service; # Show logs related to a cgroup.
```

### Filter by kernel logs

```bash
journalctl -k; # Show only kernel logs.
journalctl -k -p err; # show only kernel logs with error level or higher.
```

### Filter by boot

```bash
journalctl -b; # Show logs from the current boot
journalctl -b -1 # Show logs from the previous boot
journalctl --list-boots; # List available boots.
```

### Output control

```bash
journalctl --no-pager; # Show logs without pagination.nx

journalctl -o short; # Show compact logs.
journalctl -o verbose; # Show detailed log information.
```