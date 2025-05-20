```bash
# keeps only the most recent logs, retaining up to 500 megabytes of data
sudo journalctl --vacuum-size=500m; 

sudo journalctl --vacuum-time=1week;
sudo journalctl --vacuum-time=1s;
journalctl --disk-usage;
```

```bash
journalctl -u <local.service>; # view logs for perticular service.
```