- Identifies NAT type (e.g., Full Cone, Symmetric).
- maps the public port to the private port on a device.

When a client (e.g., a WebRTC application or VoIP client) communicates with a STUN server, the primary goal is to discover its public IP address and port. Once this information is obtained, the client uses it to establish direct peer-to-peer (P2P) connections by sharing the public facing details with other peers.

### Why this is Important?
Without STUN, the devices would have no way to knowing how to reach each other directly because NAT/firewalls hid private IP addresses.
Sharing public-facing IP and port information via STUN is critical step in bypassing NAT and ensuring peer-to-peer connectivity.
### How  it works?
#### Client discovers public details:
- The client sends request to a STUN server.
- The STUN server responds with the client's public IP and port as seen from outside the NAT.
- Example: If the client's private IP is `192.168.1.10:4000`, the public IP and port might be `203.0.113.5:6000`.
#### Sharing public details:
- The client shares this public IP and port with other peers during a signaling process (e.g., using [[SDP]] via protocols like [[SIP]] or [[WebRTC signaling channels]])
- the signaling process doesn't involve STUN but relies on a separate signaling server to exchange connection metadata between peers.
#### Peers Establish a direct connection:
- The receiving peer attempts to establish a connection to the provided public IP and port.
- If both peers use STUN, They each discover their public-facing details and attempt to reach each other directly.
- Example: Peer A sends packets to Peer B's public IP/port, and Peer B does the same for Peer A.
#### Testing and NAT hole punching
- During connection attempts, both peers send packets to each other simultaneously to punch a hole in their respective NATs, allowing direct traffic flow.
- If successful, data packets bypass the signaling server, resulting in faster and more efficient communication.