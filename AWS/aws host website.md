[[Route53]] · [[AWS EC2]] · [[IAM]] · [[AWS Billing and cost management]]

# aws host website

> The cheapest way to host a static website on AWS is S3 static website hosting plus CloudFront (optional) and Route 53 for DNS — no EC2 required unless you need server-side logic.

---

## Architecture options

| Pattern | Best for |
|---------|----------|
| **S3 + CloudFront** | Production static sites, HTTPS, global cache |
| **S3 website endpoint only** | Internal demos, HTTP-only |
| **Amplify Hosting** | SPA with CI/CD built in |
| **EC2 + nginx** | When you need custom server config (usually overkill for static files) |

## S3 static hosting (classic pattern)

1. Create S3 bucket named to match site (e.g. `www.example.com`) or use CloudFront with any bucket name.
2. Enable **static website hosting**; set `index.html` and `error.html`.
3. Upload files; set public read via bucket policy (or keep private and use CloudFront OAC).
4. Request ACM certificate in **us-east-1** for CloudFront custom domain.
5. Create CloudFront distribution with S3 origin, HTTPS redirect, compression.
6. Point [[Route53]] A/AAAA alias to CloudFront.

### Bucket policy (public read example — prefer OAC in production)

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::www.example.com/*"
  }]
}
```

## Why CloudFront

- **HTTPS** with free ACM certificates at the edge
- **Caching** reduces S3 request cost and latency
- **Origin Access Control (OAC)** keeps bucket private

## SPA routing

Configure CloudFront custom error response: `403` → `/index.html` with `200` so client-side routers work.

## Cost levers

S3 storage + requests, CloudFront data transfer, Route 53 hosted zone monthly fee. Static sites at low traffic are typically cents per month.

## Recall

- Why must ACM certificates for CloudFront be in us-east-1?
- When is S3 alone without CloudFront insufficient for production?

## Sources

- [Hosting a static website on Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Getting started with a secure static website (CloudFront + S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/website-hosting-cloudfront-walkthrough.html)
