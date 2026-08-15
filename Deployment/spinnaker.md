[[DevOps/Jenkins]] [[Github action]] [[Kubernates/kubectl]] [[Docker/Docker compose]]

# Spinnaker

> Multi-cloud continuous delivery control plane — pipelines, optional image bakes, deploy stages, judgments, and rollback — Netflix-style CD.

## Interview Relevance

Interviewers separate CI (build artifact) from CD (promote safely): baking, server groups, manual judgment/canary, and rollback strategy.

## Sources

- [Spinnaker docs](https://spinnaker.io/docs/) — deep-dive
- [Wikipedia — Spinnaker (software)](https://en.wikipedia.org/wiki/Spinnaker_(software)) — overview

## Key Concepts

- **Application / pipeline:** service boundary + DAG of stages.
- **Bake:** immutable AMI/image from base + package (optional).
- **Deploy stage:** rolling/blue-green via cloud drivers (K8s, ASG, etc.).
- **Server group:** homogeneous instances/replicas for a version.
- **Artifact:** versioned image/jar produced by CI and consumed by CD.

## Technical Details

```txt
CI builds image → Spinnaker pipeline
  → Bake (optional)
  → Deploy staging
  → Manual judgment / canary
  → Deploy prod
  → Rollback prior server group / pipeline version
```

| Concept | Meaning |
|---------|---------|
| Clouddriver | Caches cloud state for the UI/API |
| Trigger | Docker tag, Git, cron, webhook |
| Judgment | Human gate before prod |

Spinnaker orchestrates; the cluster executes. Stale Clouddriver cache looks like “UI drift.”

## Real-World Applications

Promote the same container digest staging → prod with a judgment gate and automated rollback hooks.

**Example:** Jenkins builds `api:1.4.2` → Spinnaker deploys to EKS staging → canary → prod.

## Pros/Cons or Trade-offs

- **Pro:** Rich multi-cloud deploy semantics and visibility.
- **Con:** Operationally heavy versus GitHub Actions-only deploys for small teams.

## Comparison

- vs [[Github action]]: Actions often builds and deploys; Spinnaker specializes in progressive delivery control planes.
- vs raw `kubectl apply` in CI: Spinnaker adds inventory, strategies, and gated pipelines.

## Mistakes to Avoid

- Baking mutable “latest” without digest pinning.
- Skipping judgments on prod for high-risk services without automated analysis.
- Debugging only the UI when Clouddriver cache is stale — check cloud APIs directly.
