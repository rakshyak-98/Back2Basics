
# Test mail server

```bash
telnet <mail.server> <port> # (STARTTLS)
openssl s_client -connect smtp.yourserver.com:465 -quiet # (SSL/TLS)
```

```bash
nc -zv <mail.server> <port> # port reachable / port is open
```

### scan open port of host

```bash
ss -lntup # all listening ports (TCP+UDP) + process name + PID
```

```bash
sudo nmap -p- localhost
```