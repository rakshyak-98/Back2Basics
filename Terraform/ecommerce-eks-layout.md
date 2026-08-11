[[Terraform setup]] [[terraform]] [[Terraform workflow]] [[variable file]] [[helm]] [[ecommerce-platform-architecture]] [[ecommerce-cicd-environments]] [[ingress]] [[AWS ECR]]

# ecommerce eks layout

> ecommerce eks layout — environments/ # one state per env (dev, test, staging, prod)

---

## Mental model

```txt
terraform/
  environments/     # one state per env (dev, test, staging, prod)
    └── eks, vpc, rds, msk, ecr, iam
  modules/          # reusable infra slices

helm/
  charts/
    platform/       # ingress, external-secrets, argo-rollouts
    services/       # one chart per microservice (+ order)
```

**Terraform owns** cloud resources (network, cluster, databases, broker, IAM). **Helm owns** workload manifests (Deployments, HPA, Rollouts, ConfigMaps). **GitOps** (Argo CD) syncs Helm releases from environment branches or OCI chart versions.

---

## Standard config / commands

```bash
cd live/dev
terraform init
terraform plan
terraform apply
```

## AWS / cluster strategy

| Env | EKS cluster name | Namespace(s) | State key (S3) |
|-----|------------------|--------------|----------------|
| dev | `commerce-dev` | `dev` | `dev/infra/terraform.tfstate` |
| test | `commerce-test` | `test`, `test-pr-*` | `test/infra/terraform.tfstate` |
| staging | `commerce-staging` | `staging` | `staging/infra/terraform.tfstate` |
| production | `commerce-prod` | `prod` | `prod/infra/terraform.tfstate` |
| live (slice) | `commerce-prod` (same) | `live-canary` | no extra state — Helm only |

**Account layout:** `commerce-dev` (development+test optional), `commerce-staging`, `commerce-prod` — separate IAM boundaries per [[ecommerce-cicd-environments]].

**Node pools (production example):**
- `system` — tainted; ingress, CoreDNS, Argo
- `general` — app microservices
- `promotions-burst` — optional pool with higher max for flash sales (scale via Karpenter or CA)

---

## Sample Terraform directory structure

```txt
infra/
├── README.md
├── modules/
│   ├── vpc/
│   │   ├── main.tf          # subnets, NAT, flow logs
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   │   ├── main.tf          # cluster, OIDC, node groups / Karpenter
│   │   ├── irsa.tf          # pod identity roles per service
│   │   └── outputs.tf
│   ├── rds/
│   │   ├── main.tf          # Postgres (per-service DB or shared cluster + schemas)
│   │   └── outputs.tf
│   ├── elasticache/
│   │   └── main.tf          # Redis replication group
│   ├── msk/
│   │   └── main.tf          # Kafka (or managed alternative module)
│   ├── documentdb/          # optional — Mongo-compatible for catalog blobs / notifications
│   │   └── main.tf
│   ├── ecr/
│   │   └── main.tf          # repos per service — [[AWS ECR]]
│   ├── alb-ingress/
│   │   └── main.tf          # ALB + [[ingress]] controller IAM
│   ├── secrets/
│   │   └── main.tf          # Secrets Manager paths per env
│   └── observability/
│       └── main.tf          # CloudWatch, AMP, X-Ray optional
├── environments/
│   ├── dev/
│   │   ├── main.tf          # module calls
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   ├── backend.tf       # key = dev/infra/terraform.tfstate
│   │   ├── versions.tf
│   │   └── providers.tf
│   ├── test/
│   │   └── ...              # same layout
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
└── global/
    └── iam-github-oidc/     # CI deploy roles — one module, separate roles per env
        └── main.tf
```

### Module boundary rules

| Module | Owns | Does not own |
|--------|------|--------------|
| `vpc` | CIDR, subnets, NAT, VPC endpoints | Service pods |
| `eks` | Cluster, node pools, IRSA OIDC provider | Application Helm releases |
| `rds` | Instance, backups, parameter group | Schema migrations (app Job) |
| `msk` | Brokers, topics (optional — or topics via app/terraform kafka provider) | Consumer groups |
| `ecr` | Repository + lifecycle policy | Image build (CI) |
| `alb-ingress` | ALB, WAF association | Per-service Ingress rules (Helm) |

### Environment `main.tf` sketch

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
  source             = "../../modules/rds"
  identifier         = "${var.env}-payment"
  instance_class     = var.rds_payment_class
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.db_subnet_ids
}

# IRSA: payment service → Secrets Manager + RDS IAM auth optional
module "irsa_payment" {
  source            = "../../modules/irsa-service"
  cluster_oidc_arn  = module.eks.oidc_provider_arn
  service_account   = "payment"
  namespace         = var.k8s_namespace
  policy_arns       = [module.secrets.read_policy_arn]
}
```

Pin versions per [[Terraform setup]] — separate `terraform.tfvars` per environment; never share production secrets.

---

## Sample Helm directory structure

```txt
deploy/
├── helm/
│   ├── charts/
│   │   ├── platform/
│   │   │   ├── argo-rollouts/       # controller + AnalysisTemplates
│   │   │   ├── external-secrets/    # ClusterSecretStore per account
│   │   │   ├── ingress-nginx/       # or AWS LB Controller chart wrapper
│   │   │   └── kafka-ui/            # non-prod only
│   │   └── services/
│   │       ├── _common/             # library chart (templates partials)
│   │       │   ├── templates/
│   │       │   │   ├── _deployment.tpl
│   │       │   │   ├── _hpa.tpl
│   │       │   │   ├── _service.tpl
│   │       │   │   └── _servicemonitor.tpl
│   │       │   └── Chart.yaml       # type: library
│   │       ├── order/
│   │       ├── payment/
│   │       ├── refund/
│   │       ├── notification/
│   │       ├── promotions/
│   │       ├── catalog/
│   │       ├── pricing/
│   │       ├── vendor/
│   │       └── customer/
│   └── values/
│       ├── dev/
│       │   ├── payment.yaml
│       │   └── catalog.yaml
│       ├── test/
│       ├── staging/
│       └── prod/
│           ├── payment.yaml
│           └── catalog.yaml
├── argocd/
│   ├── apps/
│   │   ├── dev-payment.yaml         # Application CR → path + values
│   │   └── prod-payment-rollout.yaml
│   └── app-of-apps.yaml
└── kustomize/                       # optional overlays per env
    └── prod/
        └── payment/
            └── kustomization.yaml
```

### Per-service chart contents

Each `services/<name>/` chart typically includes:

```txt
Chart.yaml
values.yaml          # defaults
templates/
  deployment.yaml    # or rollout.yaml for payment/order on prod
  service.yaml
  hpa.yaml
  pdb.yaml
  ingress.yaml       # only if edge-exposed (rare — prefer gateway)
  serviceaccount.yaml  # IRSA annotation
  configmap.yaml
  externalsecret.yaml
  servicemonitor.yaml
```

**Rollout versus Deployment:** payment, order, catalog use **Argo Rollout** in production/live; development uses simple Deployment.

### Values layering example (`payment` prod)

```yaml
# helm/values/prod/payment.yaml
image:
  repository: 123456789012.dkr.ecr.us-east-1.amazonaws.com/commerce/payment
  digest: sha256:abc...   # pinned by CD — not :latest

replicaCount: 4
resources:
  requests: { cpu: 500m, memory: 512Mi }
  limits:   { cpu: 2000m, memory: 1Gi }

autoscaling:
  enabled: true
  minReplicas: 4
  maxReplicas: 20
  metrics:
    - type: Pods
      pods:
        metric: { name: kafka_consumer_lag }
        target: { type: AverageValue, averageValue: "1000" }

rollout:
  enabled: true
  steps:
    - setWeight: 5
    - pause: { duration: 30m }
    - setWeight: 25
    - pause: { duration: 2h }
    - setWeight: 100

serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/prod-payment-irsa

env:
  KAFKA_TOPIC_PREFIX: prod.
  PSP_MODE: live

externalSecrets:
  - name: payment-secrets
    keys: [PSP_API_KEY, DATABASE_URL]
```

---

## Terraform ↔ Helm handoff

| Concern | Terraform output → Helm input |
|---------|-------------------------------|
| EKS cluster endpoint | Argo CD cluster secret |
| IRSA role ARN | `serviceAccount.annotations` in values |
| RDS endpoint | ExternalSecret / Secrets Manager key |
| MSK bootstrap brokers | ConfigMap via ESO |
| ECR repo URL | `image.repository` in values |
| ALB hostname | Ingress annotation or Route53 [[Route53]] record |

Use **External Secrets Operator** — Terraform creates Secrets Manager entries; Helm only references keys.

---

## CI integration touchpoints

| Step | Path |
|------|------|
| `terraform plan` | `infra/environments/<env>` on path filter `infra/**` |
| Image push | Updates values digest or Argo CD Image Updater |
| Helm template test | `helm template payment deploy/helm/charts/services/payment -f deploy/helm/values/staging/payment.yaml` |
| Deploy | Argo CD sync or `helm upgrade` from [[Github action]] |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pod `AccessDenied` Secrets | IRSA annotation vs Terraform role | Align SA name, namespace, trust policy |
| Helm upgrade loop | CRD / Rollout conflict | Separate platform chart upgrade window |
| RDS connection storm | Too many pods, no [[connection pooling]] | PgBouncer sidecar or RDS Proxy in Terraform module |
| Wrong cluster deploy | Argo CD destination | `destination.server` + namespace guardrails |
| State lock | [[Terraform workflow]] | `terraform force-unlock` after confirming no run |

---

## Gotchas

> [!WARNING]
> **One mega Terraform root** — blast radius; split state: `network`, `eks`, `data` per env.

> [!WARNING]
> **Helm chart copying Deployment yaml eight times** — use library chart `_common` templates.

> [!WARNING]
> **MSK + RDS in same module as EKS** — coupling; harder to destroy dev without wiping data — use `prevent_destroy` on prod data modules.

> [!WARNING]
> **live-canary namespace without NetworkPolicy** — canary talks to prod Kafka topics — enforce `prod.` prefix ACLs on MSK.

---

## When NOT to use

- **Local/docker-compose only** — use [[Terraform docker]] + compose for development; skip EKS module until integration environment needed.
- **ECS instead of EKS** — replace `modules/eks` with ECS/Fargate module; Helm section becomes task definitions.

---

## Related

[[Terraform setup]] · [[terraform]] · [[variable file]] · [[helm]] · [[cli]] · [[ingress]] · [[Kubernetes services]] · [[ecommerce-platform-architecture]] · [[ecommerce-cicd-environments]] · [[AWS ECR]] · [[Route53]]
