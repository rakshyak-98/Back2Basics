```sh
journalctl -u <service name>; # view basic logs for a service
journalctl -u <service name> -f; # real-time (like tail -f)
journalctl -u <service name> -b; # show logs since the last boot.
journalctl -u <service name> --since "1 hour ago";
journalctl -u <service name> -p err..crit; # show only error and critical message
journalctl -u <service name> -o json; # show logs with JSON output
```