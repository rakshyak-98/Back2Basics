Egress -> Traffic that leaves VPC and goes out to the internet
Ingress -> Traffic that comes in from the internet. 

|Direction|Name|Example in Your 3-Tier Lab|Who Usually Pays?|
|---|---|---|---|
|Internet → INTO VPC|Ingress|Someone in India opens your website → data enters AWS|Almost always free|
|← OUT OF VPC|**Egress**|Your EC2 downloads updates, sends logs to CloudWatch, RDS backup to S3|This one can cost money!|

> [!NOTE]
> - Do everything in the same region (don’t copy files to Mumbai if you’re in N. Virginia)
> - Use s3, CloudWatch, SSM inside the same region -> zero cost
> - Cache packages (create your own yum repo or Docker registry inside VPC)
> - Use CloudWatch -> set retention to 1-3 months instead of "never expire"

## How to check Ingress Egress usage

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +"%Y-%m-01"),End=$(date -u +"%Y-%m-%d") \
  --granularity MONTHLY \
  --metrics "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["Data Transfer"]}}'
```