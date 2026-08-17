[[Terraform setup]] [[terraform]] [[terraform provider]] [[Terraform CLI]] [[variable file]]

# Terraform workflow

> The core Terraform loop is init → plan → apply (and destroy) — desired HCL plus credentials plus state become cloud API calls and an updated state file.

```txt
        Terraform workflow ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe state locking, dependency graphs, lifecycle guards, and wh…

## Sources
- [HashiCorp — Core Terraform workflow](https://developer.hashicorp.com/terraform/intro/core-workflow) — deep-dive
- Yevgeniy Brikman, *Terraform: Up & Running* — deep-dive
- Scott Winkler, *Terraform in Action* — overview

## Technical Details
```txt
.tf desired state  +  credentials  +  state file
                         │
                    terraform plan
                         │
              + create / ~ update / - destroy
                         │
                   terraform apply
                         │
                 cloud API + new state
```

| Step | Command | Purpose |
|------|---------|---------|
| Initialize | `terraform init` | Download providers/modules; configure backend |
| Plan | `terraform plan` | Diff: desired config vs state (+ refresh from cloud) |
| Apply | `terraform apply` | Execute the plan; update state |
| Destroy | `terraform destroy` | Remove managed resources; clear state |

```shell
terraform init
terraform plan -out=tfplan
terraform apply tfplan
terraform destroy

terraform init -upgrade
terraform init -migrate-state
terraform state list
terraform state show aws_instance.web
```

- What `init` does: read `required_providers` / modules → download to `.terrafo…

- What `plan`/`apply` do: load config + [[variable file]] → refresh state → com…

```hcl
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags]
  }
}
```

| Argument | Use |
|----------|-----|
| `create_before_destroy` | Zero-downtime replacements |
| `prevent_destroy` | Guard rails for critical resources |
| `ignore_changes` | Stop Terraform fighting out-of-band edits |

- Safe team loop: branch + PR with plan in CI

| Symptom | Check | Fix |
|---------|-------|-----|
| State lock held | Who holds remote lock | Wait or `force-unlock` after confirming no run |
| Plan empty but drift | Refresh off / wrong workspace | `terraform workspace show`; refresh on |
| Apply partial fail | Which resource errored | Fix API error; re-apply (idempotent) |
| Destroy blocked | `prevent_destroy` | Remove lifecycle guard deliberately |
| Wrong backend | `backend` block vs old state | `init -migrate-state` |

## Mistakes to Avoid
- **Mistake:** Interactive apply that diverges from the reviewed CI plan
- **Mistake:** Casual `force-unlock` while another run is alive
- **Mistake:** Destroy in production without a destroy plan review
- **Mistake:** Fighting both the console and Terraform on the same objects

## Pros/Cons or Trade-offs
- **Pro:** Diff-driven changes with locking beat shared local state.
- **Con:** Hotfixes outside Terraform create drift — import or accept it consciously.
- **Con:** `force-unlock` during a live apply can corrupt state.

## Comparison
- Language blocks → [[terraform]]; plumbing → [[Terraform setup]]; CLI flags → [[Terraform CLI]].
- Data-source-only applies can change state/outputs without changing cloud inventory.


### Use cases
- PR plans for network changes, production applies from saved plans, and guarde…

- **Example:** CI posts `terraform plan` on a PR
