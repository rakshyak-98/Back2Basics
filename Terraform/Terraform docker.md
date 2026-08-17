[[Terraform setup]] [[terraform provider]] [[terraform]] [[Terraform workflow]] [[variable file]] [[Terraform CLI]]

# Terraform docker

> Practice Terraform against the local Docker provider — same init/plan/apply patterns as cloud, without a cloud bill.

```txt
        Terraform docker ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers like Docker-provider demos to prove you understand providers, im…

## Sources
- [kreuzwerkel/docker provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs) — deep-dive
- Scott Winkler, *Terraform in Action* — overview
- Yevgeniy Brikman, *Terraform: Up & Running* — overview

## Key Concepts
- **Non-cloud provider:** still pin → configure → resource → plan/apply.
- **Implicit graph:** container references image ID → correct create order.
- **Local state OK for learning;:** teams need remote state later.
- **Patterns transfer; blast radius does not:** — Docker ≠ production cloud quotas/IAM.

## Technical Details
```txt
terraform-docker/
├── versions.tf
├── providers.tf
├── main.tf
└── variables.tf
```

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

provider "docker" {
  # host = "unix:///var/run/docker.sock"
}

variable "nginx_tag" {
  type        = string
  default     = "1.25-alpine"
  description = "nginx image tag"
}

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

```shell
terraform init && terraform apply -auto-approve
curl -I http://localhost:8080
terraform destroy -auto-approve
TF_LOG=DEBUG terraform apply
```

| Knob | Why it matters |
|------|----------------|
| Docker daemon up | Provider talks to local socket |
| Image pin (`var.nginx_tag`) | Reproducible pulls |
| Port map | Host 8080 → container 80 |

| Docker here | Analog on AWS/GCP |
|-------------|-------------------|
| `docker_image` | AMI / container image lookup |
| `docker_container` | EC2 / Cloud Run / GCE VM |
| Local socket auth | IAM / ADC / az identity |
| Local state fine | Move to remote backend for teams |

| Symptom | Check | Fix |
|---------|-------|-----|
| Cannot connect to Docker | Daemon / socket perms | Start Docker; fix group/`DOCKER_HOST` |
| Port already allocated | `ss -lptn 'sport = :8080'` | Change `external` port or stop conflict |
| Image pull fail | Network / tag | Fix tag; retry pull |
| Destroy leaves container | State lost | `docker rm` manually; re-import or ignore |
| Provider version mismatch | lock vs constraint | `init -upgrade` intentionally |

## Mistakes to Avoid
- **Mistake:** Treating local Docker Terraform as a production orchestrator
- **Mistake:** Losing state and assuming `destroy` cleaned host containers
- **Mistake:** Unpinned image tags in learning projects that later become “prod…

## Pros/Cons or Trade-offs
- **Pro:** Fast, free feedback on Terraform mechanics.
- **Con:** Not how you run production containers day-to-day (prefer k8s/ECS + CI).
- **Con:** Compose may teach Linux networking faster than HCL for that narrow goal.

## Comparison
- Same plugin pattern as [[terraform provider]]
- Core language still [[terraform]].


### Use cases
- Onboarding engineers to HCL without cloud accounts

- **Example:** Apply nginx on `:8080`, curl it, destroy
