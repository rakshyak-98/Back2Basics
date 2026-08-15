[[ssh login]] [[sshd config]] [[SOCKS (Socket Secure)]] [[non-Routable address]]

# ssh private network

> Reach SSH on private (RFC1918) hosts via VPN or a jump host — and firewall port 22 so only trusted private source ranges can connect.

## Interview Relevance

Interviewers check that you know private IPs are not internet-routable, and that bastion/`ProxyJump` plus tight `ufw`/SG rules are the usual pattern.

## Sources

- [RFC 1918 — Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918) — overview
- [OpenSSH — ProxyJump](https://man.openbsd.org/ssh_config.5#ProxyJump) — deep-dive
- [UFW community docs](https://help.ubuntu.com/community/UFW) — overview

## Key Concepts

- **Non-routable addresses:** `10/8`, `172.16/12`, `192.168/8` need VPN or jump — not public routes ([[non-Routable address]]).
- **Least exposure:** delete wide-open `allow 22` rules; allow from private CIDR only.
- **ProxyJump:** one public bastion; inner hosts stay private.
- **Source IP reality:** NAT egress can break `from=` / firewall expectations.

## Technical Details

```bash
ip addr show | grep inet
ip route
```

Remove wide-open SSH rules, then allow from the private network:

```bash
sudo ufw delete allow 22
sudo ufw delete allow ssh
sudo ufw delete allow OpenSSH

sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp
sudo ufw allow from 192.168.1.0/24 to any port ssh
sudo ufw reload
sudo ufw status numbered
```

```bash
ssh -J bastion.internal user@10.0.5.20
# ~/.ssh/config
# Host internal
#   ProxyJump bastion.internal
#   HostName 10.0.5.20
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Timeout to private IP | No route; VPN down | Connect VPN; verify route to RFC1918 range |
| Bastion works; inner host fails | Security group; inner sshd | Open port 22 on inner SG; check inner sshd |
| Wrong source IP seen on inner host | Jump not used | Use `ProxyJump` or `-J` |
| MTU black hole | VPN plus small MTU | Lower interface MTU on client |

## Real-World Applications

VPC admin access, lab networks locked to `192.168.1.0/24`, and zero-public-SSH fleets behind a bastion.

**Example:** Laptop VPN gets `10.0.0.0/8` routes; `ufw` allows SSH only from that range; operators never open 22 to `0.0.0.0/0`.

## Pros/Cons or Trade-offs

- **Pro:** Shrinks attack surface versus public SSH.
- **Con:** Depends on VPN/bastion availability — plan break-glass console access.
- **Con:** Incorrect `ufw` proto/port syntax fails closed or open — verify with `status numbered`.

## Comparison

- vs public SSH + keys only: private network + jump is defense in depth; keys alone are not enough.
- vs [[SOCKS (Socket Secure)]] `-D`: SOCKS tunnels app traffic; ProxyJump is for SSH itself (can combine).

## Mistakes to Avoid

- Exposing RFC1918 addresses to the internet with port forwarding.
- `ufw allow ... proto http` typos when you meant `tcp`.
- Assuming the bastion’s client IP is what the inner host sees without understanding jump behavior.
- Deleting all SSH rules before confirming alternate access.
