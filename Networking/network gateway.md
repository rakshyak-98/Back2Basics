> [!INFO]
> find your public IP `https://ifconfig.me`

### 0.0.0.0 - Default gateway
- routes traffic from a local network to destinations outside the network, such as the internet.
- means default route. All traffic that does not match a more specific route in the routing table will be sent to this gateway.
- in the context of IP addressing, is used to represent an unspecified address.
- means it not bound to any specific address on the host.
- in routing tables, `0.0.0.0/0` is used to specify the default route. The `/0` network mask interface that no bits are fixed, so this route matches any destination IP address.

### How to access private network from public IP over the internet?
- To access a private network (behind NAT/firewall) from a public IP over the internet, you need to punch through the NAT or relay/forward.

#### Port forwarding
- you control the router/firewall on the private network.
##### From Router
1. Run Node.js app on know port
2. Login to your router (usually `192.168.1.1`)
3. go to **Port Forwarding**
4. Forward external port (e.g., `8080`) -> internal IP `192.168.1.x:3000`
5. Find your public IP (e.g., https://ifconfig.me)

#### Reverse SSH Tunnel
```bash
ssh -R 8080:localhost:3000 user@public-server.com;
```

#### VPN (Virtual Private Network)
#### ZeroTier/Tailscale/Ngrok/Cloudflare Tunnel