# Agent Note Rules — Internal Reference Memory

> How AI agents write and rewrite notes in this vault. Leaf notes follow a fixed **interview-prep** section order. Omit empty sections. Meta and hub notes stay routing-only.

---

## Core principles (from learning science)

Effective notes eliminate friction so understanding emerges naturally. Three principles govern every note:

### 1. Clarity over complexity

- Use simple, accessible language. Simplicity does not reduce credibility — it increases comprehension.
- The writer (agent) bears responsibility for whether the reader understands.
- Spell out abbreviations on first use. Name the real objects, steps, and failure signals — not jargon labels alone.
- Prefer complete sentences in summaries. Avoid telegraphic shorthand and unexplained insider terms.

### 2. Structure for recall and interviews

- Leaf notes use the **interview-prep skeleton** below so definitions, trade-offs, and pitfalls are easy to find.
- Prefer **networked, lateral links** (`[[wikilinks]]`) over isolated one-off pages.
- Use mind-map thinking: hub notes route to leaf notes; leaf notes link siblings and parents.
- **Omit** any section that has nothing useful to say — no placeholder stubs.

### 3. Active engagement

- Open with a **one-sentence plain-English anchor** (blockquote under the title).
- Use **visual hierarchy**: headings, tables, ASCII diagrams, and bullet clusters where they aid scanning.
- Embed **recall-prompting** material in Interview Relevance, Comparison, and Mistakes to Avoid.
- Transform passive facts into material the reader can **apply**: commands to run, checks to perform, decisions to make.

### Unifying rule

Both writer and learner must eliminate unnecessary friction. Clear writing, a predictable section order for leaf notes, and structural cues that invite interaction — not effort that obscures meaning.

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

Tag each source with coverage level: **overview** or **deep-dive**.

---

## Leaf note shape (interview-prep)

Each leaf note answers **one focused topic**. Use this section order. Skip sections that do not apply.

```markdown
[[Related]] [[Sibling]] [[Parent]]

# Topic Name

> Plain-English definition — what it does / why it exists.

## Interview Relevance
Why interviewers ask; what signal they want.

## Sources
- [Name](url) — overview | deep-dive

## Core Definition
1–2 sentences in your words (deepen the blockquote only when useful — avoid duplicate blurbs).

## Key Concepts
- **Concept A:** what → why it matters
- **Concept B:** what → why it matters

## Technical Details
Formulas, algorithms, architecture, commands, diagrams from sources.

## Real-World Applications
Practical use; one concrete scenario.

## Pros/Cons or Trade-offs
- **Pro:** advantage + context
- **Con:** limitation + context

## Comparison
vs related concept: key difference (with `[[wikilinks]]`).

## Mistakes to Avoid
Common misconceptions / wrong approaches.
```

| Section | Reader need |
|---------|-------------|
| **Interview Relevance** | Why this topic shows up in interviews |
| **Sources** | Verifiable grounding with coverage tags |
| **Core Definition** | Short precise restatement |
| **Key Concepts** | What → why it matters |
| **Technical Details** | Mechanisms, formulas, commands |
| **Real-World Applications** | Concrete ops / product scenarios |
| **Pros/Cons or Trade-offs** | Decision context |
| **Comparison** | Boundaries vs siblings |
| **Mistakes to Avoid** | Misconceptions and wrong approaches |

**Do not** force empty sections. **Do not** add strategy labels, HTML strategy tags, or boilerplate triage rows copied from other topics.

### Exclusions (do not force this skeleton)

- Meta: `AGENT_NOTE_RULES`, `AGENTS.md`, `README`, Cursor rules
- Routing hubs: `INDEX`, domain hubs that are link tables only
- Redirect stubs (`→ [[Canonical]]`)
- Canvas / non-note assets

---

## Formatting conventions

- **Title**: `# Topic Name` matching filename stem where possible.
- **Top wikilinks**: Related notes at the top (parent, siblings, dependencies).
- **Blockquote summary**: One breath — plain English; what this is and why it exists (see simple-English definition rule).
- **Wikilinks**: Obsidian `[[note]]` and `[[note|alias]]`; link siblings in the same domain.
- **Code**: Literal commands and configs in fenced blocks; do not expand tool names inside blocks.
- **Sources**: Prefer early **Sources** section with overview/deep-dive tags; keep citations honest.
- **Hub notes** (`INDEX.md`, domain roots): routing only — no deep duplication of leaf content.

---

## What to avoid

- Empty placeholder sections (“TBD”, “N/A”, bare headings with no content).
- `## Index` auto-lists unless the note is long and benefits from jump links.
- Generic triage tables (Auth/TLS/Deploy) unrelated to the note's topic.
- Casual shortenings in prose: auth, config, env, prod, repo, creds (use full words in body text).
- Duplicate stubs — merge and redirect to a canonical note.
- Placeholder wikilinks (`[[Parent]]`, `[[Sibling]]`, `[[Tool]]`) in finished notes.
- Duplicating the blockquote verbatim under Core Definition.

---

## Agent workflow for creating or rewriting a note

1. **Read** the filename, path, and any existing content for context and sibling notes in the folder.
2. **Research** the topic using authoritative sources (RFC, official docs, Wikipedia + primary source).
3. **Map** existing content into the interview-prep sections; omit empties.
4. **Write** with clarity, visual hierarchy, and wikilinks to related vault notes.
5. **Verify** facts against sources; tag coverage; add Interview Relevance and Mistakes to Avoid when thin.
6. **Link** — ensure related notes cross-link; update hub notes if routing changes.

---

## Vault integrity

- The deliverable is **notes and cross-links**, not build tooling.
- Meaningful check: `[[wikilinks]]` resolve to existing notes where possible (100% resolution is not expected for folder names and intentional stubs).
- Navigation entry points: [[README]] · [[INDEX]] · [[general]] · [[staff engineer]].

---

## Related

[[README]] · [[INDEX]] · [[AGENTS.md]]
