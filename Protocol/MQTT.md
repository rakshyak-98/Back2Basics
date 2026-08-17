[[TCP]] [[UDP]] [[webSocket]] [[Firebase/FCM Token (Firebase Cloud Messaging Token)]]

# MQTT

> MQTT is a lightweight publish/subscribe protocol for constrained devices and unreliable networks — brokers fan out messages by topic, with QoS levels trading delivery guarantees for overhead.

```txt
        MQTT ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask topic wildcards, QoS 0/1/2 semantics, and when MQTT beats HT…

## Sources
- [MQTT Version 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) — deep-dive
- [Eclipse Mosquitto documentation](https://mosquitto.org/documentation/) — overview

## Key Concepts
- **Publisher / broker / subscriber:** devices publish to topics; the broker routes; subscribers use filters.
- **Topic hierarchy:** slash-separated paths with `+` (one level) and `#` (multi-level suffix) wildc…
- **QoS:** 0 at most once; 1 at least once (may duplicate); 2 exactly once (four-step).
- **Transport:** TCP 1883 cleartext (lab); 8883 TLS; WebSocket for browsers.

## Technical Details
| Component | Function |
|-----------|----------|
| **Publisher** | Sends messages to a **topic** |
| **Broker** | Routes messages (Mosquitto, HiveMQ, AWS IoT Core) |
| **Subscriber** | Receives messages for subscribed topic filters |

- OASIS MQTT 5.0; v3.1.1 still widely deployed.

```
sensors/building-a/floor-2/temperature
```

| QoS | Guarantee | Handshake |
|-----|-----------|-----------|
| **0** | At most once (fire and forget) | None |
| **1** | At least once (may duplicate) | PUBACK |
| **2** | Exactly once | Four-step |

- Choose QoS 0 for telemetry where loss is acceptable; QoS 1 for commands.

```bash
mosquitto_sub -h broker.example.com -t 'sensors/+/temp' -u device -P secret
mosquitto_pub -h broker.example.com -t 'sensors/room1/temp' -m '22.5'
```

- Security baseline: unique credentials per device

## Mistakes to Avoid
- **Mistake:** Cleartext 1883 in production
- **Mistake:** Shared credentials across all devices
- **Mistake:** Using QoS 2 everywhere “for safety”
- **Mistake:** Assuming MQTT replaces point-to-point TCP without planning broke…

## Pros/Cons or Trade-offs
- **Pro:** Persistent subscriptions, tiny headers, works on constrained devices.
- **Con:** Broker is a required middle box — operational and ACL complexity.
- **Con:** QoS 1 duplicates — consumers must be idempotent.

## Comparison
| MQTT | HTTP |
|------|------|
| Persistent subscription | Request/response |
| Tiny headers | Heavier per message |
| Broker required | Direct client-server |

- vs [[webSocket]]: WebSocket is a full-duplex pipe


### Use cases
- IoT sensors, industrial SCADA bridges, and mobile push bridges that need tiny…

- **Example:** Thousands of thermostats publish `sensors/+/temp` at QoS 0
