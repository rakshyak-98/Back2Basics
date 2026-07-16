
```bash 

ip link set dev en0s31f5 mtu 9000
ip link show  en0s31f5

```


```bash
ip -s link; # Check interface statistics (RX/TX packets)
```

```bash
sar -n DEV 1;
```

```shell
ip -d route; # Show detaild output
ip route show; # output the main table
```

```bash

ip route get 8.8.8.8
# via -> gateway (Next hop) The IP address of the route that forwards the packet toward the destination.
# dev -> Outgoing interface
# src -> source ip

# [Add default gateway]
ip route add default via 192.168.1.1
```

```txt
8.8.8.8 via 192.168.1.1
```
- `via` -> `192.168.1.1` is the next device that receives the packet.
- used when the destination is not on the local network.

