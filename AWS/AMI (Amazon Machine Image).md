is a pre-configured template that contains everything needed to launch an EC2 instance, including:
- OS, Application Server and dependencies.
- EBS volume Snapshots (Root volume + additional storage if needed).

> [!INFO] Features of API
> - When you start an [[AWS EC2]] instance, you must select an AMI as the base image.
> - you can create your own API by customizing an existing EC2 instance and saving it as a image.
> - AWS Marketplace API -> Pre-configures images with commercial software (e.g., WordPress, Jenkins).
> - AMI are ties to specific AWS region but can be copied to other regions.
> - AMI use [[EBS (Elastic Block Store)]] snapshots to store the root volume.