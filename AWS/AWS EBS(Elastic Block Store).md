[[AWS EC2]] [[EBS (Elastic Block Store)]] [[AWS EFS (Elastic File System)]] [[AWS Billing and cost management]]

# AWS EBS(Elastic Block Store)

> EBS is network-attached block storage for EC2 instances — the canonical note is [[EBS (Elastic Block Store)]]; this page covers the same service with emphasis on console naming and attach workflows.

```txt
        AWS EBS(Elastic Bl ──┬── Interview
               ├── Sources
               ├── Mechanism
               └── Pitfalls
```

## Interview Relevance
- **Interview probes:** Interviewers ask about AWS EBS(Elastic Block Store) to see whether you can de…

## Sources
- [Amazon EBS User Guide](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html) — overview

## Technical Details
### Quick attach workflow

1. Create volume in the **same Availability Zone** as the target [[AWS EC2]] instance.
2. Choose type (usually **gp3**), size, and encryption.
3. Attach volume to instance; note device name (`/dev/sdf` → often `/dev/nvme1n1` on Nitro).
4. Partition, format (once), mount, add `fstab` entry.

```bash
aws ec2 create-volume --availability-zone us-east-1a --size 50 --volume-type gp3
aws ec2 attach-volume --volume-id vol-0abc --instance-id i-0abc --device /dev/sdf
```

### Operations checklist

| Task | Command / action |
|------|------------------|
| List volumes | `aws ec2 describe-volumes` |
| Snapshot | `aws ec2 create-snapshot --volume-id vol-0abc` |
| Detach safely | Stop writes, `umount`, then `detach-volume` |
| Delete | Detach first; snapshots remain until deleted separately |

## Mistakes to Avoid
- **Mistake:** **Volume stuck attaching**
- **Mistake:** **Wrong AZ** — volume and instance must match AZ
- **Mistake:** **Full disk** — expand volume, grow partition, resize filesystem

See [[EBS (Elastic Block Store)]] for volume types, encryption, and comparison with [[AWS EFS (Elastic File System)]].
