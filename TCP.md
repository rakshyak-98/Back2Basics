[[Byte stream]] [[SSH]] 

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