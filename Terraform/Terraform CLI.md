[[Terraform setup]] [[terraform provider]] [[Terraform workflow]] [[terraform]] [[variable file]]

# Terraform CLI

> Commands & debugging — **Terraform: Up & Running** (Brikman) + **Terraform in Action** (Winkler) + HashiCorp CLI reference.

Most day-to-day work is the [[Terraform workflow]] quartet. This note covers flags, logging, provider inspection, and formatting.

---

## Everyday commands

```shell
terraform version
terraform fmt -recursive      # rewrite HCL style
terraform validate            # syntax + basic type checks (after init)
terraform init
terraform plan
terraform apply
terraform destroy
terraform output
terraform console             # REPL for expressions
```

Brikman tip: run `fmt` + `validate` in CI before plan.

---

## Init flags

```shell
terraform init
terraform init -upgrade                 # refresh providers/modules within constraints
terraform init -reconfigure             # re-ask backend config
terraform init -migrate-state           # move state to new backend
terraform init -backend=false           # skip backend (rare / tooling)
```

Backend living in [[Terraform setup]].

---

## Plan / apply flags

```shell
terraform plan -out=tfplan
terraform apply tfplan                  # apply saved plan exactly
terraform apply -auto-approve           # CI only; risky interactively
terraform plan -var='region=us-west-2'
terraform plan -var-file=prod.tfvars
terraform plan -target=aws_instance.web # surgical; avoid habitually (Brikman)
```

Variable sources: [[variable file]]

---

## Logging (provider troubleshooting)

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

Shows how core talks to [[terraform provider]] plugins.

---

## Provider / schema inspection

```shell
terraform providers
terraform providers mirror ./provider-mirror
```

```shell
terraform providers schema -json \
  | jq '.provider_schemas | keys'

terraform providers schema -json \
  | jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas | keys'

terraform providers schema -json \
  | jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["aws_instance"]'
```

Use schema to learn required args without guessing (Winkler: schema is the contract).

---

## State subcommands (careful)

```shell
terraform state list
terraform state show ADDRESS
terraform state mv OLD NEW      # rename address after refactor
terraform state rm ADDRESS      # stop managing (does not destroy cloud object)
terraform state pull            # dump remote state to stdout
```

> [!WARNING] Brikman — prefer refactor with `moved` blocks / `state mv` over hand-editing `terraform.tfstate`.

Workflow context: [[Terraform workflow]]

---

## Useful env vars

| Var | Role |
|-----|------|
| `TF_LOG` / `TF_LOG_PATH` | Logging |
| `TF_VAR_name` | Set variable `name` |
| `TF_DATA_DIR` | Override `.terraform` dir |
| `TF_CLI_ARGS_plan` | Extra default args for a subcommand |

---

## First-time failure checklist

1. No `.tf` files? → create `main.tf` ([[Terraform setup]])
2. Provider download fail? → `TF_LOG=DEBUG terraform init`
3. Auth errors? → cloud credentials ([[terraform provider]])
4. Wrong region/project? → provider block + [[variable file]]

---

## Book takeaways

- **Brikman**: automate fmt/validate/plan in CI; treat state commands as ops tools
- **Winkler**: schema + graph explain *why* a plan looks that way — use CLI to inspect both
