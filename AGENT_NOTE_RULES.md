# Agent Note Rules — Internal Reference Memory

> How AI agents write and rewrite notes in this vault. Pick **Mind Map** or **Cornell** shape based on how the topic connects in memory — then use shared interview-prep sections where they fit. Omit empty sections. Meta and hub notes stay routing-only.

---

## Core principles (from learning science)

Effective notes eliminate friction so understanding emerges naturally. Three principles govern every note:

### 1. Clarity over complexity

- Use simple, accessible language. Simplicity does not reduce credibility — it increases comprehension.
- The writer (agent) bears responsibility for whether the reader understands.
- Spell out abbreviations on first use. Name the real objects, steps, and failure signals — not jargon labels alone.
- Prefer complete sentences in summaries. Avoid telegraphic shorthand and unexplained insider terms.

### 2. Structure for recall and interviews

- Match **note shape** to how the topic is learned: radiating branches (Mind Map) vs ordered flow (Cornell).
- Prefer **networked, lateral links** (`[[wikilinks]]`) over isolated one-off pages.
- Hub notes route to leaf notes; leaf notes link siblings and parents — the vault is a mind map at macro scale.
- **Omit** any section that has nothing useful to say — no placeholder stubs.

### 3. Active engagement

- Open with a **one-sentence plain-English anchor** (blockquote under the title) — the **center** of every leaf note.
- Use **visual hierarchy**: headings, tables, ASCII diagrams, and bullet clusters where they aid scanning.
- Embed **recall-prompting** material: cue questions (Cornell), Interview Relevance, Comparison, and Mistakes to Avoid.
- Transform passive facts into material the reader can **apply**: commands to run, checks to perform, decisions to make.

### Unifying rule

Both writer and learner must eliminate unnecessary friction. Clear writing, a shape that mirrors how the brain holds the topic, and structural cues that invite interaction — not effort that obscures meaning.

---

## Choose note shape: Mind Map vs Cornell

| Signal in the topic | Use | Why |
|---------------------|-----|-----|
| Many related concepts around one idea; systems, ecosystems, trade-offs | **Mind Map** | Non-linear capture mirrors associative thinking |
| Clear sequence: steps, phases, lecture order, pipeline A→B→C | **Cornell** | Preserves order while building recall cues |
| Brainstorming, architecture overview, “map the territory” | **Mind Map** | Branches can grow anywhere; cross-links are natural |
| Procedures, onboarding runbooks, algorithm walkthroughs | **Cornell** | Numbered spine + cue column for review |
| Interview topic with comparisons and pitfalls | **Mind Map** (often) | Sibling concepts as peer branches |
| Certification / lecture notes with exam-style recall | **Cornell** | Cue column becomes the study guide |

**Default for this vault:** Mind Map for concept-heavy leaf notes (most domains). Cornell when the note’s value is **ordered execution** or **time-ordered capture**.

```
Mind Map (associative)                 Cornell (sequential)
                    ┌─ Branch 1       ┌──────────┬─────────────────┐
        Center ─────┤                 │ Cues     │ 1. First step   │
                    └─ Branch 2       │          │ 2. Second step  │
                                      ├──────────┴─────────────────┤
                                      │ Summary: A → B → C         │
                                      └────────────────────────────┘
```

---

## Mind Map note shape

A mind map starts with a **central idea** and branches outward. In Markdown, the center is the title + blockquote; **primary branches** are major `##` sections (aim for **4–7**); **secondary** and **tertiary** levels are bullets and sub-bullets under each branch.

### ASCII template

```
                    ┌─ Definition / Core
                    ├─ Key Concepts
        Main Topic ─┤─ Technical Details
                    │  ├─ Mechanism
                    │  └─ Commands
                    └─ Trade-offs / Pitfalls
```

### Vault mapping

| Mind map level | In this vault |
|----------------|---------------|
| **Center** | `# Title` + `> plain-English anchor` (dominant; one breath) |
| **Primary branches** (4–7 themes) | `##` sections — pick names that fit the topic, not a fixed global order |
| **Secondary branches** | `###` or bold lead bullets under each `##` |
| **Tertiary branches** | Sub-bullets, tables, short code blocks — keywords and facts, not paragraphs of prose |
| **Cross-branch links** | `[[wikilinks]]` to siblings; optional “see also” under Comparison |
| **Visual weight** | ASCII diagrams and tables for mechanisms; thinner detail in nested bullets |

### Typical primary branches (pick 4–7)

Use topic-appropriate names. Common clusters for staff-engineer notes:

- **Interview Relevance** — why this shows up in interviews
- **Sources** — verifiable grounding (overview | deep-dive tags)
- **Core Definition** — restate center only when the blockquote is not enough
- **Key Concepts** — secondary branches as `**Term:** what → why`
- **Technical Details** — mechanisms, diagrams, commands
- **Real-World Applications** — one concrete scenario
- **Pros/Cons or Trade-offs** — decision context
- **Comparison** — vs `[[sibling]]` notes
- **Mistakes to Avoid** — misconceptions

**Do not** force all nine every time. Consolidate when branches overlap (e.g. fold Applications into Key Concepts).

### Mind map craft rules

- **Keywords over sentences** on branches — 2–3 words per node when possible; expand only where precision demands it.
- **No more than 7 primary branches** — merge themes before adding an eighth `##`.
- **Hierarchy visible** — primary `##`, secondary bullets, tertiary sub-bullets; tables for parallel detail.
- **Cross-links** — when two branches relate, link explicitly (`[[note]]` or a short “connects to” line).
- **Review** — reader should grasp the whole topic from center + branch headings in one pass.

### Best use cases

Brainstorming expansions, complex systems (databases, K8s, networking), architecture summaries, comparison-heavy interview topics, hub-adjacent deep dives with many siblings.

### Common mistakes

| Mistake | Fix |
|---------|-----|
| Too much text on branches | Keywords; move depth to tertiary bullets or tables |
| Too many `##` sections | Consolidate to 5–7 primary themes |
| Flat bullet laundry list | Group under branch headings |
| Sequential steps forced into branches | Switch to **Cornell** shape |
| Duplicate center | Do not repeat the blockquote verbatim under Core Definition |

### Example skeleton

````markdown
[[Related]] [[Sibling]] [[Parent]]

# Topic Name

> Center — one plain-English sentence: what it is and why it exists.

## Interview Relevance
Why interviewers ask; what signal they want.

## Sources
- [Name](url) — overview | deep-dive

## Key Concepts
- **Branch A:** what → why it matters
- **Branch B:** what → why it matters

## Technical Details
```txt
Optional ASCII mind map or flow
```
| Mechanism | Detail |
|-----------|--------|

## Comparison
vs [[Sibling]]: boundary in one line.

## Mistakes to Avoid
- Misconception → correction
````

---

## Cornell note shape

The Cornell method keeps **sequence** in the main column and adds **recall cues** plus a **summary**. Ideal when order matters: lectures, pipelines, boot sequences, debugging flows.

### ASCII template

```
┌──────────────────┬──────────────────────────┐
│ Cue: What is     │ 1. First concept — define │
│ the main flow?   │ 2. Second concept — apply │
│                  │ 3. Third concept — result │
├──────────────────┴──────────────────────────┤
│ Summary: Sequence moves from A → B → C      │
└─────────────────────────────────────────────┘
```

### Vault mapping

| Cornell zone | ~Share of note | In this vault |
|--------------|----------------|---------------|
| **Notes** (right, ~60%) | Main capture | `## Technical Details` with **numbered** steps; `## Core Definition` for setup context |
| **Cues** (left, ~25%) | Retrieval prompts | `## Interview Relevance` + `## Recall Cues` (questions the notes answer) |
| **Summary** (bottom, ~15%) | 3–5 sentence synthesis | Top blockquote (center) **or** `## Summary` at bottom if blockquote stays definitional |

### Cornell craft rules

- **During capture:** write only the notes column — numbered list is the spine; use abbreviations in drafts if needed.
- **On rewrite:** add `## Recall Cues` — questions, key terms, “How does X relate to Y?”
- **Summary:** state the **flow** (A→B→C) and the main takeaway; complete sentences.
- **Review loop:** cues should let a reader answer from memory before reading Technical Details.
- **Diagrams:** put flows in Technical Details or margin-style `txt` blocks; do not break numbered sequence.

### Typical section order (Cornell leaf)

```markdown
[[Related]] [[Sibling]] [[Parent]]

# Topic Name

> Summary-quality anchor — often the A→B→C takeaway in one breath.

## Interview Relevance
What interviewers probe along this sequence.

## Sources
- [Name](url) — overview | deep-dive

## Core Definition
Setup context before the numbered flow (optional if blockquote suffices).

## Recall Cues
- What triggers step 1?
- What fails if step 3 is skipped?
- Key term: …

## Technical Details
1. First step — define / observe
2. Second step — apply / transform
3. Third step — verify / result

## Mistakes to Avoid
- Wrong order or skipped step → symptom

## Comparison
When to use this sequence vs [[alternative]].
```

Omit **Recall Cues** only if Interview Relevance already lists equivalent questions. Omit **Comparison** when not applicable.

### Best use cases

Lecture-style material, CI/CD stages, request lifecycles, incident response checklists, algorithm traces, certification study notes.

### Common mistakes

| Mistake | Fix |
|---------|-----|
| Cues written before notes exist | Add cues on rewrite, not first draft |
| Unnumbered Technical Details | Number the spine; sub-bullets for detail per step |
| Summary missing the arrow | Explicit “starts with X, ends with Y” |
| Transcription | Synthesize; cues + summary force compression |

---

## Shared interview-prep vocabulary

Both shapes reuse the same **section names** where they apply. This keeps the vault grep-friendly and interview-aligned.

| Section | Reader need | Mind Map | Cornell |
|---------|-------------|----------|---------|
| **Interview Relevance** | Why this topic shows up | Often a primary branch | Often cue seeds |
| **Sources** | Verifiable grounding | Early branch | Early, before long sequence |
| **Core Definition** | Short precise restatement | Only if blockquote insufficient | Setup before numbered flow |
| **Key Concepts** | What → why | Secondary branches | Usually merged into steps |
| **Technical Details** | Mechanisms, commands | Diagrams, tables, depth | **Numbered spine** |
| **Recall Cues** | Questions for active recall | Optional | **Recommended** |
| **Real-World Applications** | Concrete ops scenario | Branch or bullet | After sequence |
| **Pros/Cons or Trade-offs** | Decision context | Branch | After sequence |
| **Comparison** | Boundaries vs siblings | Cross-branch links | vs alternative flow |
| **Mistakes to Avoid** | Misconceptions | Branch | Wrong order / skipped steps |
| **Summary** | Page synthesis | Usually blockquote only | Blockquote or `## Summary` |

**Do not** add strategy labels, HTML strategy tags, or boilerplate triage rows copied from other topics.

### Exclusions (do not force either shape)

- Meta: `AGENT_NOTE_RULES`, `AGENTS.md`, `README`, Cursor rules
- Routing hubs: `INDEX`, domain hubs that are link tables only
- Redirect stubs (`→ [[Canonical]]`)
- Canvas / non-note assets

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

## Formatting conventions

- **Title**: `# Topic Name` matching filename stem where possible.
- **Top wikilinks**: Related notes at the top (parent, siblings, dependencies).
- **Blockquote summary**: One breath — plain English; center of Mind Map notes; often summary in Cornell notes.
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
- Wrong shape: numbered runbook in Mind Map branches, or concept laundry list without Cornell cues.

---

## Agent workflow for creating or rewriting a note

1. **Read** the filename, path, and any existing content; scan sibling notes in the folder.
2. **Choose shape** — Mind Map (associative) vs Cornell (sequential) using the decision table above.
3. **Research** the topic using authoritative sources (RFC, official docs, Wikipedia + primary source).
4. **Map** content to the chosen shape; for Mind Map, sketch 4–7 primary branches; for Cornell, outline numbered spine then cues.
5. **Write** center (title + blockquote), branches or numbered notes, then cues/summary as appropriate.
6. **Verify** facts against sources; tag coverage; add Interview Relevance and Mistakes to Avoid when thin.
7. **Link** — `[[wikilinks]]` to related notes; update hub notes if routing changes.

---

## Vault integrity

- The deliverable is **notes and cross-links**, not build tooling.
- Meaningful check: `[[wikilinks]]` resolve to existing notes where possible (100% resolution is not expected for folder names and intentional stubs).
- Navigation entry points: [[README]] · [[INDEX]] · [[general]] · [[staff engineer]].

---

## Related

[[README]] · [[INDEX]] · [[AGENTS.md]]
