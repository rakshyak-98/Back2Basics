### 0.0.0.0 - Default gateway
- routes traffic from a local network to destinations outside the network, such as the internet.
- means default route. All traffic that does not match a more specific route in the routing table will be sent to this gateway.
- in the context of IP addressing, is used to represent an unspecified address.
- means it not bound to any specific address on the host.
- in routing tables, `0.0.0.0/0` is used to specify the default route. The `/0` network mask interface that no bits are fixed, so this route matches any destination IP address.

### How to access private network from public IP over the internet?
- To access a private network (behind NAT/firewall) from a public IP over the internet, you need to punch through the NAT or relay/forward.

#### Port forwarding
- you control the router/firewall on the private network 
#### Reverse SSH Tunnel
#### VPN (Virtual Private Network)
#### ZeroTier/Tailscale/Ngrok/Cloudflare Tunnel