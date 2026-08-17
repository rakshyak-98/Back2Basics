[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]]

# Compound Components

> Compound components are a React composition pattern where a parent and its named children share implicit state through Context — giving consumers a flexible, declarative JSX API without prop drilling.

---

## Why It Matters

When a component's API is naturally expressed as a tree of related pieces (`<Tabs><TabList><Tab/></TabList><TabPanels><TabPanel/></TabPanels></Tabs>`), compound components let users rearrange and omit parts while the parent coordinates behavior. This pattern appears in Radix UI, Reach UI, React Aria, and internal design systems. Reviewers ask when to use compound components vs custom hooks vs render props — the answer depends on whether the **JSX structure** is part of the public API.

---

## Sources

- [React — Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context) — Official guide to Context as the mechanism behind compound component state sharing.
- [Kent C. Dodds — Compound Components with React Hooks](https://kentcdodds.com/blog/compound-components-with-react-hooks) — Modern implementation using custom hooks instead of class-based implicit state.
- [Radix UI Primitives](https://www.radix-ui.com/primitives) — Production examples of accessible compound component APIs in the wild.

---

## Key Concepts

```txt
<Tabs>                    ← Provider: holds activeIndex state
  <TabList>               ← Consumes context: renders tab buttons
    <Tab index={0} />     ← Registers itself; sets active on click
    <Tab index={1} />
  </TabList>
  <TabPanels>
    <TabPanel index={0} />  ← Shows content when activeIndex matches
    <TabPanel index={1} />
  </TabPanels>
</Tabs>
```

| Concept | Detail |
|---------|--------|
| **Implicit state** | Parent holds state; children read via Context without prop drilling. |
| **Flexible composition** | Consumers reorder, omit, or wrap children — unlike monolithic props. |
| **Static sub-components** | `Tabs.List`, `Tabs.Tab` attached to parent — discoverable API. |
| **vs custom hooks** | Hooks share logic; compound components share logic **and** JSX structure. |
| **vs render props** | Render props pass behavior as a function; compound components pass structure as children. |

---

## Technical Details

### Implementation with Context + hooks

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

type AccordionContext = { openIndex: number | null; setOpenIndex: (i: number | null) => void };
const Ctx = createContext<AccordionContext | null>(null);

function useAccordion() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('Accordion sub-components must be inside <Accordion>');
  return ctx;
}

function Accordion({ children }: { children: ReactNode }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  return <Ctx.Provider value={{ openIndex, setOpenIndex }}>{children}</Ctx.Provider>;
}

function Item({ index, children }: { index: number; children: ReactNode }) {
  const { openIndex, setOpenIndex } = useAccordion();
  const isOpen = openIndex === index;
  return (
    <div>
      <button onClick={() => setOpenIndex(isOpen ? null : index)}>Toggle</button>
      {isOpen && <div>{children}</div>}
    </div>
  );
}

Accordion.Item = Item;
export { Accordion };
```

### Consumer API

```tsx
<Accordion>
  <Accordion.Item index={0}>Section one content</Accordion.Item>
  <Accordion.Item index={1}>Section two content</Accordion.Item>
</Accordion>
```

### When to use each pattern

| Pattern | Best for |
|---------|----------|
| **Custom hook** (`useTabs()`) | Logic reuse; consumer owns JSX structure |
| **Compound components** | JSX structure is part of the contract; design system primitives |
| **Render props** | Maximum flexibility; consumer controls rendering entirely |
| **HOC** | Legacy libraries; avoid in greenfield 2026 code |

---

## Mistakes to Avoid

- Compound components for simple boolean toggle — `useState` alone is enough.
- Context holding high-frequency changing values inside compound tree — re-renders all consumers.
- Missing runtime guard (`useAccordion` throws outside provider) — silent `null` context bugs.
- Attaching 15 sub-components to one parent — flatten or split into multiple compound families.
- Using HOCs in greenfield code when a hook + compound component achieves the same result.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Declarative, readable JSX API | More boilerplate than a single component with props |
| Consumers control layout and order | Harder to tree-shake than flat components |
| Familiar pattern in design systems | Overkill when a hook alone suffices |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[react hooks]] | Hooks share logic; compound components also define JSX composition contract |
| [[Component Presentational Pattern]] | Container/presentational splits data from view; compound splits coordination from pieces |
| [[data fetching component]] | Different concern — data loading vs UI composition |

---

## Use cases

- Design system `<Select>`, `<Dialog>`, `<Tabs>` with accessible sub-parts.
- Multi-step wizard where steps can be reordered: `<Wizard><Wizard.Step/><Wizard.Navigation/></Wizard>`.
- Form field groups: `<Fieldset><Fieldset.Legend/><Fieldset.Input/></Fieldset>`.
