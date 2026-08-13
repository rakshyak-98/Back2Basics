# Agent Note Rules — Internal Reference Memory

> How AI agents write and rewrite notes in this vault. No predefined templates. Structure follows **conceptual relationships**, not delivery order.

---

## Core principles (from learning science)

Effective notes eliminate friction so understanding emerges naturally. Three principles govern every note:

### 1. Clarity over complexity

- Use simple, accessible language. Simplicity does not reduce credibility — it increases comprehension.
- The writer (agent) bears responsibility for whether the reader understands.
- Spell out abbreviations on first use. Name the real objects, steps, and failure signals — not jargon labels alone.
- Prefer complete sentences in summaries. Avoid telegraphic shorthand and unexplained insider terms.

### 2. Structure mirrors cognition

- Organize by **conceptual relationships** and subject-level grouping, not lecture sequence or arbitrary section templates.
- Prefer **networked, lateral links** (`[[wikilinks]]`) over isolated one-off pages.
- Use mind-map thinking: hub notes route to leaf notes; leaf notes link siblings and parents.
- Headings emerge from what the topic needs — not from a fixed skeleton (no mandatory "Mental model → Triage → Gotchas" blocks).

### 3. Active engagement

- Open with a **one-sentence anchor** that states what this is and why it matters.
- Use **visual hierarchy**: headings, tables, ASCII diagrams, and bullet clusters where they aid scanning.
- Embed **recall-prompting questions** where useful (e.g. "What breaks first when…?", "When would you choose X over Y?").
- Transform passive facts into material the reader can **apply**: commands to run, checks to perform, decisions to make.

### Unifying rule

Both writer and learner must eliminate unnecessary friction. Clear writing, organized by how ideas connect, with structural cues that invite interaction — not effort that obscures meaning.

---

## Source of truth (when researching or recreating notes)

Ground content in authoritative, verifiable sources. Prefer:

| Tier | Examples |
|------|----------|
| **Standards & specs** | RFCs, W3C, ISO, vendor official docs (AWS, Kubernetes, PostgreSQL) |
| **Academic & research** | MIT OpenCourseWare, Stanford CS notes, Oxford reading lists, peer-reviewed papers |
| **Canonical references** | O'Reilly / Addison-Wesley texts cited by the field (Kleppmann, Kerrisk, Stevens, Burns) |
| **Encyclopedic baseline** | Wikipedia (cross-check with primary sources) |
| **Industry practice** | Google SRE book, CNCF docs, major cloud provider architecture guides |

Do not invent facts. If a topic is uncertain, say what is known and link the source. Strip wiki/ChatGPT citation spam; keep real attributions.

---

## Note shape (flexible, not templated)

Each note answers **one focused topic** (tool, concept, procedure, comparison, or hub). Choose sections based on what the reader needs:

| Reader need | Typical content (use only what fits) |
|-------------|--------------------------------------|
| **Understand** | Definition, mechanism, how parts relate, trade-offs |
| **Operate** | Configuration, commands, verification steps |
| **Debug** | Symptom → check → fix rows for *this* topic only |
| **Decide** | Criteria, options, when to pick each |
| **Navigate** | Routing table, curated links (hub notes) |

**Do not** force empty sections. **Do not** add strategy labels, HTML strategy tags, or boilerplate triage rows copied from other topics.

---

## Formatting conventions

- **Title**: `# Topic Name` matching filename stem where possible.
- **Top wikilinks**: Related notes at the top (parent, siblings, dependencies).
- **Blockquote summary**: One breath — what this is and the first thing that breaks or matters.
- **Wikilinks**: Obsidian `[[note]]` and `[[note|alias]]`; link siblings in the same domain.
- **Code**: Literal commands and configs in fenced blocks; do not expand tool names inside blocks.
- **Sources**: End with a **Sources** or inline citations where facts are non-obvious.
- **Hub notes** (`INDEX.md`, domain roots): routing only — no deep duplication of leaf content.

---

## What to avoid

- Predefined template section order mandated across all notes.
- `## Index` auto-lists unless the note is long and benefits from jump links.
- Generic triage tables (Auth/TLS/Deploy) unrelated to the note's topic.
- Casual shortenings in prose: auth, config, env, prod, repo, creds (use full words in body text).
- Duplicate stubs — merge and redirect to a canonical note.
- Placeholder wikilinks (`[[Parent]]`, `[[Sibling]]`, `[[Tool]]`) in finished notes.

---

## Agent workflow for creating or rewriting a note

1. **Read** the filename, path, and any existing content for context and sibling notes in the folder.
2. **Research** the topic using authoritative sources (RFC, official docs, Wikipedia + primary source).
3. **Plan** structure from conceptual relationships — what must the reader know first, what depends on what?
4. **Write** with clarity, visual hierarchy, and wikilinks to related vault notes.
5. **Verify** facts against sources; add citations for specs, defaults, and numbers.
6. **Link** — ensure related notes cross-link; update hub notes if routing changes.

---

## Vault integrity

- The deliverable is **notes and cross-links**, not build tooling.
- Meaningful check: `[[wikilinks]]` resolve to existing notes where possible (100% resolution is not expected for folder names and intentional stubs).
- Navigation entry points: [[README]], [[INDEX]], [[general]], [[staff engineer]].

---

## Related

[[README]] · [[INDEX]] · [[AGENTS.md]]
