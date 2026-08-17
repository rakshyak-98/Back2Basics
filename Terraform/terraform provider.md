[[Terraform setup]] [[terraform]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]]

# terraform provider

> A provider is a plugin that implements create/read/update/delete against an API — Terraform core loads it and reconciles resources; it does not hard-code EC2 or GCE itself.





## Interview Relevance
Interviewers want version pins, aliases for multi-region/account, schema as the argument contract, and credentials never in HCL.

## Sources
- [HashiCorp — Providers](https://developer.hashicorp.com/terraform/language/providers) — deep-dive
- Scott Winkler, *Terraform in Action* — deep-dive
- Yevgeniy Brikman, *Terraform: Up & Running* — overview

## Key Concepts
- **Plugin boundary:** core builds the graph; provider RPC performs each resource op.
- **`required_providers`:** source + version constraint; lock file pins checksums.
- **Aliases:** extra provider instances for other regions/accounts — set `provider = aws.west` on resources.
- **Resource vs data:** same plugin ships both manage and lookup types.

## Technical Details
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_s3_bucket" "logs" {
  provider = aws.west
  bucket   = "my-logs-west"
}

resource "aws_vpc" "app" { … }   # manage
data "aws_vpc" "existing" { … }  # lookup only
```

Without `provider = …`, resources use the default (unaliased) instance.

Flow: `init` downloads plugins → plan/apply calls provider RPC → attributes land in state ([[Terraform workflow]]).

```shell
terraform providers
terraform providers mirror ./mirror
terraform providers schema -json | jq '.provider_schemas | keys'
TF_LOG=DEBUG terraform init
```

| Do | Don’t |
|----|--------|
| Env vars, roles, ADC, SSO | Hardcode access keys in HCL |
| Short-lived credentials in CI | Commit `.tfvars` with secrets |

Non-cloud: Docker → [[Terraform docker]]; Kubernetes example under [[Terraform setup]].

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth failed | Env / profile / role | Fix cloud creds; never hardcode in HCL |
| Wrong region | Default vs `alias` | Set `provider = aws.west` on resource |
| Schema unknown arg | Provider version | Upgrade pin; check `providers schema` |
| Init can’t download | Registry / mirror / proxy | Mirror or open registry access |
| Lock file conflict | `.terraform.lock.hcl` | Commit lock; `init -upgrade` on purpose |

## Real-World Applications
Multi-region DR buckets, GitHub/Kubernetes providers beside cloud, and provider mirrors in air-gapped CI.

**Example:** Default `aws` in `us-east-1` plus `aws.west` for a replica bucket — each resource selects its provider explicitly.

## Pros/Cons or Trade-offs
- **Pro:** One workflow across clouds and SaaS APIs.
- **Con:** Unpinned providers drift between CI and laptop.
- **Con:** Not every SaaS click deserves a Terraform resource.

## Comparison
- Setup context → [[Terraform setup]]; language → [[terraform]]; flags → [[Terraform CLI]].
- Read-only inventory may be simpler with cloud SDKs than a full provider graph.

## Mistakes to Avoid
- Forgetting `provider =` on aliased resources — silent wrong region/account.
- “Latest” provider in production.
- Storing credentials in provider blocks.
