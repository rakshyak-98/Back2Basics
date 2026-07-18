A non-routable address is an IP address that cannot be used for communication beyond its local network. These addresses are used for internal communication
- this addresses are used for internal communication within a system or network but cannot be reached from external network (e.g., the internet).

An IP address may be not reachable due to several reasons, categorized into network-level, host-level and firewall-level issues.

#### Network level issues

| Issue                    | Cause and solution                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| non-routable IP          | Using private/local IPs like `0.0.0.0`, `127.0.0.1` or `169.254.x.x` which cannot be accessed externally. Instead use a real private `192.169.x.x` or public IP. |
| Incorrect subnet         | The IP is on a different network and the subnet doesn't allow communication. Ensure both devices are in the same subnet.                                         |
| Gateway Misconfiguration | No valid route exists to reach the destination. Check `ip route` or `netstat -rn`                                                                                |
| DNS resolution Failure   | Hostname does not resolve to the correct IP. Use `nslookup` or `dig` to check resolution                                                                         |

### **Host-Level Issues**
These occur when the destination machine is **not accepting connections**.

| Issue                            | Cause & Solution                                                                                          |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Service Not Running**          | The target service (e.g., Kafka) is down. **Fix:** Start it with `systemctl start kafka` or check logs.   |
| **Listening on Wrong Interface** | The service is bound to `127.0.0.1` instead of `0.0.0.0` or a proper IP. **Fix:** Check `netstat -tulnp`. |
| **Port Not Open**                | No service is listening on the required port. **Fix:** Use `nc -zv <IP> <port>` to test.                  |
### **Firewall-Level Issues**
Firewalls or security rules may block access.

| Issue                        | Cause & Solution                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Local Firewall Blocking**  | `iptables` or `ufw` blocks the port. **Fix:** Run `ufw allow 9092/tcp`.                                |
| **Cloud Security Rules**     | If using AWS/GCP, security groups might block traffic. **Fix:** Allow inbound rules.                   |
| **Docker Network Isolation** | Containers have separate networks. **Fix:** Use `--network=host` or set up proper `bridge` networking. |
