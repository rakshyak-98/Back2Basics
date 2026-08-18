[[GPT]] [[prompt]]

# Prompt engineering

> Write clear instructions so the model gives you useful output. Models do not always give the same answer twice, but good prompts make results more reliable.

## Context, Task, Constraints, and Persona

Give the model:
- **Context** — background it needs
- **Task** — what you want it to do
- **Constraints** — limits (length, format, tone)
- **Persona** — role it should play (e.g. "senior SRE", "support agent")

## LLM

LLMs build text one token at a time. Each step picks the next most likely word based on the input. They do not plan the full answer first — they figure it out as they write.

LLMs only know data from training up to a cutoff date.

- **Deterministic systems** (like calculators) always give the same output for the same input.
- **LLMs are not deterministic.** Run the same prompt twice and you may get different answers. They follow probability, not fixed rules.
- **Cutoff date matters.** Older training data is usually more reliable. Newer facts may be missing or wrong unless the model can search the web.

## Chain of thought

Ask the model to think step by step, or show a few examples first (few-shot prompting).

## Temperature, Top P, Tokens, and Context window

**Temperature** controls randomness.

- Range: 0 to 2.
- **0** — always picks the most likely next word. Best for factual tasks (medical, legal, code).
- **Higher** — may pick less likely words. More creative, but can become nonsense.
- Creative apps: try ~1.4. Factual apps: try ~0.5. **2** is mostly random.

## Top P

Top P works like temperature but cuts off unlikely options.

Example: sky color — blue 80%, gray 15%, orange 5%.

- **Top P = 0.9** — only consider options in the top 90%. Orange (5%) is dropped.
- Use Top P or temperature — usually not both at high values.

> **Context window** — how many tokens the model can read at once (input + output).
