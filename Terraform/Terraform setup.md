[[terraform]] [[terraform provider]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]]

# Terraform setup

> Getting started & project plumbing — **Terraform: Up & Running** (Brikman) + **Terraform in Action** (Winkler).

Setup = install CLI → pin versions → configure [[terraform provider]] → auth → (optional) remote state → first [[Terraform workflow]].

---

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

## Version constraints (Brikman)

Pin Terraform **and** providers so laptops and CI behave the same.

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

| Constraint | Meaning |
|------------|---------|
| `~> 5.0` | ≥ 5.0.0 and < 6.0.0 |
| `>= 1.5.0, < 2.0.0` | Allow patches/minors in 1.x only |
| Exact `"5.40.0"` | Strictest pin for prod CI |

Details: [[terraform provider]]

---

## Provider blocks (cloud endpoint)

> [!NOTE] Winkler — provider block is the bridge from HCL to the API (region / project / subscription).

### AWS
```hcl
provider "aws" {
  region = var.aws_region
}
```

### GCP
```hcl
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
```

### Azure
```hcl
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}
```

### Kubernetes
```hcl
provider "kubernetes" {
  config_path = "~/.kube/config"
}
```

Aliases / multi-region → [[terraform provider]]

---

## Authentication (never commit secrets)

> [!WARNING] Brikman — secrets in env, secret manager, or CI; not in `.tf` or committed `.tfvars`.

| Cloud | Typical auth |
|-------|----------------|
| AWS | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`, `~/.aws/credentials`, SSO, IAM role |
| GCP | `GOOGLE_APPLICATION_CREDENTIALS`, `gcloud` ADC |
| Azure | `az login`, SP env (`ARM_CLIENT_ID` …), managed identity |

Pass non-secret knobs via [[variable file]] (`TF_VAR_*`, `*.tfvars`).

---

## Remote state / backend (Brikman — state chapter)

Local `terraform.tfstate` is fine solo. Teams need:

1. Shared storage
2. Encryption
3. **Locking** (two applies don’t corrupt state)

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

Also common: GCS, Azure Blob, HCP Terraform / Terraform Cloud, HTTP.

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

All root `*.tf` files are merged into one config (order of files does not matter).

### Environments (Brikman)

Prefer **separate directories** (or separate state keys) for `dev` / `stage` / `prod` over relying only on workspaces for isolation.

---

## First-run checklist

1. Install Terraform
2. `versions.tf` + provider → [[terraform provider]]
3. Cloud credentials
4. Optional `backend.tf`
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
