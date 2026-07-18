Network Address Translation -> modifies IP headers in transit, remapping address spaces by overwriting source/destination IP addresses and/or port numbers in the packet header. It enables private network address conservation and topology hiding.

## Lifecycle Hooks & Packet Processing

Ingress (Internal to External)
	- lookup -> check session table for existing flow.
	- Allocation -> if absent, assign ephemeral port from range `1024-65535`
	- Rewrite -> Replace `Source_IP` with `Public_IP` and `Source_port` with `Assigned_Port`
	- Checksum -> Recalculate IP and TCP/UDP checksums.