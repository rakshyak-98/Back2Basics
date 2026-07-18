Egress traffic from a VPC to the public internet typically traverses through a managed gateway or a NAT device.

### Standard NAT Gateway platform
- used for private instances needing internet access without unsolicited inbound connections.

Flow: Private Subnet -> Route Table -> Nat Gateway -> Internet Gateway (IGW) -> Public Internet