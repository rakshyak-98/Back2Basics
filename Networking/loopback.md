loopback resolution refers to the process where a domain name resolves to a loopback IP address (`127.0.0.1`) for IPV4 or `::1` for IPV6.
- this directs network traffic back to the same machine rather than sending it over the network.

> [!WARNING] if a malicious domain resolves to `127.0.0.1` it could trick applications into interacting with unintended local services.

> [!INFO] Firewalls can block or warn about loopback-based redirection from external sources.