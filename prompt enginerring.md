is the process of writing effective instructions for a model such that it consistently generates content that meets your requirements. Because the content generate from a model is nondeterministic, prompting to get your desired output is a mix of art and science. However, you can apply techniques and best practices to get good results consistently.

Context, Task, Constraints, and Persona

## LLM
LLM are pattern predictors that generate one token at a time. They predict the next most likely token based on the input provided. The generation happens token by token with no planning ahead, meaning LLMs only think while they are typing. They will most often predict the next most likely token, but sometimes may predict other likely tokens instead.

LLM -> have a cut off date.

- Deterministic systems, like calculators, always produce the same output for a given input (e.g., 2 + 2 always equals 4). Nondeterministic systems can produce different outputs for the same input. LLMs are nondeterministic, meaning if you enter the same prompt multiple times, you will likely get different answers each time. This is because they predict tokens based on probability, not fixed rules.

- LLMs are trained on data collected up to a certain cutoff date. While many LLMs now have multi-modality features like internet searching that allow them to find information after their cutoff date, information before the cutoff date tends to be more reliable. This is because post-cutoff information may only exist in limited sources, making the LLM's responses potentially less accurate for very recent events or new technologies.
## Chain of thought

- asking the AI to think step-by-step or Few-Shot Prompting

> [!INFO]
> Attention is All You Need research paper introduced the transformer architecture with an attention mechanism. This allowed models to pay attention to thousands of words at a time instead of just 5-10 words like phone autocomplete. The architecture also enabled models to learn which tokens mattered most for predictions. Additionally, the paper revealed scaling laws showing that when model size increased by 10x, capability increased by 100x, leading to models that can now handle over a million tokens.