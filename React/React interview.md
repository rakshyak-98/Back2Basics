[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React interview

> What strong React interviews probe — hooks rules, state placement, RSC boundaries, and debugging re-renders — with crisp trade-offs.





## Interview Relevance
This note is the study map: expect hooks, state vs server cache, keys/lists, effects vs events, and performance storytelling.

## Sources
- [React Learn](https://react.dev/learn) — overview
- [React Reference](https://react.dev/reference/react) — deep-dive

## Core Definition
React interviews reward precise mental models (render → commit → effects) and production judgment over trivia.

## Recall Cues
- Why do interviewers care about This note is the study map: expect hooks, state vs server cache, keys/lists, effects vs events, and performance storytelling?
- What is step 1: Why can’t hooks be conditional??
- What is step 2: When is Context the wrong tool??
- What is step 3: How do you fix a hydration mismatch??
- What mistake is **Answering “useMemo everything.”**?
- What mistake is **Claiming Redux is required for all apps**?

## Technical Details
Practice prompts:

1. Why can’t hooks be conditional?
2. When is Context the wrong tool?
3. How do you fix a hydration mismatch?
4. Redux vs Query vs Zustand — pick for a notifications dropdown.

## Mistakes to Avoid
- Answering “useMemo everything.”
- Claiming Redux is required for all apps.

## Comparison
- Cross-link deep leaves: [[react hooks]], [[React State management]], [[RSC (React Server Component boundaries)]].

## Real-World Applications
Whiteboard a notifications bell: unread count from query cache, dropdown open in local state, mark-read mutation with optimistic update.

## Pros/Cons or Trade-offs
- **Pro:** Structured prep covers 80% of FE rounds.
- **Con:** Memorizing API lists without failure stories fails senior bars.
