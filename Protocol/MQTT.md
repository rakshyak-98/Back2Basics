[[TCP]] · [[UDP]] · [[webSocket]] · [[Firebase/FCM Token (Firebase Cloud Messaging Token)]]

# MQTT

> MQTT is a lightweight publish/subscribe messaging protocol for constrained devices and unreliable networks — brokers fan out messages to subscribers by topic, with QoS levels trading delivery guarantees for overhead.

---

## Roles

| Component | Function |
|-----------|----------|
| **Publisher** | Sends messages to a **topic** |
| **Broker** | Routes messages (Mosquitto, HiveMQ, AWS IoT Core) |
| **Subscriber** | Receives messages for subscribed topic filters |

OASIS standard [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html); v3.1.1 widely deployed.

## Topic hierarchy

```
sensors/building-a/floor-2/temperature
```

Wildcards:

- `+` — single level
- `#` — multi-level suffix

## QoS levels

| QoS | Guarantee | Handshake |
|-----|-----------|-----------|
| **0** | At most once (fire and forget) | None |
| **1** | At least once (may duplicate) | PUBACK |
| **2** | Exactly once | Four-step |

Choose QoS 0 for telemetry where loss is acceptable; QoS 1 for commands.

## Transport

- **TCP 1883** — cleartext (lab only)
- **TCP 8883** — TLS
- **WebSocket** — browser clients

## Session example (mosquitto)

```bash
mosquitto_sub -h broker.example.com -t 'sensors/+/temp' -u device -P secret
mosquitto_pub -h broker.example.com -t 'sensors/room1/temp' -m '22.5'
```

## vs [[HTTP module]] / [[webSocket]]

| MQTT | HTTP |
|------|------|
| Persistent subscription | Request/response |
| Tiny headers | Heavier per message |
| Broker required | Direct client-server |

Common in IoT, mobile push bridges, and industrial SCADA.

## Security

- Unique credentials per device
- TLS + cert pinning on brokers
- ACLs per topic prefix

## Recall

- When does QoS 1 duplicate messages?
- Why is a broker required unlike point-to-point TCP?

## Sources

- [MQTT Version 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
- [Eclipse Mosquitto](https://mosquitto.org/documentation/)
