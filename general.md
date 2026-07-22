[[INDEX]] [[NOTES_STANDARD]] [[README]] [[staff engineer]]

# general

> Vault meta hub — where to start, how notes are written, and what this collection is for.

---

## Mental model

**Back2Basics** is a staff-engineer field notebook: fast retrieval under incident pressure, not a tutorial site or man-page mirror.

```txt
Symptom / design question
        ↓
    [[INDEX]]  (routing table)
        ↓
    Domain note  (mental model + triage + gotchas)
        ↓
    Fix / configure / decide
```

Every note follows [[NOTES_STANDARD]] — mental model first, then commands, then breakage playbook.

---

## Start here

| Need | Open |
|------|------|
| Symptom → note map | [[INDEX]] |
| Note format & quality bar | [[NOTES_STANDARD]] |
| Repo purpose & conventions | [[README]] |
| Staff-level scope & skills | [[staff engineer]] |

---

## How to use this vault

1. **On-call:** open [[INDEX]] → triage row → run checks in that note's table.
2. **Design review:** read mental model + "When NOT to use" before proposing tech.
3. **New note:** copy template from [[NOTES_STANDARD]]; link siblings with `[[wikilinks]]`.
4. **Rewrite thin stubs:** prioritize P0/P1 in [[NOTES_STANDARD]] vault priorities.

---

## Related

[[INDEX]] · [[NOTES_STANDARD]] · [[README]] · [[staff engineer]] · [[we]]
