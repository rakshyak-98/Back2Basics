[[INDEX]] [[README]] [[staff engineer]] [[we]] [[AGENTS.md]]

# general

> Vault entry hub — where to start in Back2Basics, how notes are written, and what this collection is for.

```txt
        general ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Not a classic review topic

## Sources
- Vault: [[README]] — overview
- Vault: [[AGENTS.md]] — overview (agent editing guide)

## Key Concepts
- **Symptom routing:** Start at [[INDEX]], not random folder browsing.
- **Hubs:** Domain roots route to leaves; avoid duplicating deep content here.
- **Mission:** Force-multiply under incident pressure ([[we]], [[staff engineer]]).


- **Core:** **Back2Basics** is a staff-engineer field notebook: fast retrieval for debug …

## Technical Details
```txt
Symptom / design question
        ↓
    [[INDEX]]  (routing table)
        ↓
    Domain note  (summary + links + actionable detail)
        ↓
    Fix / configure / decide
```

| Need | Go to |
|------|-------|
| Symptom → note | [[INDEX]] |
| Vault overview | [[README]] |
| Staff skill model | [[staff engineer]] |
| Agent / cloud editing | [[AGENTS.md]] |
| Mission statement | [[we]] |

| Domain | Hub |
|--------|-----|
| Linux & OS | [[Linux]] · [[Operating System]] |
| Networking | [[Networking]] · [[DNS]] · [[Protocol]] |
| Containers | [[Docker]] · [[Kubernates]] |
| Data | [[Database]] · [[MongoDB]] · [[Redis]] |
| Cloud & IaC | [[AWS]] · [[Terraform]] |
| Web & runtimes | [[NodeJS]] · [[React]] · [[nginx]] |
| Security | [[Security]] · [[ssh]] |

## Mistakes to Avoid
- **Mistake:** Duplicating full leaf content into this hub
- **Mistake:** Leaving placeholder wikilinks that never resolve to real notes
- **Mistake:** Treating the vault as a blog

## Pros/Cons or Trade-offs
- **Pro:** Predictable navigation; shared language across the team.
- **Con:** Hubs rot if leaves are not linked; resist turning this file into a second INDEX dump.

## Comparison
- vs [[INDEX]]: INDEX is symptom→note


### Use cases
- On-call: paste the error into your memory of [[INDEX]] categories → open the …
