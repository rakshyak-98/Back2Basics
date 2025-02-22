An Amazon Resource Name (ARN) is a unique identifier for AWS resources.
- a standard format used to specify resources across different AWS services.

> [!INFO] ARN Look like this
> ```txt
> arn:partition:service:region:account-id:resource
> ```
> ```txt
> arn:aws:iam::123456789012:user/john_doe
> arn:aws:ec2:us-east-1:123456789012:instance/i-0abcd1234efgh5678
> arn:aws:lambda:us-east-1:123456789012:function:my-function
>  ```


| Component  | Description                                 | Example Value                 |
| ---------- | ------------------------------------------- | ----------------------------- |
| arn        | Prefix for all ARNs                         |                               |
| partition  | AWS partition (aws, aws-cn, aws-us-gov)     | aws                           |
| service    | AWS service name (e.g., `S3`, `ec2`, `iam`) | `iam`                         |
| region     | AWS region (if applicable)                  |                               |
| account-id | AWS account number                          |                               |
| resource   | The specific resource name or path          | `bucket-name/folder/file.txt` |
> [!INFO] Why ARN Important
> - Many AWS cli and SDK operations require ARN to specify resources.