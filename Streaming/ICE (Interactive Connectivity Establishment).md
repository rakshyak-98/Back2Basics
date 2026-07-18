ICE (Interactive Connectivity Establishment) server configuration is a method used in WebRTC and other real-time communication protocols 
- to help peers (devices, or applications) establish a direct connection with each other, even if they are behind firewalls or [[NAT (Network Address Translation)]] .
- ICE servers facilitate the process of discovering the best path of communication between peers.

#### STUN (Session Traversal Utilities for NAT)
- A server used to discover the public IP address and port of a client behind a NAT or firewall.
- Candidate Gathering ICE uses STUN and [[TURN server (Traversal Using Relays around NAT)]] to gather candidates (potential connection paths) for peer-to-peer communication.
- Prioritization ICE servers prioritize the best candidates based on their network conditions, like latency or availability.

> [!INFO] When a WebRTC client tries to connect to another client, it will contact a STUN server to get its public IP address.
- if direct communication isn't possible (e.g., due to restrictive firewalls), the client will fall back on a [[TURN server (Traversal Using Relays around NAT)]] server to relay the communication.

### Signaling
- Signaling is needed in order for two peers to share how they should connect.
- usually this is solved through a regular HTTP-based Web API (REST service, or other RPC mechanism), where web applications can relay the necessary information before the peer connection is initiated.

> [!INFO] Signaling is needed in order for two peers to share how they should connect. Usually this is solved through regular HTTP-based Web API.
- Where web applications can relay the necessary information before the peer connection is initiated.

```js
const signalingChannel = new SignalingChannel()
```