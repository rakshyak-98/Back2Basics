[[Terraform setup]] [[Terraform workflow]] [[terraform]] [[terraform provider]] [[Terraform CLI]]

# variable file

> Inputs, locals, outputs, tfvars — **Terraform: Up & Running** (Brikman) + **Terraform in Action** (Winkler).

Variables make one config work across envs (dev/stage/prod) without editing resource blocks. They feed [[terraform provider]] region/project and resource args during [[Terraform workflow]].

---

## Declare inputs (`variables.tf`)

```hcl
variable "variable_name" {
  type        = string          # or number, bool, list, map, object, any
  default     = null            # optional; omit => required
  description = "Why this exists"
  sensitive   = false           # hide from CLI UI when true
  nullable    = true
}
```

### Scalar
```hcl
variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Cloud region to deploy to"
}
```

### List
```hcl
variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}
```

### Map
```hcl
variable "tags" {
  type = map(string)
  default = {
    Env   = "dev"
    Owner = "platform"
  }
}
```

### Object (Winkler — structured config)
```hcl
variable "app_config" {
  type = object({
    name     = string
    version  = string
    replicas = number
  })
}
```

### Validation (Brikman — catch bad inputs early)
```hcl
variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "stage", "prod"], var.environment)
    error_message = "environment must be dev, stage, or prod."
  }
}
```

Reference in config: `var.region`, `var.tags["Env"]`.

---

## How values are supplied (precedence)

Highest wins (simplified from HashiCorp docs / both books):

1. `-var` / `-var-file` on CLI
2. `*.auto.tfvars` / `*.auto.tfvars.json`
3. `terraform.tfvars` / `terraform.tfvars.json`
4. Env `TF_VAR_<name>`
5. `default` in the variable block

```shell
export TF_VAR_region=us-west-2
terraform plan -var-file=prod.tfvars
```

```hcl
# terraform.tfvars  (non-secrets only — gitignore secrets)
region      = "us-east-1"
environment = "dev"
```

> [!WARNING] Brikman — do **not** commit secrets in `tfvars`. Use env / secret store / CI.

Project layout: [[Terraform setup]]

---

## Locals (named expressions)

```hcl
locals {
  name_prefix = "${var.environment}-${var.project}"
  common_tags = merge(var.tags, {
    ManagedBy = "terraform"
  })
}

resource "aws_instance" "web" {
  # …
  tags = local.common_tags
}
```

Winkler: locals avoid repeating concatenations; not overridable from outside like variables.

---

## Outputs (`outputs.tf`)

```hcl
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "ID of the app VPC"
}

output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

```shell
terraform output
terraform output -raw vpc_id
```

Brikman: outputs are the module’s public API — also how root modules share values (`module.vpc.vpc_id`) and how remote state consumers read deps.

---

## Module variables

Child modules declare their own `variable` blocks; root passes values:

```hcl
module "vpc" {
  source = "./modules/vpc"

  cidr_block = var.vpc_cidr
  env        = var.environment
}
```

Module overview: [[terraform]]

---

## Book takeaways

| Practice | Source |
|----------|--------|
| Variables + separate env dirs/files | Brikman |
| Types, objects, locals, expressions | Winkler |
| Validate + `sensitive` | Both / modern Terraform |
| Wire into provider | [[terraform provider]] · [[Terraform setup]] |
| Used at plan/apply | [[Terraform workflow]] · [[Terraform CLI]] |
