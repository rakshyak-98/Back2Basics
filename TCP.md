Transmission Control Protocol
- Data is continuous flow of bytes.
- The application cannot write more data when the buffer is full.
- TCP is [[Byte stream]] instead of packet based.
- multiplexing.
- Connection oriented protocol (formal purpose for setup and tear down).
- reliable delivery.
- recovery from errors (build in feature).
- can manage out-of-order messages or re-transmissions (can be re-sent from the source).
- flow control (the receiver can manage how much data is sent).
- HTTPS
	- return receipt
- [[SSH]]
	- terminal communication between systems.
- Application doesn't worry about out of order frames or missing data.
- TCP handles all the communication.

layer is added to top of IP packets. TCP provides:
- [[Byte stream]] instead of packets.
- Reliable and ordered delivery.
- UDP is on the same layer as TCP, but is still packed-based like the lower layer.
- UDP just adds port numbers over IP packets.
1. TCP send buffer: This is where data is stored before transmission. Multiple writes are indistinguishable from a single write.
2. Data is encapsulated as one or more IP packets, IP boundaries have a relationship to the original write boundaries.
3. TCP receive buffer: data is available to application as it arrives.
>[!INFO] Protocols are required to interpret TCP data by imposing boundaries within the byte stream.

- TCP is bidirectional and Full Duplex, Once established
	- TCP connection can be used as a bi--directional byte stream
	- with 2 channels for each direction.
- TCP END with 2 Handshakes
	- A peer tells the other side that no more data will be sent with the FIN flag.
	- other side ACKs the FIN.
	- remote application is notified of the termination when reading from the channel.
	- each direction of channel can be terminated independently, so the other side also performs the same handshake to fully close the connection.