[[INDEX]] [[AGENT_NOTE_RULES]] [[README]] [[staff engineer]] [[we]] [[AGENTS.md]]

# general

> Vault entry hub — where to start in Back2Basics, how notes are written, and what this collection is for.





## Interview Relevance
Not a classic interview topic — it is the map for using this vault under pressure: symptom → [[INDEX]] → domain note → fix. Staff practice includes building retrieval systems like this.

## Sources
- Vault: [[AGENT_NOTE_RULES]] — deep-dive (note shape)
- Vault: [[README]] — overview
- Vault: [[AGENTS.md]] — overview (agent editing guide)

## Core Definition
**Back2Basics** is a staff-engineer field notebook: fast retrieval for debug and configure work, not a tutorial site or man-page mirror.

## Key Concepts
- **Symptom routing:** Start at [[INDEX]], not random folder browsing.
- **Leaf shape:** Mind Map or Cornell shape when the note is a focused topic ([[AGENT_NOTE_RULES]]).
- **Hubs:** Domain roots route to leaves; avoid duplicating deep content here.
- **Mission:** Force-multiply under incident pressure ([[we]], [[staff engineer]]).

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
| How to write notes | [[AGENT_NOTE_RULES]] |
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

## Real-World Applications
On-call: paste the error into your memory of [[INDEX]] categories → open the leaf → run the listed checks. Writing: follow [[AGENT_NOTE_RULES]] so the next incident finds Interview Relevance and Mistakes fast.

## Pros/Cons or Trade-offs
- **Pro:** Predictable navigation; shared language across the team.
- **Con:** Hubs rot if leaves are not linked; resist turning this file into a second INDEX dump.

## Comparison
vs [[INDEX]]: INDEX is symptom→note; `general` is meta orientation. vs [[we]]: mission/why; `general` is how to navigate.

## Mistakes to Avoid
- Duplicating full leaf content into this hub.
- Leaving placeholder wikilinks that never resolve to real notes.
- Treating the vault as a blog — optimize for retrieval, not narrative.
