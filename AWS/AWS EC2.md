[[AWS]] [[AWS Networking]] [[Security group]] [[AMI (Amazon Machine Image)]] [[EBS]] [[ARN (Amazon Resource Name)]]

# AWS EC2

Turning compute capacity into an **API-controlled infrastructure resource** instead of treating the physical server as the deployment boundary, the architecture treats an independently provisionable virtual machine as that boundary.

**Vertical scaling dependency:** capacity increases require hardware procurement, installation, migration, and eventually another hardware ceiling. Even when the hardware is available, the application remains coupled to one machine's failure domain.

EC2 survives these problems by making the VM the provisioning boundary. The physical hardware remains AWS's concern, while the application receives a logically isolated, virtualized compute environment with its own CPU, memory, storage, networking, operating system, and security boundary. 

Bootstrap scripts setup are scripts that run where an instance is launched to automatically configure it.

**Launch EC2 -> User data/bootstrap script runs -> Install/configure software -> start application -> instance becomes ready**
For example, a bootstrap script might:
- Install Java
- Install/configure Nginx
- Pull your application artifact
- Set environment/configuration
- Start the service
- Register the instance with a load balancer

**Instance Store** is temporary, block-level storage physically attached to the host running an EC2 instance. Unlike EBS, its lifetime is tied to the EC2 instance, so it is designed for data that can be recreated rather than durable applications state. 
- instance store exists to provide **very low-latency, high-throughput local storage** without introducing a separate network-attached storage layer. It is useful for workloads such as caches, temporary files, buffers, scratch space, intermediate computation, and data that is replicated elsewhere. The available capacity and number of volumes are properties of the selected EC2 instance type; not ever instance you provided instance store.

The critical property is **ephemerality**. Data survives an ordinary reboot, but is lost when the instance is stopped, hibernated, terminated, or otherwise loses the associated instance-store lifetime; the volume cannot be detached from one instance and attached to another.

"This makes instance store particularly valuable is **stateless or distributed architectures.**" For example, an application server can keep a large local cache or temporary processing data on instance store while the authoriative copy remains in S3, a database, or another durable system. If the server disappears, the system simply reconstructs that local data on a replacement instance.

> At the system level, introducing instance store **reduce storage latency and can provide extremely high local I/O throughput,** while avoiding a separate storage charge for the included instance-store capacity.
- The trade-off is durability: the application must tolerate data loss and cannot treat instance store as its source of truth. It also couples storage capacity to the chosen instance type and makes instance replacement a storage loss event.

[[Network Attached Storage]]
[[AWS S3]] durable object storage suitable for preserving data outside the lifecycle of compute instances.

different instance for different workloads/computer power/ processing power
general task  
compute optimize instances
memory optimize instances
storage optimize instances

EBS  (persistent block storage)
- attach to one instance to another
- when EBS volumn fails (replicate in availablity zons) EBS snapshot (safe points), data protection , and migration data to different regions. Schedule snapshot of EBS volumes.
- AMI (pre configured package to launch to instance with specific configs), to standardize the deployments, and share configuration. Packing and distribution application.

EFS (Network file system)
- shared access to multiple launched instances
- shared network drive
- data sharing
- EFS can grow and shrink (dynamic)
- NFS (primiry used in linux environment not native support for windows)

IMDS
- get information about themselves
- each instance can access + IAM role used
- used for dynamic configuration to configure them selves appropriately
IMDSv1
IMDSv2 (more security) always use

T series instances (occasional requirement)

M5.2xlarge -> instance family and generation M (general puprose), 2x instance size nano/micro/large

security groups - traffic control for EC2
- customize security groups allow/deny rules on traffic, setting rule for control access.
- remember the connection access
- common ports 22, 443, 80, 3389 (RDP windows)

EC2 purchasing (Pricing model)
on demand instances - pay for what you use. short terms (testing environments)
reserved instances - leasing for longer term
saving plans instances
spot instances
dedicated host (physical server)/dedicate instances (not shared hardware)

## Mental model

An EC2 instance is compute on shared hardware (or Dedicated Host) with **ENI(s)** in a subnet. Launch = AMI + instance type + key pair/instance profile + [[Security group]]. Storage = root + optional [[EBS]] volumes. **Terminate ≠ delete all billable artifacts.**

```
Launch template ──► AMI + type + subnet + SG + user-data
                         │
                         ├── instance profile (IAM role → STS creds)
                         └── EBS volumes (persist after terminate unless delete_on_termination)
```

Every instance needs a **VPC** (default or custom) — networking is not optional ([[AWS Networking]]).

## Standard config / commands

### Launch checklist (prod)

| Setting | Typical choice | Why |
|---------|----------------|-----|
| Subnet | Private app tier | No direct internet exposure |
| Public IP | Off (use ALB) | Smaller attack surface |
| SG | Tier-specific (`app-sg`) | Not `default` |
| IAM | Instance profile with least privilege | No keys on disk |
| IMDS | v2 required, hop limit 1 (2 for containers) | SSRF credential theft mitigation |
| EBS | `gp3`, encrypted, `delete_on_termination` tuned | Cost + compliance |
| User-data | cloud-init bootstrap | Idempotent; log to `/var/log/cloud-init-output.log` |

```bash
aws ec2 describe-instances --filters "Name=tag:Env,Values=prod" \
  --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name,Type:InstanceType,Subnet:SubnetId}'

aws ec2 terminate-instances --instance-ids i-xxx
# THEN verify orphans:
aws ec2 describe-volumes --filters "Name=status,Values=available"
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null]'
```

### AZ awareness

- Check **subnet AZ** matches resilience plan — `describe-instances` → `Placement.AvailabilityZone`.
- Multi-AZ ASG: one subnet per AZ in LT/ASG.

### Budget / billing visibility

- IAM: allow billing console for finance role (not every developer).
- **AWS Budgets** + Cost Anomaly Detection on EC2/NAT/EIP line items.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Instance unreachable (SSH/app) | SG, NACL, route, public IP/subnet | Full path debug ([[AWS Networking]], [[Security group]]) |
| Status checks failed | System vs instance check in console | Reboot; migrate if hardware; fix disk full (instance check) |
| Out of CPU credits (T-family) | CloudWatch `CPUCreditBalance` | Unlimited mode or resize to M/C family |
| User-data didn't run | `/var/log/cloud-init-output.log`; MIME multipart | Fix script; re-run with `cloud-init clean` |
| IAM role calls fail on instance | Profile attached? IMDS reachable? | Attach profile; curl IMDSv2 token flow |
| Bill after terminate | EBS volumes, EIP, NAT GW, snapshots | Delete orphans (see WARNING below) |
| Wrong region/AZ capacity | `InsufficientInstanceCapacity` | Retry another AZ/type; use capacity reservations |

## Gotchas

> [!WARNING]
> **Terminate EC2, then manually delete EBS volumes, Elastic IPs, and NAT gateways** — terminate stops compute; **EBS/EIP/NAT keep charging** if left behind.

> [!WARNING]
> **Don't attach EIP + NAT casually** — each EIP costs when unassociated; NAT GW hourly + per-GB.

> [!WARNING]
> **Default VPC placement** — fine for sandbox; prod needs explicit subnet tiering.

> [!WARNING]
> **Stopping vs terminating** — stop preserves EBS; terminate (with default delete_on_termination) removes root volume per setting.

## When NOT to use

- **Long-running stateless web at scale without ASG** — use Auto Scaling Group + ALB.
- **Batch/analytics** — consider Fargate, [[AWS Lambda]], or Spot Fleet for cost.
- **Bare metal driver/hardware timing needs** — consider Dedicated Hosts or on-prem.

## Related

[[AWS]] · [[AWS Networking]] · [[Elastic IP]] · [[Security group]] · [[AMI (Amazon Machine Image)]] · [[EBS]] · [[aws STS (Security Token Service)]] · [[AWS Auto Scaling]] · [[ALB (Application Load Balancer)]] · [[AWS Lambda]]
