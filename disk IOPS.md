Dist IOPS (Input/Output Operations Per second). Number of read + write operations a storage device can complete in 1 second. Measures operation count, not data size.

```bash
iostat -dx 1
```

per process I/O (database process)

```bash
pidof mysqld;
pidof postgres;

pidstat -d 1
```

Cloud databases (Use provider monitoring dashboard)
- AWS RDS -> CloudWatch -> ReadIOPS, WritIOPS
- Azure SQL -> Azure Monitor -> IOPS metrics
- Google Cloud SQL -> Cloud Monitoring -> Disk Read/Write Operations