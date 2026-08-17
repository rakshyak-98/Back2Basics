[[DevOps/Jenkins]] [[Github action]] [[Kubernates/kubectl]] [[Docker/Docker compose]]

# Spinnaker

> Multi-cloud continuous delivery control plane — pipelines, optional image bakes, deploy stages, judgments, and rollback — Netflix-style CD.

```txt
        Spinnaker ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers separate CI (build artifact) from CD (promote safely): baking, s…

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

- Spinnaker orchestrates; the cluster executes.
- Stale Clouddriver cache looks like “UI drift.”

## Mistakes to Avoid
- **Mistake:** Baking mutable “latest” without digest pinning
- **Mistake:** Skipping judgments on prod for high-risk services without automa…
- **Mistake:** Debugging only the UI when Clouddriver cache is stale

## Pros/Cons or Trade-offs
- **Pro:** Rich multi-cloud deploy semantics and visibility.
- **Con:** Operationally heavy versus GitHub Actions-only deploys for small teams.

## Comparison
- vs [[Github action]]: Actions often builds and deploys
- vs raw `kubectl apply` in CI: Spinnaker adds inventory, strategies, and gated pipelines.


### Use cases
- Promote the same container digest staging → prod with a judgment gate and aut…

- **Example:** Jenkins builds `api:1.4.2` → Spinnaker deploys to EKS staging → …
