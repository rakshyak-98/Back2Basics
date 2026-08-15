[[general]] [[staff engineer]] [[AGENT_NOTE_RULES]] [[Repro]] [[TL;DR]]

# Useful prompt for learning with AI chat

> Useful learning prompts — ask the model for facts to memorize, real problems to solve, contrasts, and post-mortems on your mistakes.

## Interview Relevance
Self-taught and staff candidates who learn deliberately beat those who only paste “explain X.” These prompts force retrieval practice, comparison, and error analysis — the same skills interviews test.

## Sources
- [Make It Stick — retrieval practice (overview via authors’ site)](https://www.retrievalpractice.org/) — overview
- Vault authoring: [[AGENT_NOTE_RULES]] — deep-dive (how we structure notes for recall)

## Core Definition
A learning prompt is a reusable question pattern that turns a chat model into a tutor: it demands concrete facts, worked examples, contrasts, or diagnosis of *your* error — not a vague dump of documentation.

## Key Concepts
- **Memorize with structure:** Ask for key facts/formulas *and* a mnemonic.
- **Apply:** Solve a realistic problem; demand the thought process.
- **Compare:** Force boundaries between sibling concepts.
- **Error analysis:** Describe your mistake; get the fix and a prevention rule.
- **Verify:** Cross-check answers against primary docs ([[AGENT_NOTE_RULES]] sources tier).

## Technical Details
Copy-paste patterns (replace `(topic)` / `(concept)`):

1. **Memorize:** “What are the most important facts, dates, or formulas related to (topic)? Help me create a memorization technique to remember them easily.”
2. **Apply:** “Use your knowledge of (topic) to solve a real-world problem. Explain your thought process and share your solution.”
3. **Compare:** “Compare and contrast (concept 1) and (concept 2). Use examples.”
4. **Debug me:** “I made a mistake while practicing (skill). [Describe it]. Explain what went wrong and how I avoid it next time.”

Follow with: “Cite the RFC/official doc I should read” and “Give me a 3-question self-quiz.”

## Real-World Applications
Studying Postgres indexes: compare B-tree vs GIN, then ask for a broken `EXPLAIN` to diagnose. Studying networking: contrast [[Broadcast]] vs [[Multicast]], then invent a packet-capture quiz.

## Pros/Cons or Trade-offs
- **Pro:** Active learning; portable across topics; pairs well with vault notes.
- **Con:** Models hallucinate — always verify; prompts without primary sources create false confidence.

## Comparison
vs passive “explain X”: weaker retention. vs writing a leaf note: prompts gather material; notes ([[AGENT_NOTE_RULES]]) are the durable artifact. Related: [[TL;DR]] for compressing answers; [[Repro]] for bug-study discipline.

## Mistakes to Avoid
- Accepting answers without a source check.
- Only asking for summaries — skip application and comparison prompts.
- Pasting proprietary code/secrets into public chat tools.
