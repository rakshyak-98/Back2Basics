- control the rate of data transfer to prevent congestion, ensure fair resource distribution, and maintain Quality of Service (QoS).

### Throttling algorithms
#### Token bucket
- allows burst of traffic while enforcing an average rate limit.
- Tokens are added to a bucket at a fixed rate; packets can be sent only if there are enough tokens.
- Efficient for controlling bursty traffic.
#### Leaky bucket
- Converts variables traffic into a steady flow.
- Packets enter a queue (bucket) and leave at a constant rate.
- Prevents congestion but may drop excess packets if the bucket overflows.
#### Rate-based throttling (fixed rate limiting)
- strictly limits traffic to a predefined rate (e.g., Mbps).
- simple but can lead to inefficient bandwidth utilization.
#### Random Early Detection (RED)
- Proactively drop packets based on queue length and probability to prevent congestion.

> [!INFO] (RED) Random Early Detection is used in TCP congestion control.

#### Explicit Congestion Notification (ECN)
- Marks packets instead of dropping them to signal congestion to the sender.
- works with TCP to reduce congestion without packet loss.

#### TCP flow control & Congestion Control (e.g., TCP Reno, Cubic)
- Adjusts sending rate dynamically based on network feedback (ACKs, dropped packets).
- Ensures fair bandwidth sharing.