[[IAM]] · [[AWS Lambda]] · [[Docker/docker file]] · [[AWS cli commands]]

# AWS ECR

> Elastic Container Registry stores Docker/OCI images privately in your AWS account — Lambda, ECS, and EKS pull images using IAM-authenticated `docker push` and `docker pull`.

---

## Repositories and images

- **Repository** — logical name (`my-app/backend`)
- **Image** — identified by tag and immutable **digest** (`sha256:…`)
- **Lifecycle policies** — expire untagged or old images to control storage cost
- **Scanning** — basic or enhanced vulnerability scanning on push

Images are regional. Replicate across regions for disaster recovery with ECR replication rules.

## Authentication

ECR uses a token from [[aws STS (Security Token Service)]]:

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

## Push workflow

```bash
aws ecr create-repository --repository-name my-app
docker build -t my-app:latest .
docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
```

Deploy by **digest**, not floating `:latest`, in production pipelines.

## IAM permissions (typical CI role)

```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:GetAuthorizationToken",
    "ecr:BatchCheckLayerAvailability",
    "ecr:PutImage",
    "ecr:InitiateLayerUpload",
    "ecr:UploadLayerPart",
    "ecr:CompleteLayerUpload"
  ],
  "Resource": "*"
}
```

`GetAuthorizationToken` is account-wide; repository actions scope to [[ARN (Amazon Resource Name)]].

## Integration points

| Consumer | Notes |
|----------|-------|
| **ECS / Fargate** | Task definition `image` URI |
| **EKS** | `imagePullSecrets` not needed when node/instance role allows ECR |
| **Lambda** | Container image functions up to 10 GB |

## Recall

- Why deploy by digest instead of tag?
- What breaks if `ecr:GetAuthorizationToken` is missing from the CI role?

## Sources

- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [OCI Image Specification](https://github.com/opencontainers/image-spec)
