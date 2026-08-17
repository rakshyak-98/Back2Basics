[[Security]] [[Descriptive]] [[Etherium]]

# GPL (GNU General Public License)

> Copyleft open-source license — distribute derivatives **only** if you provide corresponding source under the same license; understand v2 vs v3 and linking boundaries before shipping products.

```txt
        GPL (GNU General P ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** GPL reviews check copyleft obligations

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [GPL — Wikipedia](https://en.wikipedia.org/wiki/GNU_General_Public_License) — overview

## Technical Details
### Identify GPL in dependency tree

```bash
# Node
npm ls --all 2>/dev/null | rg -i 'gpl|agpl|lgpl'
npx license-checker --summary

# Go
go list -m -json all | jq -r '.Path, .Module.GoVersion'

# Java
./gradlew dependencies | rg -i 'gpl'

# Container image
docker sbom myimage:tag | rg -i 'gpl'
```

### Typical compliance checklist (distribution)

1. Inventory GPL/AGPL components in shipped artifact.
2. Provide **Corresponding Source** (build scripts, lockfiles, instructions).
3. Include LICENSE texts and copyright notices.
4. Document how users obtain source (repository URL, offer for physical media if applicable).
5. Do **not** impose extra restrictions contradicting GPL.

### Safer integration patterns (engineering — not legal advice)

| Pattern | Risk sketch |
|---------|-------------|
| GPL app + proprietary **separate process** (microservice) | Lower coupling — often analyzed as aggregation |
| Static link GPL into proprietary binary | High — usually triggers copyleft |
| Dynamic link LGPL | LGPL conditions — provide relinkable object files |
| SaaS using GPL **without** distributing binary | GPL may not trigger; **AGPL** may |

### Replace or isolate

```bash
# Prefer MIT/Apache-2.0 alternatives when policy forbids copyleft
# Or run GPL component as sidecar with IPC only — document boundary
```

## Mistakes to Avoid
> [!WARNING]
> **AGPL in backend** — SaaS distributing no binaries can still trigger AGPL if users interact with modified AGPL code over network.

> [!WARNING]
> **"Community Edition" ≠ MIT** — marketing name; read `LICENSE` file per component.

> [!WARNING]
> **Vendor `{ "license": "UNLICENSED" }` with GPL deps** — your `package.json` license field doesn't override dependency obligations.

> [!WARNING]
> **Internal use only** — no distribution often means no GPL trigger — but **giving** to customers, contractors, or cloud images may count as distribution.

| Symptom | Check | Fix |
|---------|-------|-----|
| Legal flagged release | SBOM missing GPL | Run license scan in CI; block on AGPL/GPL without approval |
| Can't open-source product module | GPL static link | Swap library; isolate process; or GPL the module (business call) |
| Customer asks for source | GPL component in appliance | Publish source bundle matching exact versions |
| Patent clause concern | GPLv3 vs v2 | Review with counsel; prefer v3 for patent grant clarity |
| MySQL connector confusion | Oracle dual-licensing history | Verify **current** connector license (often GPL v2 with FOSS exception) |

## Pros/Cons or Trade-offs
- **As a substitute for legal review**
- **Assuming LGPL == GPL**
- **Ignoring patents** — GPLv3 addresses patents; v2 does not explicitly.
