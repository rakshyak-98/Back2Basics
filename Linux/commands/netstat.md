Used to inspect connections, listening ports, routing table, interface statistics, and protocol statistics.

```shell
sudo netstat -p; # Show pid of executable
```

```bash
# [Check all listing ports]
sudo netstat -luntp;
# - verify service is listening.
# - identify process occupying a port.


# [Find what process is using a specific port]
sudo netstat -tulnp | grep :8080
```

```bash
# [Check active connections]
netstat -ant

# - Client/server communication
# - Hanging connections

# States:
# 
# - ESTABLISHED → Normal communication
# - SYN_SENT → Waiting for server
# - SYN_RECV → Half-open connection
# - TIME_WAIT → Recently closed
# - CLOSE_WAIT → Remote closed, local not
# - FIN_WAIT1/2 → Closing
# - LISTEN → Waiting for clients

```

```bash
# [Protocol statistics]
netstat -s

# - TCP retransmissions
# - UDP errors
# - ICMP statistics
# - IP statistics

# Usefull for:
# - Package loss
# - Retransmissions
# - Network congestion

```

