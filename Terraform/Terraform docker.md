[[Terraform setup]] [[terraform provider]] [[terraform]] [[Terraform workflow]] [[variable file]] [[Terraform CLI]]

# Terraform docker

> Hands-on provider example — same patterns as cloud, without a bill. Framework from **Terraform in Action** (Winkler) + practices from **Terraform: Up & Running** (Brikman).

Docker is a **non-cloud** [[terraform provider]]. Setup still follows: pin → configure → resource → plan/apply ([[Terraform setup]] · [[Terraform workflow]]).

---

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
