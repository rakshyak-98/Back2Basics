
```bash
ip addr show | grep inet
```

**Remove any wide-open ssh rule** 

```bash
sudo ufw delete allow 22;
sudo ufw delete allow ssh;
sudo ufw delete allow OpenSSH;
```

**Allow SSH only from your private network**

```bash
sudo ufw allow from 192.168.1.0/24 to any port 22 proto http
```

```bash
sudo ufw allow from 192.168.1.0/24 to any port ssh
sudo ufw allow from 192.168.1.0/24 port 22 proto tcp
```

**Reload `ufw`**

```bash
sudo ufw reload; # reload
sudo ufw status numbered; # verify the rule
```