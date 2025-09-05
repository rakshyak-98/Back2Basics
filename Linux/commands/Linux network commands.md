```bash
netstat -tuln; # to show all active TCP & UDP Connections (with servers);
ss -tuln
lsof -i -P -n | grep LISTEN
```

```bash
nc -zv <domain name> <port>; # check if the server is reachable on port 443;
```

## Socket Statistics
- list all ports and their protocols
## List open files
- list all open files related to network ports, showing which services are using which ports

### `netstat` 
```txt
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 ubuntu-Latitude-5:40422 20.189.173.8:https      ESTABLISHED
tcp        0      0 ubuntu-Latitude-5:45274 140.227.186.35.bc:https ESTABLISHED
tcp        0      0 ubuntu-Latitude-5:40404 93.243.107.34.bc.:https ESTABLISHED
tcp        0      0 ubuntu-Latitude-5:56124 lb-140-82-113-26-:https ESTABLISHED
tcp        0      0 ubuntu-Latitude-5:45068 13.67.9.5:https         ESTABLISHED
tcp6       0      0 ubuntu-Latitude-5:53746 2620:1ec:bdf::58:https  ESTABLISHED
tcp6       0      0 ubuntu-Latitude-5:45970 2606:4700:8392:7c:https ESTABLISHED
tcp6       0      0 ubuntu-Latitude-5:39062 2606:4700:8392:7c:https ESTABLISHED
```
- showing active TCP connections without servers (listening sockets excluded).

`Proto` -> Protocol (TCP/TCP6)
`Recv-Q ` -> Received queue (data waiting to be processed)
`Send-Q` -> Sent queue (data waiting to be acknowledged)
`Local Address` -> Your system's IP + port
`Foreign Address` -> Remote system's IP + port
`State` -> connection state

`-a` -> show all sockets (listening and non-listening)
`-t` -> show TCP
`-u` -> show UDP
`-l` -> show listening ports (servers)
`-n` -> show numeric address (skip DNS resolution)
`-p` -> show process name/PID

## `tcpdump`

```shell
tcpdump -i any port 80 or port 443;
```
- capture HTTP(S) traffic, including WebSockets.
- look for `Upgrade: WebSocket` in HTTP headers.

### `iptables`

```shell
iptables -L # Displays the current firewall ruleset.
iptables -F # Flushes (deletes) all firewall rules.
iptables -A # Appends a new rule to the end of the firewall ruleset.
iptables -I # Inserts a new rule at a specific position in the firewall ruleset.
iptables -D # Deletes a specific rule from the firewall ruleset.
iptables -P # Sets the default policy for a chain (ACCEPT, DROP, or REJECT).
iptables -N # Creates a new user-defined chain.
iptables -E # Renames a user-defined chain.
iptables -Z # Resets the packet and byte counters for a chain.
iptables-save # Saves the current firewall ruleset to a file.
iptables-restore # Restores a saved firewall ruleset from a file.
```

## `nc`

```shell
nc google.com 80; # Connect to google.com on port 80
```

```shell
nc -l -p 1234; # listen on port 1234

nc -l -p <port> > incomming.txt; # Receiver
nc <host ip> <port> < file.txt; # Sender
```

```shell
nc -z -v host_ip 20-100  # Scan ports 20 to 100
```

```shell
nc -l -p <port> -e /bin/bash; # bind shell
```

## nslookup

```bash
nslookup <domain.name>; # omit schema, port, and path
```

## DNS settings
```shell
system-resolve --status;
```

```yaml
Global
	Protocols: -LLMR -mDNS -DNSOverTLS DNSSEC=no/unsupported
	resolv.conf mode: stub
```

- [[LLMNR]] and [[mDNS]] Disabled -> local name resolution (for finding devices on the network) is off.