is the process of writing effective instructions for a model such that it consistently generates content that meets your requirements. Because the content generate from a model is nondeterministic, prompting to get your desired output is a mix of art and science. However, you can apply techniques and best practices to get good results consistently.

Context, Task, Constraints, and Persona

## LLM
LLM are pattern predictors that generate one token at a time. They predict the next most likely token based on the input provided. The generation happens token by token with no planning ahead, meaning LLMs only think while they are typing. They will most often predict the next most likely token, but sometimes may predict other likely tokens instead.

LLM -> have a cut off date.

- Deterministic systems, like calculators, always produce the same output for a given input (e.g., 2 + 2 always equals 4). Nondeterministic systems can produce different outputs for the same input. LLMs are nondeterministic, meaning if you enter the same prompt multiple times, you will likely get different answers each time. This is because they predict tokens based on probability, not fixed rules.

- LLMs are trained on data collected up to a certain cutoff date. While many LLMs now have multi-modality features like internet searching that allow them to find information after their cutoff date, information before the cutoff date tends to be more reliable. This is because post-cutoff information may only exist in limited sources, making the LLM's responses potentially less accurate for very recent events or new technologies.
## Chain of thought

- asking the AI to think step-by-step or Few-Shot Prompting


## Temperature, Top P, Tokens, and Context window

Temperature -> our way of changing a model's creativity or randomness
- controls how predictable the AI output will be. This is range from 0 to 2. At temperature 0, the LLM will always pick the most likely next word (remember, they are pattern predictors, so their responses are just picking words based on computer science and statistics). 

When we raise the temperature, the AI might pick the 2nd most likely word, or the 100th most likely word. This can make our outputs much more creative, but can also add too much randomness and make them incoherent.

> [!NOTE]
> If you are writing an application focused on creativity, you might bump the temperature up to 1.4 (remember 2 is completely random and incoherent). But if you are running a medical AI application, you might dial it way down to .5. So keep this in mind when working with these APIs.

## Top P

**Top P**: Top P _sounds similar_ to temperature, but it does something a bit different.

In every word prediction, the percentage of words that can be predicted add up to 100%. So if I ask the color of the sky, "blue" might be 80% most likely, "gray" 15% most likely, and "orange" 5% most likely. We can see that these three options add up to 100%.

- If we are running a business and want to only consider the top 90% of options, we can change our top p to .9, and it will only consider the first 90% of token/word options. What does that mean for our sky example? That "orange" would no longer be considered, because its not in the top 90% most likely next words.

> **Context Windows**: how many tokens an LLM can "remember" at a time.

