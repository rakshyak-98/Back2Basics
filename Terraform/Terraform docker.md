[[Terraform setup]] [[terraform provider]] [[terraform]] [[Terraform workflow]] [[variable file]] [[Terraform CLI]]

# Terraform docker

> Hands-on provider example — same patterns as cloud, without a bill. Framework from **Terraform in Action** (Winkler) + practices from **Terraform: Up & Running** (Brikman).

---

## How it works

Docker is a **non-cloud** [[terraform provider]]. Setup still follows: pin → configure → resource → plan/apply ([[Terraform setup]] · [[Terraform workflow]]).


## Configuration and commands

```shell
terraform init && terraform apply -auto-approve
curl -I http://localhost:8080
terraform destroy -auto-approve
```

| Knob | Why it matters |
|------|----------------|
| Docker daemon up | Provider talks to local socket |
| Image pin (`var.nginx_tag`) | Reproducible pulls |
| Port map | Host 8080 → container 80 |


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Cannot connect to Docker | Daemon / socket perms | Start Docker; fix group/`DOCKER_HOST` |
| Port already allocated | `ss -lptn 'sport = :8080'` | Change `external` port or stop conflict |
| Image pull fail | Network / tag | Fix tag; retry pull |
| Destroy leaves container | State lost | `docker rm` manually; re-import or ignore |
| Provider version mismatch | lock vs constraint | `init -upgrade` intentionally |


## Gotchas

> [!WARNING]
> **Local state only** — fine for learning; teams need remote state ([[Terraform setup]]).

> [!WARNING]
> **docker ≠ production cloud** — patterns transfer; quotas, IAM, and blast radius do not.


## When not to use

- **Real production containers** — use k8s/ECS + CI, not Terraform Docker day-to-day.
- **Learning Linux networking** — compose may teach faster than HCL.


## Why practice with Docker

| Goal | Benefit |
|------|---------|
| Learn HCL + workflow | No AWS/GCP account needed |
| See provider plugins live | Same `init` / lock file behavior |
| Safe destroy loops | Tear down containers freely |

Brikman: learn the tool first; swap provider for a real cloud later.

---


## Minimal project

```txt
terraform-docker/
├── versions.tf
├── providers.tf
├── main.tf
└── variables.tf
```

### versions.tf
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
```

### providers.tf
```hcl
provider "docker" {
  # host defaults to local Docker socket
  # host = "unix:///var/run/docker.sock"
}
```

Same idea as `provider "aws"` — only the plugin changes → [[terraform provider]]

### variables.tf
```hcl
variable "nginx_tag" {
  type        = string
  default     = "1.25-alpine"
  description = "nginx image tag"
}
```

→ [[variable file]]

### main.tf
```hcl
resource "docker_image" "nginx" {
  name = "nginx:${var.nginx_tag}"
}

resource "docker_container" "web" {
  name  = "tf-nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 8080
  }
}
```

Implicit dependency: container references image → correct order (Winkler graph).

---


## Run it

```shell
# Docker daemon must be running
terraform init
terraform plan
terraform apply
curl -I http://localhost:8080
terraform destroy
```

Debug provider issues: `TF_LOG=DEBUG terraform apply` → [[Terraform CLI]]

---


## Map to cloud thinking

| Docker here | Analog on AWS/GCP |
|-------------|-------------------|
| `docker_image` | AMI / container image lookup |
| `docker_container` | EC2 / Cloud Run / GCE VM |
| Local socket auth | IAM / ADC / az identity |
| Local state fine | Move to remote backend for teams ([[Terraform setup]]) |

---


## Book takeaways

- **Winkler**: providers are interchangeable plugins; resources + references define the graph
- **Brikman**: pin versions, use variables, destroy cleanly, graduate to remote state when collaborating
- Core language still: [[terraform]]


## Related

[[Terraform setup]] [[terraform provider]] [[terraform]] [[Terraform workflow]] [[variable file]] [[Terraform CLI]]

## Sources

- [Wikipedia — Terraform docker](https://en.wikipedia.org/wiki/Terraform_docker)
