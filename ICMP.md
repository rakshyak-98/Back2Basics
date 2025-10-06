Internal Control Message Protocol
- Used for network diagnostics (`ping`, `traceroute`).
- Echo Request -> sent by client.
- Echo Reply -> returned by server.

An ICMP sequence -> refers to the sequence number field in an ICMP Echo Request/Reply request, commonly seen in `ping`. It helps track and match packets.

- each echo request gets a unique sequence number, usually incremented by 1.
- helps the sender:
	- match replies to requests.
	- Detect packet loss.
	- Measure round-trip time per packet.

> [!NOTE]
> Wraps around after 65535 (16-bit field).