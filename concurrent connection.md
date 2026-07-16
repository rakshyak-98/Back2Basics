[[context switching]] [[Networking]]

In the context of media streaming and infrastructure architecture, a concurrent connection is as active, sustained session between a client (or source) and a server where data is being actively transmitted or maintained in a state-ready condition.

### Network Concurrency

This is the total number of TCP/UDP sockets open to your server. In a 300-channel scenario, if you are receiving 300 unique streams, your server must manage 300 distinct socket file descriptors. This consumes kernel memory and require efficient handling of the `epoll` or `kqueue` event loops to prevent context-switching bottlenecks.

Encoding/Decoding concurrency (Process-level) -> This is the number of active NVENC/NVDEC hardware session, Even if 300 network connections are open, the limiting factor is how many simultaneous media pipeline the GPU hardware can handle before the fixed-function circuitry saturates.