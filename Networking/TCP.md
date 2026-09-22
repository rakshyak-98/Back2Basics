[[Byte stream]] [[SSH]] 

Connection-oriented, reliable transport-layer protocol used to deliver data between applications over an IP network. It sits above IP and provides applications with a reliable **byte stream** rather than individual packets.

[[TCP/TCP connection]]
[[TCP/TCP three-way handshake]] The three packets establish TCP connection. After that, TCP segments the application data, numbers the segments using **sequence numbers**, and uses **ACKs** to confirm successful reception.
[[TCP/Receive window]] TCP prevents a fast sender from overwhelming a slow receiver using the **receive window.**
[[TCP/TCP segment]]
[[Byte stream]]
[[TCP/TCP connection termination]]

**TCP adjusts its sending rate based on network congestion.**

> TCP uses port numbers to identify applications, such as HTTP on port 80 and HTTPS on port 443
**Application -> Port -> TCP connection -> IP -> Network**
TCP does not identify an application directly. TCP use **port numbers** to identify the endpoint/application process that should receive the data.

> Flow control protects the receiver; congestion control protects the network.

## Application communication
An application creates a network socket to communicate

[[Network socket]] is an OS-managed communication endpoint. An application accesses that socket through the OS's socket API. 

When data arrives at a machine, the operating system looks at the **destination port** to determine which socket/application should receive it.

TCP provides the communication mechanism.

**The port acts as the bridge between TCP networking and the application process.**

> IP identifies the machine, port identifies the network endpoint/application-socket on that machine, and TCP provides the reliable connection between those endpoints.

### Transmission Control Protocol (TCP) Architecture

#### Protocol Primitives & Characteristics

- **Stream-Oriented Abstraction:** Operates as a continuous byte stream. Application-layer write boundaries are entirely discarded at the transport layer.
    
- **Connection-Oriented (Stateful):** Requires explicit state synchronization for setup (3-way handshake) and teardown (4-way handshake).
    
- **Full-Duplex:** Establishes independent, bi-directional transmit (TX) and receive (RX) channels over a single connection.
    
- **Multiplexing:** Identifies unique connections using the standard 4-tuple: `(Source IP, Source Port, Destination IP, Destination Port)`.
    
- **Underlying Application Substrate:** Serves as the transport foundation for protocols requiring guaranteed delivery (e.g., HTTPS, SSH).
    

#### Reliability & Control Mechanisms

- **Guaranteed, Ordered Delivery:** Utilizes sequence (SEQ) numbers and acknowledgment (ACK) numbers to track byte offsets, ensuring in-order delivery to the application space.
    
- **Error Recovery:** Transparently handles out-of-order segments, packet loss, and data corruption via retransmission (e.g., Retransmission Timeout, Fast Retransmit).
    
- **Flow Control:** Receiver dynamically advertises its available buffer capacity (Receive Window, `rwnd`) to throttle the sender, preventing application buffer exhaustion.
    

#### Buffer & Memory Management

- **TCP Send Buffer (TX):**
    
    - Data is queued here via application syscalls (`write()`, `send()`).
        
    - The OS/TCP stack segments the byte stream into Maximum Segment Sizes (MSS) for IP encapsulation.
        
    - Multiple consecutive application writes may be coalesced into a single TCP segment, or a single write may be fragmented across multiple segments.
        
    - Application threads block (or return `EAGAIN`/`EWOULDBLOCK`) if the TX buffer is full.
        
- **TCP Receive Buffer (RX):**
    
    - Segments are collected, reordered, and buffered upon arrival.
        
    - Data is exposed to the application layer stream (`read()`, `recv()`) as it becomes contiguous.
        
- **Boundary Enforcement (Application Layer Responsibility):** Because TCP is stream-based, protocols relying on it _must_ implement application-level framing (e.g., `Content-Length` headers, delimited payloads) to parse discrete messages out of the continuous stream.
    

#### Protocol Encapsulation (Layer 4)

- **TCP over IP:** TCP headers and payload (Segments) are encapsulated within IP Packets. IP fragment boundaries have zero correlation to original application write boundaries.
    
- **Comparison to UDP:** UDP operates at the same layer and provides multiplexing (ports) over IP, but retains the Layer 3 datagram (packet-based) model without state, flow control, or delivery guarantees.
    

#### Connection Teardown (State Machine)

- **Half-Close Capability:** Because channels are independent, each direction is terminated separately, allowing a peer to stop transmitting while continuing to receive.
    
- **Termination Sequence (4-Way Handshake):**
    
    1. Active closer transmits a `FIN` control flag.
        
    2. Passive closer acknowledges with an `ACK`. (The remote application receives an `EOF` on its next `read()` operation).
        
    3. Passive closer transmits its own `FIN` when its application channel is closed.
        
    4. Active closer responds with a final `ACK`.