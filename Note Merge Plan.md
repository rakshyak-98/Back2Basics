[[INDEX]] [[Similar Notes — Cluster Map]] [[README]] [[general]]

# Note Merge Plan

> Which topics merge into one canonical note, which stay separate, and where each domain keeps its CLI reference.

---

## Policy

1. **One file per topic** — merge true duplicates (case, typo, path, or numbered variants) into a single canonical note; leave a redirect stub (`→ [[Canonical]]`) at the old path.
2. **CLI stays separate** — each major domain gets one **CLI reference** file with commands grouped under cluster headings; deep-dive leaf notes remain linked from the CLI file.
3. **Do not merge** cross-domain homonyms (`Configuration` for Nginx vs MySQL), related-but-distinct concepts (symmetric vs asymmetric encryption), or library vs protocol notes (`uWebSocket` vs `webSocket`).

---

## Executed merges (canonical ← redirect)

| Canonical note | Merged / redirected sources | Reason |
|----------------|----------------------------|--------|
| [[Encryption]] | [[Asymmetrical Encryption]], [[symmetrical encryption]] | Single crypto reference |
| [[React State management]] | [[React data management]] | Unified client + server state architecture |
| [[connection pooling]] | [[Connection Pool]] (LLD) | App pool + LLD design in one note |
| [[Blocking Vs Non-Blocking]] | [[non-blocking]] | Combined I/O models |
| [[MySQL Triggers]] | `mysql triggers` | Case duplicate |
| [[mysql partitioning]] | `Database/mysql partitioning` (parent path) | Same topic, two paths |
| [[systemctl]] | `Linux/management/systemctl` | Same topic, two paths |
| [[Abstract Factory]] | `Abstract Factor` | Typo stub |
| [[MySQL Engines]] | `mysql engine` | Case duplicate |
| [[EventEmitter]] | `event emitter` | Case duplicate |
| [[web workers]] | `web worker` | Plural canonical |
| [[Compound Components]] | `Compound Components 1` | Numbered duplicate |
| [[MySQL Events]] | `mysql events 1` | Numbered duplicate |
| [[mail server]] | `E mail server` | Spacing duplicate |
| [[AWS EBS(Elastic Block Store)]] | `EBS (Elastic Block Store)` | Title duplicate |
| [[data fetching component]] | `Data Fetching HOC component` | Same React pattern |
| [[MBR]] | `MBR(Master Boot Record)` | Abbrev vs full name |
| [[GitHub CLI]] | `Github cli (2)` | Redirect stub |
| [[NodeJS CLI]] | `node command`, `npm command` | Folded into domain CLI |

All canonical notes above have been **rewritten** with full topic explanations and one-line descriptions on every external link.

---

## Per-cluster CLI files (one CLI per domain)

| Domain | CLI file | Cluster headings |
|--------|----------|------------------|
| Linux | [[Linux CLI]] | Shell & daily ops · Process · Networking · Services · Users · Files · Packages |
| Docker | [[Docker CLI]] | Build · Run · Inspect · Network · Volumes · Compose |
| Git | [[Git CLI]] | Recovery · bisect · merge dry-run |
| Node.js | [[NodeJS CLI]] | Node runtime · npm |
| npm / pnpm | [[npm CLI]] | pnpm · npm |
| MySQL | [[MySQL CLI]] | mysql client |
| PostgreSQL | [[psql essential]] | *(topic note — no separate CLI yet)* |
| AWS | [[AWS CLI]] | Commands · Installation |
| Terraform | [[Terraform CLI]] | init/plan/apply/state |
| Go | [[Go CLI]] | mod · build · test |
| Helm | [[Helm CLI]] | repo · install · upgrade |
| Redis | [[Redis CLI]] | connect · INFO · memory · SCAN |
| Flutter | [[Flutter CLI]] | devices · run · build · pub |
| GitHub | [[GitHub CLI]] | auth · PR · secrets |
| Kubernetes | [[kubectl CLI]] | context · workloads · debug |
| Apache | [[Apache CLI]] | modules · sites · configtest |
| Vim | [[Vim CLI]] | command-mode · ex |
| Neovim | [[Neovim CLI]] | command-mode |
| Deployment | [[Deployment CLI]] | Vercel · Render |

Regenerate CLI aggregates: `python3 scripts/consolidate_vault.py`

---

## Recommended merges (not yet done — review first)

| Pair | Recommendation |
|------|----------------|
| [[SQL normalization]] / [[mysql normalization]] | Keep mysql-specific under [[mysql normalization]]; link from general SQL note |
| [[mysql]] / [[mysql2]] | **Do not merge** — driver vs database |
| [[network managmeen]] / [[network management]] | **Do not merge** — NetworkManager typo note vs streaming ops |
| [[name server]] / [[ACME server]] | **Do not merge** — different roles |

---

## Basename collisions (renamed, not merged)

| Old basename | Resolution |
|--------------|------------|
| `cli` (helm, mysql, NodeJS, Linux) | Renamed to `Helm CLI`, `MySQL CLI`, `NodeJS CLI`; Linux keeps [[CLI]] as concept hub + [[Linux CLI]] for commands |
| `commands` (Linux, nvim) | `Linux/Commands.md` hub + `nvim/Neovim CLI.md` |
| `Configuration` (mysql, Nginx) | **Keep both** — disambiguate by folder in wikilinks |
| `python` (Errors, Python) | **Keep both** — rename candidate: `Errors/Python.md` → `python-errors.md` |

---

## Domain topic clusters (keep as separate leaf notes)

These are **related** but should **not** merge into one file — link via hub + CLI instead:

- **Linux/commands/** — 50+ per-binary leaves (grep, ss, dig, …) linked from [[Linux CLI]] and [[Commands]]
- **GIT/** — workflow leaves (`git rebase`, `git merge`, …) linked from [[Git CLI]]
- **Design pattern/** — one note per pattern (GoF), not one mega-file
- **Streaming/** — protocol leaves (HLS, DASH, RTMP, …) anchored by [[Streaming]] hub
- **React/** — hooks, state, architecture leaves anchored by [[React Architecture]]

---

## Next steps

1. Review [[Similar Notes — Cluster Map]] likely-duplicate pairs table.
2. Run `python3 scripts/consolidate_vault.py` after adding new merges to `MERGES` in that script.
3. Fill placeholder sections in consolidated CLI files from leaf notes as needed.
4. Rename `Errors/Python.md` → `python-errors.md` to clear basename collision.
