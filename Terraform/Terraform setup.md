[[terraform]] [[terraform provider]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]]

# Terraform setup

> Getting started & project plumbing — **Terraform: Up & Running** (Brikman) + **Terraform in Action** (Winkler).

---

## Index

- [[#Prerequisites]]
- [[#Install CLI]]
- [[#Verification]]
- [[#Mental model]]
- [[#Version constraints (Brikman)]]
- [[#AWS configuration]]
- [[#GCP configuration]]
- [[#Other providers (same pattern)]]
- [[#Remote state rules (Brikman — state chapter)]]
- [[#File layout (both books)]]
- [[#First-run checklist]]
- [[#Book map]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Triage (when things break)]]
- [[#Related]]

## Prerequisites

…

## Install CLI

[HashiCorp Linux install](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

```shell
sudo apt install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
terraform -install-autocomplete
terraform version
```

---

## Verification

```bash
# smoke test
```

## Mental model

Setup = install CLI → pin versions → configure [[terraform provider]] → authentication → (optional) remote state → first [[Terraform workflow]].

## Version constraints (Brikman)

Pin Terraform **and** providers so laptops and CI behave the same.

| Constraint          | Meaning                          |
| ------------------- | -------------------------------- |
| `~> 5.0`            | ≥ 5.0.0 and < 6.0.0              |
| `>= 1.5.0, < 2.0.0` | Allow patches/minors in 1.x only |
| Exact `"5.40.0"`    | Strictest pin for prod CI        |

Use **one** cloud block below per root module (or both if you truly manage AWS + GCP from the same root). Details: [[terraform provider]]

---

## AWS configuration

### versions.tf
```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### providers.tf
```hcl
provider "aws" {
  region = var.aws_region
  # optional: profile = "my-sso-profile"
}
```

### variables (non-secret)
```hcl
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for the default provider"
}
```

### Auth
| Method                                        | When                          |
| --------------------------------------------- | ----------------------------- |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | Local / CI keys               |
| `~/.aws/credentials` + `AWS_PROFILE`          | Named profiles                |
| AWS SSO / IAM Identity Center                 | Human interactive             |
| Instance / task IAM role                      | EC2, ECS, Lambda, GitHub OIDC |

> [!WARNING] Brikman — never commit access keys in `.tf` or `.tfvars`.

### Remote state (S3 + DynamoDB lock)
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

Create the bucket + lock table **once** (often by hand or a bootstrap stack) before `terraform init`.

---

## GCP configuration

### versions.tf
```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
```

Need GKE / beta APIs? Also pin `hashicorp/google-beta` the same way (`~> 5.0`).

### providers.tf
```hcl
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
  # zone optional; many resources take it per-resource
}
```

### variables (non-secret)
```hcl
variable "gcp_project" {
  type        = string
  description = "GCP project ID (not display name)"
}

variable "gcp_region" {
  type        = string
  default     = "us-central1"
  description = "Default region for regional resources"
}
```

### Auth
| Method                                          | When                              |
| ----------------------------------------------- | --------------------------------- |
| `gcloud auth application-default login`         | Local ADC                         |
| `GOOGLE_APPLICATION_CREDENTIALS=/path/key.json` | SA key file (CI / break-glass)    |
| Workload Identity / attached SA                 | GCE, GKE, Cloud Build, GitHub WIF |

Prefer short-lived ADC / WIF over long-lived JSON keys.

### Remote state (GCS — built-in locking)
```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "my-tf-state"
    prefix = "prod/network"
  }
}
```

GCS backends lock via object generation — no separate DynamoDB equivalent. Create the bucket first (versioning on is a good default).

---

## Other providers (same pattern)

> [!NOTE] Winkler — provider block is the bridge from HCL to the API (region / project / subscription).

### Azure
```hcl
# versions: hashicorp/azurerm ~> 3.0
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}
```

authentication: `az login`, SP environment (`ARM_CLIENT_ID` …), or managed identity. Backend: Azure Blob.

### Kubernetes
```hcl
provider "kubernetes" {
  config_path = "~/.kube/config"
}
```

Aliases / multi-region → [[terraform provider]]

Pass non-secret knobs via [[variable file]] (`TF_VAR_*`, `*.tfvars`).

---

## Remote state rules (Brikman — state chapter)

Local `terraform.tfstate` is fine solo. Teams need shared storage, encryption, and **locking**.

| Cloud | Backend | Locking |
|-------|---------|---------|
| AWS | `s3` | DynamoDB table (or S3 native lock on newer TF) |
| GCP | `gcs` | Built into GCS backend |
| Either | HCP Terraform / TFC | Platform-managed |

Also common: Azure Blob, HTTP.

After changing backend: `terraform init -migrate-state` → [[Terraform workflow]]

---

## File layout (both books)

```txt
project-root/
├── main.tf            # resources + module calls
├── variables.tf       # input variable declarations
├── outputs.tf         # outputs
├── terraform.tfvars   # non-secret values (gitignore secrets)
├── versions.tf        # required_version + required_providers
├── providers.tf       # provider blocks
├── backend.tf         # remote state
└── modules/
    └── <name>/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

All root `*.tf` files are merged into one configuration (order of files does not matter).

### Environments (Brikman)

Prefer **separate directories** (or separate state keys) for `dev` / `stage` / `prod` over relying only on workspaces for isolation.

---

## First-run checklist

1. Install Terraform
2. Pick cloud: AWS or GCP section above → `versions.tf` + `providers.tf`
3. authentication (environment / ADC / role) — never commit secrets
4. Optional remote `backend.tf` (S3 or GCS)
5. `terraform init` → download plugins ([[Terraform CLI]])
6. `terraform plan` → `terraform apply` ([[Terraform workflow]])
7. Stuck? `TF_LOG=DEBUG` ([[Terraform CLI]])

---

## Book map

| Topic | Source |
|-------|--------|
| Why IaC, state, modules, envs, secrets | *Terraform: Up & Running* — Brikman |
| HCL blocks, providers, dependency graph | *Terraform in Action* — Winkler |
| Language overview | [[terraform]] |
| Non-cloud practice | [[Terraform docker]] |
| E-commerce EKS layout (extends setup) | [[ecommerce-eks-layout]] |

## Gotchas

> [!WARNING]
> **Local state on a shared repo** — two applies corrupt ownership; use remote + lock.

> [!WARNING]
> **Keys in `.tfvars`** — Brikman: secrets via env / CI / vault only.

## When NOT to use

- **Exploring a single console resource** — click first, then codify.
- **No cloud account yet** — practice with [[Terraform docker]] first.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `terraform` not found | PATH / install | Reinstall CLI; check `terraform version` |
| Provider auth fail | Cloud creds / SSO | Fix profile/role; never commit keys |
| Backend init fail | Bucket / lock table / perms | Create backend resources; fix IAM |
| Version clash | `required_version` vs binary | Upgrade CLI or relax constraint |
| Wrong account | Profile / assume_role | Confirm `aws sts get-caller-identity` |

## Related

[[terraform]] [[terraform provider]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]] [[ecommerce-eks-layout]]
