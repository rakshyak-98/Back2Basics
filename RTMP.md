Real Time Messaging Protocol -> is a streaming protocol designed for low-latency live video delivery.

> [!NOTE]
> Most CDNs and players phased it out by 2020 due to complexity and Flash dependency

> [!INFO]
> ~2-3 second delay (vs 30+ seconds with HTTP)

- Maintains persistent TCP connection
- Auto-reconnect on network hiccups
- Bidirectional communication. Encoder can receive commands from server (stop, pause, quality adjust. Can switch streams mid-broadcast.