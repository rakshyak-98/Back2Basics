[[Terraform setup]] [[terraform]] [[Terraform workflow]] [[variable file]] [[helm]] [[ecommerce-platform-architecture]] [[ecommerce-cicd-environments]] [[ingress]] [[AWS ECR]] [[Kubernetes services]] [[Route53]]

# ecommerce eks layout

> Split e-commerce infra so Terraform owns cloud (VPC, EKS, RDS, MSK, ECR, IAM) per environment state, while Helm/GitOps owns workloads — one state per env, reusable modules.

```txt
        ecommerce eks layo ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers look for blast-radius-aware state splits, Terraform↔Helm handoff…

## Sources
- [AWS — EKS best practices](https://aws.github.io/aws-eks-best-practices/) — overview
- [Argo CD — Declarative GitOps](https://argo-cd.readthedocs.io/) — overview
- Yevgeniy Brikman, *Terraform: Up & Running* (env/module layout) — deep-dive

## Key Concepts
- **Terraform owns:** network, cluster, databases, broker, IAM.
- **Helm owns:** Deployments/Rollouts, HPA, ConfigMaps; **Argo CD** syncs releases.
- **One state per env:** (`dev`/`test`/`staging`/`prod`)
- **Handoff:** Terraform outputs (IRSA ARNs, endpoints) become Helm values / External Secret…

## Technical Details
```txt
terraform/
  environments/     # one state per env
    └── eks, vpc, rds, msk, ecr, iam
  modules/          # reusable infra slices

helm/
  charts/
    platform/       # ingress, external-secrets, argo-rollouts
    services/       # one chart per microservice (+ _common library)
```

| Env | EKS cluster name | Namespace(s) | State key (S3) |
|-----|------------------|--------------|----------------|
| dev | `commerce-dev` | `dev` | `dev/infra/terraform.tfstate` |
| test | `commerce-test` | `test`, `test-pr-*` | `test/infra/terraform.tfstate` |
| staging | `commerce-staging` | `staging` | `staging/infra/terraform.tfstate` |
| production | `commerce-prod` | `prod` | `prod/infra/terraform.tfstate` |
| live (slice) | `commerce-prod` (same) | `live-canary` | no extra state — Helm only |

- **Node pools (production):** `system` (tainted

```txt
infra/
├── modules/   # vpc, eks (+ irsa), rds, elasticache, msk, ecr, alb-ingress, secrets, observability
├── environments/{dev,test,staging,prod}/  # main.tf, tfvars, backend.tf, versions, providers
└── global/iam-github-oidc/
```

| Module | Owns | Does not own |
|--------|------|--------------|
| `vpc` | CIDR, subnets, NAT, endpoints | Service pods |
| `eks` | Cluster, node pools, IRSA OIDC | Application Helm releases |
| `rds` | Instance, backups, parameter group | Schema migrations (app Job) |
| `msk` | Brokers, topics (optional) | Consumer groups |
| `ecr` | Repository + lifecycle | Image build (CI) |
| `alb-ingress` | ALB, WAF association | Per-service Ingress rules (Helm) |

```hcl
module "vpc" {
  source = "../../modules/vpc"
  env    = var.env
  cidr   = var.vpc_cidr
}

module "eks" {
  source     = "../../modules/eks"
  env        = var.env
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
}

module "rds_payment" {
  source         = "../../modules/rds"
  identifier     = "${var.env}-payment"
  instance_class = var.rds_payment_class
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.db_subnet_ids
}

module "irsa_payment" {
  source           = "../../modules/irsa-service"
  cluster_oidc_arn = module.eks.oidc_provider_arn
  service_account  = "payment"
  namespace        = var.k8s_namespace
  policy_arns      = [module.secrets.read_policy_arn]
}
```

- Helm: library chart `_common` + per-service charts

| Concern | Terraform → Helm |
|---------|------------------|
| EKS endpoint | Argo CD cluster secret |
| IRSA role ARN | `serviceAccount.annotations` |
| RDS / MSK | ExternalSecret / ConfigMap via ESO |
| ECR repo URL | `image.repository` |
| ALB hostname | Ingress / Route53 |

```bash
cd infra/environments/dev
terraform init && terraform plan && terraform apply
helm template payment deploy/helm/charts/services/payment \
  -f deploy/helm/values/staging/payment.yaml
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Pod `AccessDenied` Secrets | IRSA annotation vs Terraform role | Align SA name, namespace, trust policy |
| Helm upgrade loop | CRD / Rollout conflict | Separate platform chart upgrade window |
| RDS connection storm | Too many pods, no pooling | PgBouncer or RDS Proxy in Terraform module |
| Wrong cluster deploy | Argo CD destination | `destination.server` + namespace guardrails |
| State lock | [[Terraform workflow]] | `force-unlock` after confirming no run |

## Mistakes to Avoid
- **Mistake:** One mega Terraform root for everything
- **Mistake:** Copy-pasting Deployment YAML eight times — use a library chart
- **Mistake:** `live-canary` without NetworkPolicy / MSK ACL prefixes
- **Mistake:** Sharing production secrets across env tfvars
- **Mistake:** Pinning images with `:latest` in prod values

## Pros/Cons or Trade-offs
- **Pro:** Clear ownership boundaries and per-env blast radius.
- **Con:** More repos/paths to learn than a single root.
- **Con:** Coupling MSK+RDS+EKS in one module makes destroy dangerous — use `prevent_destroy` on prod data.

## Comparison
- Local-only → [[Terraform docker]] + Compose until integration env needed.
- ECS instead of EKS → swap `modules/eks` for ECS/Fargate; Helm becomes task definitions.
- Platform architecture context → [[ecommerce-platform-architecture]] · [[ecommerce-cicd-environmen…


### Use cases
- Multi-env commerce platforms on EKS with GitOps deploys and flash-sale node p…

- **Example:** `prod` Terraform creates `prod-payment-irsa`
