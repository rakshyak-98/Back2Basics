[[Jenkins]] [[Airflow]] [[Docker compose]] [[Kubernates/kubectl]] [[Terraform workflow]]

# Spinnaker

> Multi-cloud continuous delivery control plane — pipelines, bakes, deploy stages, and rollback — **Netflix OSS CD mental model**.

---

## Mental model

Spinnaker separates **how artifacts are built** (CI: Jenkins, GitHub Actions) from **how they are promoted** (CD: pipelines with gates). A typical flow:

```txt
CI builds image → trigger Spinnaker pipeline
  → Bake (AMI or container) [optional]
  → Deploy to staging (K8s/ECS/ASG/Lambda)
  → Manual judgment / canary analysis
  → Deploy to prod
  → Rollback = run previous pipeline version or disable new server group
```

| Concept | Meaning |
|---------|---------|
| **Application** | Group of services (microservice boundary) |
| **Pipeline** | DAG of stages with triggers |
| **Bake** | Packer-style immutable image from base + package |
| **Deploy stage** | Blue/green or rolling via cloud provider adapter |
| **Server group** | Homogeneous instances (ASG, K8s replica set abstraction) |
| **Artifact** | Docker image, jar, deb — versioned reference from CI |

**Orchestration vs execution:** Spinnaker orchestrates; clusters (EKS, GKE, Titus) execute. Clouddriver caches cloud state — stale cache causes scary UI drift.

---

## Standard config / commands

### Pipeline trigger (Docker → EKS sketch)

```json
{
  "triggers": [{
    "type": "docker",
    "account": "docker-hub",
    "organization": "myorg",
    "repository": "api",
    "tag": "^v.*"
  }],
  "stages": [
    { "type": "deploy", "account": "eks-staging", "cloudProvider": "kubernetes", "manifestArtifactId": "k8s-manifest" },
    { "type": "manualJudgment", "judgmentInputs": ["Proceed to prod"] },
    { "type": "deploy", "account": "eks-prod", "cloudProvider": "kubernetes" }
  ]
}
```

### Common stages

```txt
Bake (AWS)     — ami from package + base AMI
Deploy (ASG)   — create new ASG, attach LB, shrink old (blue/green)
Run Job (K8s)  — migration Job before traffic shift
Canary         — Kayenta metrics comparison (Prometheus/Datadog)
Webhook        — notify Slack/PagerDuty
Rollback       — redeploy last known good artifact pin
```

### Ops CLI (gate / spin)

```shell
# Halyard (legacy install) or Operator — version-dependent
spin pipeline list --application myapp
spin pipeline execute --name deploy-prod --application myapp

# UI: Applications → Pipelines → Executions — source of truth for audits
```

### When Spinnaker vs Argo

| Factor | Spinnaker | Argo CD / Rollouts |
|--------|-----------|-------------------|
| Multi-cloud ASG/Lambda | Strong | K8s-centric |
| Complex promotion DAG | Native pipelines | Argo Workflows / separate CI |
| GitOps desired state | Secondary (pipeline-driven) | Primary (manifest in Git) |
| Ops burden | Heavy (multiple microservices) | Lighter for K8s-only shops |
| Canary analysis | Kayenta built-in | Argo Rollouts + AnalysisTemplate |

**Rule of thumb:** K8s-only + GitOps → **Argo**. Multi-cloud + legacy VM/ASG + rich pipelines → **Spinnaker**. Many teams: **Actions/Jenkins CI + Argo CD** and skip Spinnaker entirely.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pipeline not triggering | Trigger config; artifact regex; CI webhook | Match tag pattern; verify echo/delivery config |
| Deploy stuck "in progress" | Clouddriver logs; cloud quota | Kill stuck stage; refresh cache; fix IAM |
| Wrong version deployed | Artifact pin vs `:latest` | Immutable tags; forbid floating latest in prod |
| Rollback didn't revert | Deployed new server group still receiving traffic | Disable bad group; verify LB weights |
| Bake fails | Packer logs in Rosco | Base AMI deprecated; region mismatch |
| UI shows phantom resources | Cache stale | `curl` cache refresh API; clouddriver pod restart |
| K8s manifest stage error | Artifact compression; account kubeconfig | Validate manifest locally with kubectl |

```shell
kubectl -n spinnaker logs deploy/clouddriver --tail=200
kubectl -n spinnaker logs deploy/orca --tail=200
```

---

## Gotchas

> [!WARNING]
> **`:latest` in prod** — rollback impossible to reason about; pin digest/tag.

> [!WARNING]
> **Manual judgment as only gate** — human fatigue; add metrics canary or automated policy.

> [!WARNING]
> **Pipeline copy drift** — 20 near-duplicate pipelines; extract shared templates (Dhall/Jsonnet).

> [!WARNING]
> **Spinnaker HA complexity** — Redis, S3 front50, DB orca — backup and upgrade planning required.

> [!WARNING]
> **IAM too broad** — clouddriver creds with `*` — blast radius on compromise.

---

## When NOT to use

- **Single small K8s cluster** — Argo CD + Helm sufficient.
- **Serverless-only, few functions** — CI deploy per function adequate.
- **Team without dedicated platform ops** — Spinnaker maintenance will stall feature work.

---

## Related

[[Jenkins]] [[Airflow]] [[Docker compose]] [[kubectl]] [[Terraform workflow]]
