## Setup AWS Budget Setup
- allow IAM user and role to IAM user and role access to billing information.
- go to charges live services.
- configure IAM role to the instance.

> [!INFO] check the availability zone at the network tab in the EC2 instance page.

### Why need to create VPC when launching instance
- AWS create a VPC (default or custom) because Networking is essential for running EC2 instance.
- if you don't create a VPC, AWS automatically places your EC2 instance in the default VPC of the selected region.
- Every EC2 instance needs a network (IP, routing, security)
- VPC provides a controlled, private environment for instances.
- Subnet management -> segregates instances (public, private, database layers).

Default VPC -> Free (AWS Provide it automatically)
- Subnets, Route Tables, Internet Gateway -> free (included in the default VPC).
- Security Groups and NACLs -> Free (default rules apply).