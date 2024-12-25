process of dividing a large data package into smaller units
- to ensure they can traverse network links with smaller [[MTU (Maximum Transmission Unit)]]
- When a packet exceeds the MTU of a network segment, routers or devices along the path divide the packet into fragments. Each fragment is transmitted separately and reassembled at the destination.
- The receiving host or device reassembles the fragments into the original packet using information in the packet headers, such as fragment offsets and identifiers.
### **Example**
Consider a scenario where a 2000-byte packet needs to traverse a network with an MTU of 1500 bytes. The packet is fragmented into two parts:

- **Fragment 1:** 1480 bytes of data + 20-byte header = 1500 bytes
- **Fragment 2:** 480 bytes of data + 20-byte header = 500 bytes

Each fragment is transmitted separately and reassembled at the destination.