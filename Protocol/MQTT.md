[[webSocket]] [[Messaging/Web hooks]] [[TCP]] [[half-open connections]]

# MQTT

> One-line: lightweight pub/sub for devices and IoT — broker-centric topics, QoS 0/1/2, small headers; not a drop-in for HTTP REST or chat at web scale without ops discipline.

## Mental model

**MQTT** (Message Queuing Telemetry Transport) uses a **broker** (Mosquitto, EMQX, AWS IoT Core). Clients **publish** to **topics** (`sensors/room1/temp`); subscribers receive by topic filter (`sensors/+/temp`, `#` wildcard). Connection is long-lived TCP (often TLS on 8883).

```
Publisher ──PUBLISH topic──► Broker ──forward──► Subscriber(s)
                ▲
         SUBSCRIBE filter
```

**QoS:** 0 at-most-once, 1 at-least-once (dup possible), 2 exactly-once (handshake). **Retained** messages seed new subscribers. **LWT (Last Will)** publishes on unexpected disconnect.

## Standard config / commands

### Ports

| Port | Usage |
|------|--------|
| 1883 | Plain MQTT (lab/VPN only) |
| 8883 | MQTT over TLS |
| 8884 | Often WebSocket MQTT in browsers |

### Subscribe / publish (mosquitto clients)

```bash
mosquitto_sub -h broker.example.com -p 8883 \
  --cafile ca.pem -u device1 -P secret \
  -t 'sensors/+/temp' -v

mosquitto_pub -h broker.example.com -p 8883 \
  --cafile ca.pem -u device1 -P secret \
  -t 'sensors/room1/temp' -m '22.5' -q 1
```

### Mosquitto ACL snippet

```conf
user device1
topic read sensors/room1/#
topic write sensors/room1/temp

listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
require_certificate false
```

### Node.js (mqtt.js)

```javascript
import mqtt from 'mqtt';

const client = mqtt.connect('mqtts://broker.example.com', {
  username: 'device1',
  password: process.env.MQTT_PASSWORD,
  clientId: 'device1-001',
  clean: true,
  reconnectPeriod: 5000,
});

client.on('connect', () => {
  client.subscribe('commands/device1/#', { qos: 1 });
  client.publish('telemetry/device1/status', 'online', { qos: 1, retain: true });
});

client.on('message', (topic, payload) => {
  console.log(topic, payload.toString());
});
```

### Topic design

```txt
tenant/site/device/metric   — avoid single global topic flood
no leading $ for app topics ($SYS reserved by broker)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connect loop | Auth/cert/clientId clash | Unique clientId; verify user/ACL |
| Messages not received | Topic typo vs filter | Log subscribe ack; test with `mosquitto_sub -v` |
| Duplicate messages | QoS 1/2 retries | Idempotent handlers; dedupe by message id |
| Broker CPU spike | `#` subscribers; retained flood | Narrow subscriptions; limit retain |
| Silent disconnect | NAT timeout | Keepalive (ping); broker `max_keepalive` |
| TLS handshake fail | ALPN/SNI; old cipher | Update certs; mqtts:// not mqtt:// |

## Gotchas

> [!WARNING]
> **Plaintext 1883 on public internet** — credentials + payload exposed; use TLS + ACL.

> [!WARNING]
> **QoS 2 is expensive** — use QoS 1 + idempotent consumer for most IoT.

> [!WARNING]
> **Retained messages stale forever** — overwrite with empty retain to clear.

> [!WARNING]
> **Not for large payloads** — spec practical limit ~256MB but brokers often cap KB/MB; use HTTP/S3 for files.

## When NOT to use

- **Request/response HTTP APIs** — REST/gRPC clearer for CRUD.
- **Browser-first real-time** — [[webSocket]] + app server may be simpler than MQTT-over-WS.
- **Guaranteed global ordering** — MQTT doesn't order across topics; design per-key streams.

## Related

[[webSocket]] [[Messaging/Web hooks]] [[TCP]] [[half-open connections]] [[Streaming/Microservice]]
