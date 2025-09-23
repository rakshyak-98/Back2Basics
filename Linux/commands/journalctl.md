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