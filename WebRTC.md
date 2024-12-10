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