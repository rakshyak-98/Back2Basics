A production load balancer should avoid continuously sending traffic to a failed backend.

**Fault tolerance** A system is fault tolerant when failure of one component does not automatically cause total system failure.

> [!WARNING]
> One nginx instance can itself become a single point of failure. Nginx does not inherently require an upper-layer load balancer.
> - it require an upper-layer traffic-distribution mechanism **when you deploy multiple Nginx instance and need them to appear as one highly available service endpoint.**

**Multiple Nginx instance** -> nginx itself is replicated
**Load balancer in front** -> distributes traffic across Nginx instances and removes unhealthy instances.
**Floating/virtual IP** -> in environment using keeplived/VRRP, virtual IP can move from a failed Nginx node to a health one.
**Cloud-Managed load balancer** -> cloud load balancers can provide the entry point and health-check Nginx instance.

> [!NOTE]
> The **upper-layer load-balancing mechanism itself must provide high availability.**