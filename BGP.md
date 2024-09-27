- Border Gateway Protocol
- designed to exchange routing and reliability information among autonomous systems on the Internet.

### How BGP Works

BGP operates as a **path-vector protocol**, which means it maintains a record of the path that data packets take through various ASes. Each BGP router maintains a routing table that is updated based on information received from other routers. This information includes:

- **Network Layer Reachability Information (NLRI)**: This indicates which IP prefixes are reachable.
- **Path Attributes**: These include various metrics like AS_PATH (the list of ASes a route has traversed), LOCAL_PREF (local preference for route selection), and NEXT_HOP (the next hop IP address for reaching a destination).

When routers establish connections, known as **peering**, they exchange routing updates to determine the best paths for data transmission based on policies set by network administrators[1][2][3].

## Why BGP is Used

BGP serves several essential functions in internet routing:

- **Routing Between Networks**: BGP determines the optimal paths for data to travel between different ASes, ensuring efficient data transfer across the internet. It evaluates various factors such as network congestion, geographical location, and administrative policies to select the best route[1][3].

- **Network Stability and Redundancy**: BGP enhances network stability by allowing routers to quickly adapt to changes in network topology. If one path fails, BGP can reroute traffic through an alternative path, maintaining connectivity and reducing downtime[2][4].

- **Traffic Engineering**: Network administrators can implement policies that control how traffic flows between networks. This capability allows for load balancing and optimization of network performance, ensuring efficient use of available resources[2][3].

- **Dynamic Route Discovery**: The protocol enables autonomous systems to discover new routes and adapt to changes in the network structure, such as adding or removing ASes. This adaptability is vital for maintaining an up-to-date routing table[3][4].

### Types of BGP

BGP can be categorized into two main types:

- **External BGP (eBGP)**: Used for exchanging routing information between different autonomous systems. eBGP sessions are typically established between routers located at the edge of their respective ASes.

- **Internal BGP (iBGP)**: Used for routing information within a single autonomous system. iBGP helps maintain consistent routing information among routers within the same organization[1][2].

In summary, BGP is fundamental to the operation of the internet, enabling efficient data routing and ensuring network resilience across diverse and interconnected systems.

Citations:
[1] https://www.techtarget.com/searchnetworking/definition/BGP-Border-Gateway-Protocol
[2] https://www.kentik.com/kentipedia/what-is-bgp-border-gateway-protocol/
[3] https://aws.amazon.com/what-is/border-gateway-protocol/
[4] https://www.javatpoint.com/border-gateway-protocol
[5] https://www.wallarm.com/what/bgp-routing-explanation
[6] https://www.geeksforgeeks.org/border-gateway-protocol-bgp/
[7] https://www.cloudflare.com/learning/security/glossary/what-is-bgp/
[8] https://en.wikipedia.org/wiki/Border_Gateway_Protocol