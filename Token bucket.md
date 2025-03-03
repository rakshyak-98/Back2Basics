- controls data flow by allowing packets to be sent only if there are enough tokens in a bucket. Tokens are added at a fixed rate, enabling bursty traffic while maintaining an average rate limit.

### Implementation
1. A bucket holds tokens (each token represents permission to send a fixed amount of data).
2. Tokens are added at a fixed rate (R tokes per second).
3. If the bucket is full, extra tokens are discarded.
4. When a packet arrives:
	- if enough tokes are available, they are removed, and the packet is sent.
	- if not, the packet is either queued (delayed) or dropped (depending on policy).