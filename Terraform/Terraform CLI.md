[[Terraform setup]] [[terraform provider]] [[Terraform workflow]] [[terraform]] [[variable file]]

# Terraform CLI

> Terraform CLI is the day-to-day command surface — init, plan, apply, fmt/validate, logging, provider schema, and careful state surgery.

```txt
        Terraform CLI ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers watch for saved plans (`-out`), CI `fmt`/`validate`, and treatin…

## Sources
- [HashiCorp — Terraform CLI](https://developer.hashicorp.com/terraform/cli) — deep-dive
- Yevgeniy Brikman, *Terraform: Up & Running* — overview
- Scott Winkler, *Terraform in Action* — overview

## Key Concepts
- **Workflow quartet:** init → plan → apply → destroy ([[Terraform workflow]]).
- **Inspect before guess:** `providers schema` is the contract for arguments.
- **Sharp tools:** state mv/rm; prefer `moved` blocks in code.
- **Logs leak secrets:** never leave `TF_LOG=TRACE` in CI artifacts.

## Technical Details
```shell
terraform version
terraform fmt -recursive
terraform validate
terraform init
terraform plan
terraform apply
terraform destroy
terraform output
terraform console
```

### Init flags

```shell
terraform init
terraform init -upgrade
terraform init -reconfigure
terraform init -migrate-state
terraform init -backend=false
```

### Plan / apply flags

```shell
terraform plan -out=tfplan
terraform apply tfplan
terraform apply -auto-approve           # CI only; risky interactively
terraform plan -var='region=us-west-2'
terraform plan -var-file=prod.tfvars
terraform plan -target=aws_instance.web # surgical; avoid habitually
```

### Logging

```shell
TF_LOG=DEBUG terraform init
TF_LOG=TRACE terraform plan
TF_LOG_PATH=./terraform.log terraform apply
```

| Level | When |
|-------|------|
| `ERROR` | Failures only |
| `WARN` | Unusual but continuing |
| `INFO` | High-level steps |
| `DEBUG` | Provider plugin chat (usual debug) |
| `TRACE` | Very noisy |

### Provider / schema / state

```shell
terraform providers
terraform providers schema -json | jq '.provider_schemas | keys'
terraform state list
terraform state show ADDRESS
terraform state mv OLD NEW
terraform state rm ADDRESS      # stop managing — does not destroy cloud object
terraform state pull
```

| Var | Role |
|-----|------|
| `TF_LOG` / `TF_LOG_PATH` | Logging |
| `TF_VAR_name` | Set variable `name` |
| `TF_DATA_DIR` | Override `.terraform` dir |
| `TF_CLI_ARGS_plan` | Extra default args for a subcommand |

- First-time checklist: no `.tf` → create config

## Mistakes to Avoid
- **Mistake:** Hand-editing `terraform.tfstate`
- **Mistake:** Leaving TRACE logs with secrets in CI
- **Mistake:** Habitual `-target` instead of fixing the graph
- **Mistake:** Applying without a saved plan that was reviewed

## Pros/Cons or Trade-offs
- **Pro:** One CLI covers format, validate, graph execution, and inspection.
- **Con:** `-target` and state surgery create drift habits if overused.
- **Con:** Auto-approve interactively skips human review.

## Comparison
- vs console ClickOps: CLI shines when configuration is code.
- Backend living in [[Terraform setup]]; provider RPC detail in [[terraform provider]].


### Use cases
- CI pipelines that fmt/validate/plan on PR, and on-call debugging of provider …

- **Example:** `terraform plan -out=tfplan` in CI
