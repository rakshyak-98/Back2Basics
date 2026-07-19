[[Terraform setup]] [[terraform]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]]

# terraform provider

> Provider deep-dive — **Terraform in Action** (Winkler) + **Terraform: Up & Running** (Brikman).

A **provider** is a plugin that implements Create / Read / Update / Delete against an API (AWS, GCP, Azure, GitHub, Kubernetes, Docker, …).

Terraform core does not know EC2 or GCE — it loads the provider, then asks it to reconcile resources. Setup context: [[Terraform setup]].

---

## Declare source + version

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

- `source` → `registry.terraform.io/<namespace>/<name>`
- `version` → always constrain (Brikman: avoid “latest” in prod)
- Written once during [[Terraform setup]]; plugins fetched by `terraform init`

---

## Configure the provider

```hcl
provider "aws" {
  region = var.region
  # optional: profile, shared_credentials_files, assume_role, …
}
```

Winkler: arguments here are **provider-level** (region, endpoints, auth), not resource arguments.

Values often come from [[variable file]].

---

## Aliases (multi-region / multi-account)

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_s3_bucket" "logs" {
  provider = aws.west
  bucket   = "my-logs-west"
}
```

Without `provider = …`, resources use the **default** (unaliased) instance.

---

## How Terraform talks to providers

1. `terraform init` downloads plugin binaries into `.terraform/providers`
2. Plan/apply: core builds a graph (Winkler), then calls the provider RPC for each resource op
3. Provider returns attributes → written into state ([[Terraform workflow]])

Debug conversation: `TF_LOG=DEBUG terraform init` → [[Terraform CLI]]

---

## Auth reminders

| Do | Don’t |
|----|--------|
| Env vars, roles, ADC, SSO | Hardcode access keys in HCL |
| Short-lived credentials in CI | Commit `.tfvars` with secrets |

Full cloud table: [[Terraform setup]]

---

## Inspect providers

```shell
terraform providers
terraform providers mirror ./mirror
```

```shell
# schemas (attributes, required vs optional)
terraform providers schema -json | jq '.provider_schemas | keys'

terraform providers schema -json \
  | jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["aws_instance"]'
```

More flags: [[Terraform CLI]]

---

## Resource vs data for a provider

Same provider ships both:

```hcl
resource "aws_vpc" "app" { … }   # manage
data "aws_vpc" "existing" { … }  # lookup only
```

Language detail: [[terraform]]

---

## Non-cloud providers

Same pattern — `required_providers` + `provider` block:

- Docker → [[Terraform docker]]
- Kubernetes → example under [[Terraform setup]]

---

## Book takeaways

- **Winkler**: provider = plugin; config block; aliases; schema drives valid args
- **Brikman**: pin versions; never store credentials in code; registries for providers/modules
