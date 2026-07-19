[[Terraform setup]] [[terraform provider]] [[Terraform workflow]] [[Terraform CLI]] [[variable file]] [[Terraform docker]]

# Terraform

> Core notes from **Terraform: Up & Running** (Yevgeniy Brikman) and **Terraform in Action** (Scott Winkler).

Terraform is a declarative Infrastructure as Code (IaC) tool. You describe the **desired end state** in HCL; Terraform figures out create / update / delete against cloud APIs through [[terraform provider]] plugins.

---

## Why Terraform (Brikman)

| Approach | Problem |
|----------|---------|
| ClickOps (console) | Not repeatable, no review, drift |
| Scripts alone | Imperative, brittle order, hard to parallelize |
| Terraform | Declarative, plan before apply, state + dependency graph |

Brikman: treat infra like software — code review, versioning, reusable modules, CI.

---

## Building blocks (Winkler)

| Block | Role |
|-------|------|
| `terraform {}` | Version pins, backends → [[Terraform setup]] |
| `provider` | Cloud/API plugin config → [[terraform provider]] |
| `resource` | Manage something (create/update/delete) |
| `data` | Read-only lookup of existing info |
| `variable` / `output` / `locals` | Inputs, exports, computed names → [[variable file]] |
| `module` | Reusable folder of config |

---

## Resource

```hcl
resource "<PROVIDER>_<TYPE>" "<NAME>" {
  # arguments (desired config)
}
```

Reference elsewhere: `<PROVIDER>_<TYPE>.<NAME>.<ATTR>`

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  tags = {
    Name = "web"
  }
}
```

- Implicit dependency: using another resource’s attribute creates an edge in the graph (Winkler).
- Explicit: `depends_on = [aws_iam_role_policy.example]`

---

## Data source (read-only)

```hcl
data "<PROVIDER>_<TYPE>" "<NAME>" {
  # filters / query params
}
```

Reference: `data.<PROVIDER>_<TYPE>.<NAME>.<ATTR>`

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}
```

> [!INFO] Data sources do not create cloud resources. On apply they refresh reads and may only update [[Terraform workflow|state]] / outputs.

---

## Modules (Brikman — “how to stay DRY”)

```hcl
module "vpc" {
  source = "./modules/vpc"

  cidr_block = var.vpc_cidr
  env        = var.environment
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

- Local path, Git URL, or Terraform Registry
- Each module has its own `variables.tf` / `outputs.tf` / `main.tf`
- Layout: [[Terraform setup]]

---

## Registry

Public hub: `registry.terraform.io`

- **Providers** — API plugins → [[terraform provider]]
- **Modules** — packaged patterns (VPC, EKS, RDS)

```hcl
module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"
}
```

Always pin module `version` (Brikman).

---

## State (preview)

Terraform stores IDs and attributes in `terraform.tfstate` so the next `plan` can compare desired vs actual.

- Solo: local state
- Team: remote backend + locking → [[Terraform setup]]
- Behavior in the apply loop → [[Terraform workflow]]

---

## Related graph

- Install / versions / auth / backend → [[Terraform setup]]
- Provider plugins & aliases → [[terraform provider]]
- init → plan → apply → destroy → [[Terraform workflow]]
- CLI / logging / schema → [[Terraform CLI]]
- Variables & tfvars → [[variable file]]
- Docker provider example → [[Terraform docker]]
