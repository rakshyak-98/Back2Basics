## firewall

```bash
ufw status; # check firewall status.
ufw status verbose; # more detailed output.
ufw status numbered; # usefull when deleting rules.

ufw logging on; # turn logging on (low/medium/high/full) 

ufw app list;
ufw app info <profile name>;

ufw allow 3000/tcp comment 'Node.js / React dev server';
ufw allow from 192.168.1.0/24 to any port 3000 proto tcp comment 'LAN only';

ufw reset;
```

```bash
sudo ufw deny out to <ip> port <port> proto <protocol>;
sudo ufw deny in to <ip> port <port> proto <protocol>;
```

```bash
sudo ufw delete allow 3000/tcp
sudo ufw delete allow 80,443/tcp comment 'Web server'
sudo ufw delete allow 'Nginx Full'
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

```bash
sudo ufw allow in 80/tcp
sudo ufw allow out 80/tcp
```

```bash
sudo ufw allow out to 127.0.0.1 to any port 5432 proto tcp
```

"UFW mainly works with **IP protocols**, and the most commonly used ones are TCP and UDP."

> Check protocols known to Your Linux system, `ufw` relies on Linux networking/netfilter, so you can see the system's protocol names `/etc/protocols`.
