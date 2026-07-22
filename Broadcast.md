Broadcast = One sender -> All devices in the same broadcast domain (LAN).

```txt
        Sender
           |
   -----------------
   |   |   |   |   |
  PC1 PC2 PC3 PC4 PC5
```
- Every device receives the packet, even if it doesn't need it.

Characteristics
- Sent to every host in the subnet.
- Routers do not forward broadcast packets by default.
- Increase unnecessary network traffic.

> [!INFO]
> Routers generally do not forward broadcasts, so the request would never reach an Internet server.