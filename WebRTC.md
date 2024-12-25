[webrtc.googlesource](https://webrtc.googlesource.com/src)
real-time communication for the web
- it support video, voice and generic data to be sent between peers.
- the technologies behind WebRTC are implemented as an open web standard and available as regular JavaScript APIs in all major browsers.
- there are many different use-cases WebRTC, from basic web apps that uses the camera or microphone, to more advanced video-calling applications and screen sharing.

## Design

> [!INFO] Major components of WebRTC include several JavaScript API
- `getUserMedia` acquires the audio and video media (by accessing device's camera and microphone)
- `RTCPeerConnection` enables audio and video communication between peers. The data is transported using [[SCTP (Stream Control Transmission Protocol)]] over [[DTLS]] . It uses the same API as `WebSockets`
- `getStats` allows the web application to retrieve a set of statistics

### Peer connection
- connecting two applications on different computers to communicate using a peer-to-peer protocol.
- the communication between peer can be video, audio or arbitary binary data (for client supporting the `RTCDataChannel` API).
- In order to discover how two peers can connect, both clients need to provide an [[ICE (Interactive Connectivity Establishment)]]. 

## Example
### WebRTC Video call workflow
##### STUN phase:
- Browser A (behind NAT) queries a STUN server and discovers its public IP as `203.0.113.5:6000`.
- Browser B does the same and gets `203.0.113.10:7000`.
##### Signaling phase:
- Browser A shares its public IP `203.0.113.5:6000` with Browser B through a signaling server.
- Browser B share its public IP `203.0.113.10:7000` with Browser A.
##### Direct Connection:
- Browser A sends connection request to Browser B's public IP and port.
- Browser B does the same, and a direct communication channel is established.