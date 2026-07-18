Linked-Local Multicast Name Resolution
is a protocol used for local network name resolution when DNS is unavailable. 

### How it works
- devices broadcast queries on the local network.
- other devices respond if they recognize the name.
- used for resolving hostnames without a DNS server.

### Why it's disabled `-LLMNR` in your system?
- security risk: Vulnerable to spoofing attacks.
- Unnecessary: if you have a working DNS server.
- Performance: reduces network traffic.

### Why docker networks are not resolving DNS?
by default, Docker container use the host's DNS settings unless overridden.

if containers can't resolve domain names, possible reasons are:
- Docker daemon not configured for DNS
- Custom docker network without a DNS server.
- Host's `/etc/resolv.conf` is misconfigured.
- Firewall blocking external DNS requests.