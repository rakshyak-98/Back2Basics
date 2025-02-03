- A real-time subscription is a mechanism where a client subscribes to updates from a server and automatically receives new data as soon as it's available, without making repeated requests.

### How it works?
1. Client Subscribes -> sends a request to the server to listen for updates.
2. Server pushes updates -> when new data is available, the server sends it to all subscribed clients.
3. Client Updates UI -> the frontend updates automatically without refreshing the page.

### Technologies for Real-Time Subscriptions

| Technology               | Description                                      | Use Cases                            |
| :----------------------- | :----------------------------------------------- | :----------------------------------- |
| WebSockets               | Persistent Connection between client and server. | Chat apps, live notifications.       |
| SSE (Server-Sent-Events) | Server pushes updates over HTTP.                 | Stock prices, live scores.           |
| GraphQL Subscriptions    | Uses WebSockets for real-time GraphQL data.      | Real-time dashboards, live commetns. |
| MQTT                     | Lightweight protocol for IoT devices.            | Smart home, real-time sensors.       |