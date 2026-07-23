[[Security]] [[Descriptive]]

# GPL (GNU General Public License)

> Copyleft open-source license — distribute derivatives **only** if you provide corresponding source under the same license; understand v2 vs v3 and linking boundaries before shipping products.

## Mental model

GPL grants use, modify, and redistribute rights with a ** reciprocity obligation**: if you distribute a GPL-covered **combined work**, recipients get source and GPL freedoms.

```
Your app ──links/includes──► GPL library
                │
                ▼
     Combined work? ──YES──► must GPL your distributed code + provide source
                │
                NO (mere aggregation) ──► your app license unchanged
```

**Community Edition** servers (MySQL CE historically, many forks) often ship under GPL — using them as **separate processes** vs **linked libraries** changes compliance posture. Legal interpretation varies — escalate to counsel for product decisions.

Versions:
- **GPLv2** — no explicit patent grant; "system library" exception wording differs.
- **GPLv3** — explicit patent license; anti-tivoization; compatible with Apache 2.0 in some combinations.

Related licenses: **LGPL** (weaker copyleft — dynamic link boundary), **AGPL** (network use triggers source obligation).

## Standard config / commands

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
4. Document how users obtain source (repo URL, offer for physical media if applicable).
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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Legal flagged release | SBOM missing GPL | Run license scan in CI; block on AGPL/GPL without approval |
| Can't open-source product module | GPL static link | Swap library; isolate process; or GPL the module (business call) |
| Customer asks for source | GPL component in appliance | Publish source bundle matching exact versions |
| Patent clause concern | GPLv3 vs v2 | Review with counsel; prefer v3 for patent grant clarity |
| MySQL connector confusion | Oracle dual-licensing history | Verify **current** connector license (often GPL v2 with FOSS exception) |

## Gotchas

> [!WARNING]
> **AGPL in backend** — SaaS distributing no binaries can still trigger AGPL if users interact with modified AGPL code over network.

> [!WARNING]
> **"Community Edition" ≠ MIT** — marketing name; read `LICENSE` file per component.

> [!WARNING]
> **Vendor `{ "license": "UNLICENSED" }` with GPL deps** — your `package.json` license field doesn't override dependency obligations.

> [!WARNING]
> **Internal use only** — no distribution often means no GPL trigger — but **giving** to customers, contractors, or cloud images may count as distribution.

## When NOT to use

- **As a substitute for legal review** — this note orients engineers; compliance sign-off is legal/compliance team.
- **Assuming LGPL == GPL** — LGPL has different linking rules; read the actual license text.
- **Ignoring patents** — GPLv3 addresses patents; v2 does not explicitly.

## Related

[[Security]] [[Descriptive]] [[Etherium]]
