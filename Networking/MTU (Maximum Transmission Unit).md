Defines the largest size, in bytes, of a data packet that can be transmitted over a network medium without fragmentation.
- In Ethernet networks, the standard MTU is 1500 bytes.

In an Ethernet network with an MTU of 1500 bytes, if a device needs to send a 1600-byte packet, the packet must be fragmented into two smaller packets to accommodate the MTU limitation.

> MTU is the maximum size (in bytes) of a single network packet that can be transmitted over a network without fragmentation.
- `mtu 1500` -> Maximum packet size = 1500 bytes


### Example

```txt
4000 bytes
    │
    ├── Packet 1: 1500 bytes
    ├── Packet 2: 1500 bytes
    └── Packet 3: 1000 *bytes*
```
if a package exceeds the MTU and fragmentation is allowed, it is split into multiple packages, if fragmentation is not allowed (e.g., with the IP "Don't Fragment" flag), the packet is dropped and an error my be generated