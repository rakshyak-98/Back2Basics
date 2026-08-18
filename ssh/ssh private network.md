[[ssh]]

# ssh private network

> ssh private network — ip addr show | grep inet

## Mental model

**Say it in one breath:** ssh private network — ip addr show | grep inet

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

## Standard config / commands

```bash
ip route
ssh -J bastion.internal user@10.0.5.20
# ~/.ssh/config ProxyJump bastion.internal
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Timeout to private IP | No route; VPN down | Connect VPN; verify route to RFC1918 range |
| Bastion works; inner host fails | Security group; inner sshd | Open port 22 on inner SG; check inner sshd |
| Wrong source IP seen on inner host | Jump not used | Use `ProxyJump` or `-J` |
| MTU black hole | VPN plus small MTU | Lower interface MTU on client |

## Gotchas

> [!WARNING]
> Private IPs are **not routable on the public internet** — you need VPN or a jump host.

## When NOT to use

- Do not expose private RFC1918 addresses directly to the internet with port forwarding.

## Related

[[ssh]]
