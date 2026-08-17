[[general]] [[staff engineer]] [[AGENT_NOTE_RULES]] [[Repro]] [[TL;DR]]

# Useful prompt for learning with AI chat

> Useful learning prompts — ask the model for facts to memorize, real problems to solve, contrasts, and post-mortems on your mistakes.

```txt
        Useful prompt for  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Self-taught and staff candidates who learn deliberately beat those who only p…

## Sources
- [Make It Stick — retrieval practice (overview via authors’ site)](https://www.retrievalpractice.org/) — overview
- Vault authoring: [[AGENT_NOTE_RULES]] — deep-dive (how we structure notes for recall)

## Key Concepts
- **Core:** A learning prompt is a reusable question pattern that turns a chat model into…

## Technical Details
- Copy-paste patterns (replace `(topic)` / `(concept)`):

1. **Memorize:** “What are the most important facts, dates, or formulas related to (topic)? Help me create a memorization technique to remember them easily.”
2. **Apply:** “Use your knowledge of (topic) to solve a real-world problem. Explain your thought process and share your solution.”
3. **Compare:** “Compare and contrast (concept 1) and (concept 2). Use examples.”
4. **Debug me:** “I made a mistake while practicing (skill). [Describe it]. Explain what went wrong and how I avoid it next time.”

- Follow with: “Cite the RFC/official doc I should read” and “Give me a 3-quest…

## Mistakes to Avoid
- **Mistake:** Accepting answers without a source check
- **Mistake:** Only asking for summaries
- **Mistake:** Pasting proprietary code/secrets into public chat tools

## Pros/Cons or Trade-offs
- **Pro:** Active learning; portable across topics; pairs well with vault notes.
- **Con:** Models hallucinate — always verify; prompts without primary sources create false confidence.

## Comparison
- vs passive “explain X”: weaker retention. vs writing a leaf note: prompts gat…


### Use cases
- Studying Postgres indexes: compare B-tree vs GIN, then ask for a broken `EXPL…
