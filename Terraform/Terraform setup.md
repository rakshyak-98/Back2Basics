[[terraform]] [[terraform provider]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]] [[ecommerce-eks-layout]]

# Terraform setup

> Terraform setup is install the CLI, pin versions, configure providers and auth, optionally remote state, then run the first workflow.





## Interview Relevance
Interviewers ask version pins, remote state + locking, and how secrets stay out of git across AWS/GCP/Azure roots.

## Sources
- [HashiCorp — Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) — overview
- [HashiCorp — Backend configuration](https://developer.hashicorp.com/terraform/language/backend) — deep-dive
- Yevgeniy Brikman, *Terraform: Up & Running* — deep-dive

## Recall Cues
- Why do interviewers care about version pins, remote state + locking, and how secrets stay out of git across AWS/GCP/Azure roots?
- What mistake is **Keys in `.tf` / `.tfvars`**?
- What mistake is **Skipping remote state for collaborative work**?
- What mistake is **Relying only on workspaces for prod isolation**?
- What mistake is **Long-lived JSON GCP keys when WIF/ADC works**?

## Technical Details
### Install CLI

```shell
sudo apt install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
terraform -install-autocomplete
terraform version
```

| Constraint | Meaning |
|------------|---------|
| `~> 5.0` | ≥ 5.0.0 and < 6.0.0 |
| `>= 1.5.0, < 2.0.0` | Allow patches/minors in 1.x only |
| Exact `"5.40.0"` | Strictest pin for prod CI |

### AWS

```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}
```

Auth: access keys, `AWS_PROFILE`, SSO, or instance/task IAM / GitHub OIDC.

### GCP

```hcl
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

terraform {
  backend "gcs" {
    bucket = "my-tf-state"
    prefix = "prod/network"
  }
}
```

Auth: ADC (`gcloud auth application-default login`), `GOOGLE_APPLICATION_CREDENTIALS`, or Workload Identity. GCS locking is built-in.

### Azure / Kubernetes (same pattern)

```hcl
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
```

| Cloud | Backend | Locking |
|-------|---------|---------|
| AWS | `s3` | DynamoDB (or newer S3 native lock) |
| GCP | `gcs` | Built into GCS backend |
| Either | HCP Terraform / TFC | Platform-managed |

```txt
project-root/
├── main.tf / variables.tf / outputs.tf
├── terraform.tfvars   # non-secret values
├── versions.tf / providers.tf / backend.tf
└── modules/<name>/…
```

First-run: install → versions/providers → auth → optional backend → `init` → `plan`/`apply`. Practice without cloud: [[Terraform docker]]. Large layout: [[ecommerce-eks-layout]].

| Symptom | Check | Fix |
|---------|-------|-----|
| `terraform` not found | PATH / install | Reinstall CLI; `terraform version` |
| Provider auth fail | Cloud creds / SSO | Fix profile/role; never commit keys |
| Backend init fail | Bucket / lock table / perms | Create backend resources; fix IAM |
| Version clash | `required_version` vs binary | Upgrade CLI or relax constraint |
| Wrong account | Profile / assume_role | `aws sts get-caller-identity` |

## Mistakes to Avoid
- Keys in `.tf` / `.tfvars`.
- Skipping remote state for collaborative work.
- Relying only on workspaces for prod isolation.
- Long-lived JSON GCP keys when WIF/ADC works.

## Comparison
- Provider aliases/multi-account → [[terraform provider]].
- Non-secret knobs → [[variable file]]; debug → [[Terraform CLI]].

## Real-World Applications
Bootstrapping a team backend once, then per-env roots under `environments/dev|stage|prod`.

**Example:** Create S3 state bucket + DynamoDB lock table by hand once; every root’s `backend.tf` points at a unique key.

## Pros/Cons or Trade-offs
- **Pro:** Repeatable roots with remote lock scale to teams.
- **Con:** Local state on a shared repo invites corrupted ownership.
- **Con:** Exploring one console resource first can be faster — then codify.
