<!-- note-strategy: operational -->
[[AWS]] [[AWS EC2]] [[EBS (Elastic Block Store)]] [[AWS EBS(Elastic Block Store)]]

# AMI (Amazon Machine Image)

> AMI — the disk template you pick to boot an EC2 instance (OS + root volume snapshot + launch permissions).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Launch = AMI + instance type + network. The AMI points at EBS snapshots (root ± data). AMIs are **region-scoped**; copy to use elsewhere.

```txt
Customize EC2 → Create image → AMI (snapshots)
                              │
                    Launch more instances from AMI
```

| Source | When |
|--------|------|
| AWS / Marketplace | Stock OS or vendor stacks |
| Your “golden” AMI | Baked packages, agents, hardening |
| CopyImage | DR / multi-region |

---

## Standard config / commands

```bash
# Register from instance (console or)
aws ec2 create-image --instance-id i-… --name "app-golden-$(date +%F)" --no-reboot

aws ec2 describe-images --owners self --query 'Images[*].[ImageId,Name,State]' --output table
aws ec2 copy-image --source-region us-east-1 --source-image-id ami-… --name "app-eu" --region eu-west-1

aws ec2 run-instances --image-id ami-… --instance-type t3.small --subnet-id subnet-… …
```

| Knob | Why it matters |
|------|----------------|
| `--no-reboot` vs reboot | Consistency of filesystem at snapshot time |
| Launch permissions | Private vs shared accounts / public (careful) |
| Block device mappings | Extra volumes, delete-on-termination |
| Deprecation / tags | Track which AMI is prod-current |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `InvalidAMIID.NotFound` | Wrong region | Switch region or CopyImage |
| Instance fails status checks after bake | Cloud-init / sshd broken in AMI | Fix on source; re-create image |
| Huge AMI / slow launch | Bloated root; many layers of junk | Slim bake; delete unused packs |
| Marketplace AMI billing surprise | Product code on AMI | Read marketplace terms; prefer own bake |
| Can’t share AMI | Snapshot perms | Share snapshots + AMI with target account |
| Old AMI in ASG | Launch template pinned | Update LT/version; instance refresh |

---

## Gotchas

> [!WARNING]
> **Secrets in AMI** — baked keys leak to every launch; use instance roles + SSM Parameter/Secrets Manager.

> [!WARNING]
> **Region lock** — `ami-abc` in us-east-1 ≠ same id elsewhere after copy.

> [!WARNING]
> **Delete-on-termination** — root mapping can wipe data on terminate; know your LT settings.

---

## When NOT to use

- **Immutable containers only** — prefer ECR images + ECS/EKS; AMI is just the node OS.
- **One-off debug box** — launch stock Amazon Linux; don’t bake an AMI for every experiment.
- **Windows + Linux mix as one AMI** — separate images per OS.

---

## Related

[[AWS EC2]] [[EBS (Elastic Block Store)]] [[AWS EBS(Elastic Block Store)]] [[IAM]] [[AWS Networking]]
