**EBS** in AWS stands for **Elastic Block Store**.
- **Purpose**: It provides persistent block storage for EC2 instances.
- **Use**: It stores data such as file systems, databases, or application data.
- **Scalability**: EBS volumes can be dynamically resized, and you can attach them to EC2 instances.
- **Types**: Includes SSD-backed (General Purpose, Provisioned IOPS) and HDD-backed (Throughput Optimized, Cold) options.

### Advantages:
- Persistent data storage.
- Scalability and flexibility in size.
- High performance and low latency.

### Disadvantages:

- Cost varies based on usage and storage.
- Requires careful management of backups and snapshots to prevent data loss.

> [!INFO] Create retention rule for EBS volumes 
> - [AWS Recycle bin](https://ap-south-1.console.aws.amazon.com/rbin/home?region=ap-south-1#Home)
- go to EC2 snap shot, and view the Storage tier tab, you can move the span shot by archiving the snap shot

### EBS Snapshots
EBS Snapshot are point-in-time backups of AWS Volumes.
- stored in Amazons S3 and can be used to restore data or create new EBS volumes.

> [!NOTE] Snapshots are stored in AWS S3
> - but you cannot access them like regular S3 objects.
> - you can only use them to create new EBS volumes.
> - Snapshots can be copied to another AWS region for disaster recovery.
> - Can share snapshot with other AWS accounts.
> - AWS Backup or [[DML (AWS Data Lifecycle Manager)]] can automate snapshot creation and retention.