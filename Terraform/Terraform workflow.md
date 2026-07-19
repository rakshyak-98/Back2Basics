[[Terraform setup]] [[terraform]] [[terraform provider]] [[Terraform CLI]] [[variable file]]

# Terraform workflow

> Core loop & state — **Terraform: Up & Running** (Brikman) + **Terraform in Action** (Winkler).

---

## Mental model (both books)

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

Concepts used in this loop:

| Concept | Meaning | Notes |
|---------|---------|-------|
| Provider | Which cloud/API | [[terraform provider]] |
| Resource | Managed object | [[terraform]] |
| Variable | Per-env input | [[variable file]] |
| Output | Value to show / share | [[variable file]] |
| Module | Reusable package | [[terraform]] |
| State | Record of what Terraform owns | [[Terraform setup]] backends |

---

## The four commands

| Step | Command | Purpose |
|------|---------|---------|
| Initialize | `terraform init` | Download providers/modules; configure backend |
| Plan | `terraform plan` | Diff: desired config vs state (+ refresh from cloud) |
| Apply | `terraform apply` | Execute the plan; update state |
| Destroy | `terraform destroy` | Remove managed resources; clear state |

Prereqs: [[Terraform setup]] · debug: [[Terraform CLI]]

```shell
terraform init
terraform plan -out=tfplan
terraform apply tfplan
terraform destroy
```

---

## Dependency graph (Winkler)

Before plan, Terraform builds a DAG of resources:

- **Implicit** edges from references (`ami = aws_ami…` / `subnet_id = aws_subnet.a.id`)
- **Explicit** `depends_on` when there is no attribute reference but order still matters
- Independent nodes can run **in parallel**

That’s why file order among `*.tf` files does not define apply order.

---

## What `init` does

1. Read `required_providers` / module sources
2. Download plugins → `.terraform/`
3. Configure backend (local or remote)
4. Write `.terraform.lock.hcl` (provider checksums — commit this; Brikman/team practice)

```shell
terraform init
terraform init -upgrade          # allow newer providers within constraints
terraform init -migrate-state    # after backend change
```

---

## What `plan` / `apply` do

1. Load config + [[variable file]] values
2. Refresh state against cloud (unless `-refresh=false`)
3. Compute actions: create / update / replace / destroy
4. Apply: call [[terraform provider]], then write state

```txt
│ Error: No configuration files
│ The directory … contains no Terraform configuration files.
```

→ add at least one `.tf` (e.g. `main.tf` with a [[terraform provider]] block), then `terraform init`.

---

## State: why it exists (Brikman)

`terraform.tfstate` maps addresses → real IDs/attributes.

| Without state | With state |
|---------------|------------|
| Guess what exists | Know what Terraform created |
| Risk of duplicates | Diff-driven changes |
| Solo only | Remote + lock for teams |

```shell
terraform state list
terraform state show aws_instance.web
terraform refresh   # sync state from cloud (use carefully)
```

> [!INFO] Apply of **data sources only** can change state/outputs without changing cloud infrastructure.

Example: reading `data.aws_instances.all` and writing an output updates local/remote state, not EC2 inventory.

Remote backend + DynamoDB/Blob lease locking → [[Terraform setup]]

---

## Lifecycle meta-arguments (Winkler)

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

---

## Safe team loop (Brikman)

1. Branch + PR with plan output in CI
2. Remote state unlocked only after apply finishes
3. Secrets never in git
4. Pin versions (`.terraform.lock.hcl` committed)

---

## Related

- Language building blocks → [[terraform]]
- First project plumbing → [[Terraform setup]]
- Provider RPC / aliases → [[terraform provider]]
- Logs & schema → [[Terraform CLI]]
