## firewall

```bash
ufw status; # check firewall status.
ufw show; # show firewall current configurations rules.
ufw logging; # show current logging level.
ufw app list;
ufw allow 3000/tcp;
ufw reset;
ufw delete allow;
```

## UFW application profile

ufw scans files in directories

```bash
/etc/ufw/application.d/
/usr/share/ufw/application.d/ # (build-in profiles from packages)
```
- Each file defines one or more application profiles

```bash
sudo ufw app list;
ufw app info "OpenSSH"; # get detailed info about a specific application profile
```

### Allow traffic using an application profile

```bash
ufw allow "Apache FUll"
ufw allow OpenSSH 
ufw allow "Nginx HTTPS"
```

```bash
ufw deny "Apache"
ufw delete allow "Nginx HTTP"
```