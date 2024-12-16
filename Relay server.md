A relay server is a server that forwards data between two or more devices or systems that cannot communicate directly.

Both devices (Device A and Device B) first establish a connection to the relay server.
- This connection is possible because the devices initiate outgoing connections, which are generally allowed by most NAT's and firewalls (outgoing traffic is usually not blocked).
Once both devices have connected to the relay server, the server creates communication channels (virtual pipes) for each device. These channels serve as endpoints to send and receive data between the devices via the relay server.

### Why Relay servers work?
- NAT and Firewalls typically block incoming traffic to devices. So, both devices can open a connection to the relay server, but the server acts as the intermediary to relay data.
- This solves the problem of devices that cannot directly connect because of [[Symmetric NAT]], firewalls blocking incoming traffic, or other restrictive network setups.

### What Happens If a Firewall Imposes Rules on Outgoing Traffic?

If a firewall enforces **outgoing traffic rules**, it can prevent devices behind the firewall from establishing connections to external servers, including relay servers. This creates a significant challenge for communication protocols like TURN (which requires outgoing traffic to establish connections). Here's how this situation impacts the communication and what can be done to resolve it:

---

### Key Points:

1. **Firewall Blocking Outgoing Traffic**:
   
   - A **firewall** that blocks outgoing traffic would prevent the device from reaching any external server, including the relay server (e.g., TURN or STUN).
   - This effectively stops the device from initiating the connection needed to set up a communication channel via a relay server.
2. **Impact on NAT Traversal**:
   
   - **STUN** and **TURN** protocols rely on the device initiating outbound connections (because outgoing connections are typically allowed).
   - With outgoing traffic blocked, **NAT traversal** cannot occur, meaning the devices won’t be able to discover their public IPs or connect to peers through the relay server.
3. **Resulting Connectivity Issues**:
   
   - Devices that rely on **peer-to-peer** communication (e.g., WebRTC, VoIP) would be unable to function properly.
   - Even if a **TURN server** is available, the firewall would prevent the device from sending its data to the server for relaying.

---

### Potential Solutions:

1. **Using a Proxy Server**:
   
   - A proxy server can help by forwarding traffic between the client and the external server.
   - **HTTP/HTTPS Proxy**: In environments where **HTTP or HTTPS traffic** is allowed, a proxy server can be used to tunnel the communication to a TURN server.
   
   **How It Works**:
  
   - The device sends outgoing traffic to the proxy server.
   - The proxy server forwards the traffic to the relay server (TURN or STUN), allowing the NAT traversal to happen.
 
 > [!INFO] For bypassing firewall restriction and enabling communication with a TURN server, the relevant proxy is typically a forward proxy.

> [!NOTE] Not typically used for NAT traversal: Reverse proxies are less relevant in the context of bypassing firewall restrictions for TURN/STUN because the goal is for the client to access external resources, not the other way around.

2. **TURN with WebSocket or HTTP**:
   
   - Some **TURN servers** and protocols support using **WebSockets** or **HTTP/HTTPS** for communication.
   - WebSocket or HTTP connections are more likely to be allowed by firewalls since these protocols often bypass stricter rules on outgoing traffic.
   
   **How It Works**:
   
   - The TURN server uses **WebSocket** or **HTTP** as a transport layer, which is more likely to pass through firewalls that allow web traffic.
   - This allows the device behind the firewall to reach the TURN server and initiate the connection despite outgoing traffic restrictions.
3. **Network Configuration Adjustments**:
   
   - In some cases, it may be possible to reconfigure the firewall rules to allow specific outgoing connections to known **TURN servers** or **STUN servers**.
   - This requires cooperation with network administrators to whitelist certain ports and IP addresses for peer-to-peer communication.
4. **VPN (Virtual Private Network)**:
   
   - If the firewall is blocking outgoing traffic to relay servers, using a **VPN** can tunnel traffic out of the local network.
   - The device can connect to the VPN, which effectively bypasses the firewall rules and establishes communication with external servers.

---

### Advantages of These Solutions:

- **Proxy Servers**: Allow the device to access external services (like TURN) even when outgoing traffic is restricted.
- **WebSocket/HTTP TURN**: Increases the chances of traffic being allowed through the firewall by using protocols that are more commonly permitted.
- **VPN**: Bypasses firewall restrictions by tunneling traffic through a secure connection.

### Disadvantages:

- **Proxy Servers**: Requires setting up and maintaining a proxy server, which may not always be feasible.
- **WebSocket/HTTP TURN**: May not be supported by all TURN servers or may introduce additional complexity.
- **VPN**: Adds overhead, and devices may need additional configuration. Also, a VPN connection might not always be practical in certain environments.

---

### Conclusion:

When firewalls block outgoing traffic, using a **proxy server**, **WebSocket/HTTP-based TURN** servers, or **VPNs** can help bypass these restrictions and allow devices to establish connections. However, each solution has its own trade-offs, such as added complexity or potential performance issues.
