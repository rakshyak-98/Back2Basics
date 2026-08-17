[[Terraform setup]] [[terraform provider]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]]

# Terraform

> Terraform declares cloud resources as code and applies planned changes — desired state in HCL, executed through provider plugins against cloud APIs.

```txt
        Terraform ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers expect declarative IaC versus ClickOps/scripts, resource versus …

## Sources
- [HashiCorp — What is Terraform?](https://developer.hashicorp.com/terraform/intro) — overview
- Yevgeniy Brikman, *Terraform: Up & Running* — deep-dive
- Scott Winkler, *Terraform in Action* — deep-dive

## Key Concepts
- **Declarative + plan:** review the diff before apply.
- **Building blocks:** `terraform {}`, `provider`, `resource`, `data`, `variable`/`output`/`locals`,…
- **Implicit graph:** attribute references create dependencies; file order among `*.tf` does not.
- **State:** maps addresses to real IDs — deleting state does not delete cloud resources.


- **Core:** You describe the desired end state in HCL

## Technical Details
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.region }

resource "aws_s3_bucket" "logs" {
  bucket = "${var.env}-app-logs"
}
```

```shell
terraform init && terraform plan -out=tfplan && terraform apply tfplan
```

| Knob | Why it matters |
|------|----------------|
| `required_providers` pin | Same plugin on laptop and CI |
| `resource` vs `data` | Manage vs read-only lookup |
| Module `version` | Avoid surprise upstream breaks |

```hcl
resource "<PROVIDER>_<TYPE>" "<NAME>" {
  # arguments (desired config)
}
# Reference: <PROVIDER>_<TYPE>.<NAME>.<ATTR>

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

module "vpc" {
  source     = "./modules/vpc"
  cidr_block = var.vpc_cidr
  env        = var.environment
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"
}
```

| Approach | Problem |
|----------|---------|
| ClickOps (console) | Not repeatable, no review, drift |
| Scripts alone | Imperative, brittle order, hard to parallelize |
| Terraform | Declarative, plan before apply, state + dependency graph |

| Symptom | Check | Fix |
|---------|-------|-----|
| No config files | Empty dir | Add `.tf`, then `terraform init` |
| Provider not found | `required_providers` / network | Pin source; re-`init` |
| Unexpected replace | Force-new attr changed | Plan carefully; use `lifecycle` |
| State drift | Manual console edits | `plan` then import or adopt |
| Module version jump | Unpinned `source` | Pin `version = "~> x.y"` |

## Mistakes to Avoid
- **Mistake:** Treating state deletion as resource deletion
- **Mistake:** Unpinned providers/modules drifting between CI and laptop
- **Mistake:** Expecting data sources to create infrastructure

## Pros/Cons or Trade-offs
- **Pro:** Reviewable, versioned infrastructure with a dependency graph and remote state locking.
- **Con:** Day-2 application image tags belong in CI/CD, not every Terraform apply.
- **Con:** Half-baked HCL can be riskier than a careful console + runbook for one irreversible change.

## Comparison
- Install / backends → [[Terraform setup]]
- vs cloud SDKs alone: Terraform owns drift detection and team state


### Use cases
- VPCs, IAM, EKS/RDS baselines, and reusable registry modules reviewed in PRs.

- **Example:** A team pins `hashicorp/aws ~> 5.0`, plans in CI, and applies onl…
