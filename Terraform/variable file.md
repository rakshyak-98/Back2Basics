[[Terraform setup]] [[Terraform workflow]] [[terraform]] [[terraform provider]] [[Terraform CLI]]

# variable file

> Variables, locals, outputs, and tfvars make one Terraform configuration work across environments without editing resource blocks.





## Interview Relevance
Interviewers test precedence order, `sensitive` limits, validation blocks, and why secrets never live in committed tfvars.

## Sources
- [HashiCorp — Input variables](https://developer.hashicorp.com/terraform/language/values/variables) — deep-dive
- [HashiCorp — Output values](https://developer.hashicorp.com/terraform/language/values/outputs) — overview
- Yevgeniy Brikman, *Terraform: Up & Running* — overview

## Recall Cues
- Why do interviewers care about precedence order, `sensitive` limits, validation blocks, and why secrets never live in committed tfvars?
- What is step 1: `-var` / `-var-file` on CLI?
- What is step 2: `*.auto.tfvars` / `*.auto.tfvars.json`?
- What is step 3: `terraform.tfvars` / `terraform.tfvars.json`?
- What is step 4: environment `TF_VAR_<name>`?
- What is step 5: `default` in the variable block?
- What mistake is **Committing secrets in tfvars**?
- What mistake is **Debugging “wrong value” without checking precedence**?

## Technical Details
```hcl
variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Cloud region to deploy to"
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "tags" {
  type = map(string)
  default = { Env = "dev", Owner = "platform" }
}

variable "app_config" {
  type = object({
    name     = string
    version  = string
    replicas = number
  })
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "stage", "prod"], var.environment)
    error_message = "environment must be dev, stage, or prod."
  }
}
```

Precedence (highest wins):

1. `-var` / `-var-file` on CLI
2. `*.auto.tfvars` / `*.auto.tfvars.json`
3. `terraform.tfvars` / `terraform.tfvars.json`
4. environment `TF_VAR_<name>`
5. `default` in the variable block

```shell
export TF_VAR_region=us-west-2
terraform plan -var-file=prod.tfvars
terraform apply -var-file=env/prod.tfvars
```

```hcl
locals {
  name_prefix = "${var.environment}-${var.project}"
  common_tags = merge(var.tags, { ManagedBy = "terraform" })
}

output "vpc_id" {
  value       = aws_vpc.main.id
  description = "ID of the app VPC"
}

output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}

module "vpc" {
  source     = "./modules/vpc"
  cidr_block = var.vpc_cidr
  env        = var.environment
}
```

```shell
terraform output
terraform output -raw vpc_id
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Missing required var | `terraform plan` error | Pass `-var`, tfvars, or env `TF_VAR_` |
| Wrong value wins | precedence order | Remember CLI > tfvars > env > default |
| Sensitive still logged | provider debug logs | Avoid TRACE; mark sensitive; scrub CI logs |
| Type mismatch | variable type vs value | Fix type or cast in locals |
| Module can't see root var | not passed into module | Pass explicitly in module block |

## Mistakes to Avoid
- Committing secrets in tfvars.
- Debugging “wrong value” without checking precedence.
- Expecting child modules to see root variables without passing them.
- Treating `sensitive` as encryption.

## Comparison
- Wire into providers → [[terraform provider]] · [[Terraform setup]].
- Used at plan/apply → [[Terraform workflow]] · [[Terraform CLI]].

## Real-World Applications
Per-env `prod.tfvars` / `dev.tfvars`, module inputs for VPC CIDRs, and outputs consumed by remote-state data sources.

**Example:** CI injects `TF_VAR_db_password` from a secret store while `environment` and `region` come from committed non-secret tfvars.

## Pros/Cons or Trade-offs
- **Pro:** One codebase, many environments, validated inputs.
- **Con:** `sensitive = true` only redacts CLI UI — state and some logs can still hold values.
- **Con:** Hard-coding is fine for throwaways until a second environment appears.
