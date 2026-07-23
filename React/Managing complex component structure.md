[[React Pattern/Compound Components]] [[React Pattern/Provider pattern]] [[React Pattern/Summary pattern]] [[React Architecture]] [[React code smells]]

# Managing complex component structure

> Decompose large UIs with **Provider, Compound, Summary (hooks)** patterns — contain complexity without prop drilling — **patterns.dev / React docs**.

---

## Mental model

Complex UI = **state + composition + data fetching** tangled in one file. Three levers:

```txt
Provider pattern     → shared context for subtree (theme, auth, form wizard)
Compound components  → `<Tabs.List>` + `<Tabs.Panel>` implicit coordination
Summary pattern      → custom hooks absorb logic; component returns JSX only
```

```txt
Before: 800-line Page.tsx (fetch + reducer + 12 useState)
After:  usePageData() + usePageActions() + <PageView /> (80 lines JSX)
```

Match pattern to coupling:

| Pattern | When |
|---------|------|
| **Provider** | Many distant consumers, stable API |
| **Compound** | Parent/child UI kit (Select, Accordion) |
| **Summary hook** | One screen, heavy logic |
| **Container/Presentational** | Test pure view with mock props |

---

## Standard config / commands

### Provider (scoped, not global junk drawer)

```tsx
const WizardCtx = createContext<WizardApi | null>(null);

export function WizardProvider({ children }: { children: React.ReactNode }) {
  const [step, setStep] = useState(0);
  const api = useMemo(() => ({ step, setStep, next: () => setStep((s) => s + 1) }), [step]);
  return <WizardCtx.Provider value={api}>{children}</WizardCtx.Provider>;
}

export function useWizard() {
  const ctx = useContext(WizardCtx);
  if (!ctx) throw new Error("useWizard outside WizardProvider");
  return ctx;
}
```

### Compound component sketch

```tsx
function Tabs({ children, value, onChange }: TabsProps) {
  return <TabsContext.Provider value={{ value, onChange }}>{children}</TabsContext.Provider>;
}
Tabs.List = TabsList;
Tabs.Panel = TabsPanel;
```

### Summary pattern ([[React Pattern/Summary pattern]])

```tsx
function useCheckoutSummary(cartId: string) {
  const { data, isLoading } = useCart(cartId);
  const total = useMemo(() => sum(data?.items), [data]);
  const pay = useCallback(() => mutatePay(cartId), [cartId]);
  return { isLoading, total, pay };
}

export function CheckoutPage({ cartId }: { cartId: string }) {
  const { isLoading, total, pay } = useCheckoutSummary(cartId);
  if (isLoading) return <Spinner />;
  return <CheckoutView total={total} onPay={pay} />;
}
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Mystery re-renders | Context value recreated | `useMemo` context value; split contexts |
| Can't reuse child alone | Hidden coupling to parent | Export hook + subcomponents explicitly |
| God Provider | 20 values in one context | Split by domain ([[React State management]]) |
| Hooks rules violation | Conditional hook calls | Move hooks to top-level custom hook |
| Tests brittle | Logic in JSX | Summary hook unit tests |

---

## Gotchas

> [!WARNING]
> **Provider for server data** — use [[API handling]] / Query, not hand-rolled cache Context.

> [!WARNING]
> **Compound without documentation** — implicit child order confuses consumers; document in Storybook.

---

## When NOT to use

- **Two-level prop pass** — plain props faster than Context ceremony.
- **Single-use modal** — local `useState` enough.
- **Cross-app global everything** — [[Redux]] / [[zustand]] with selectors instead of mega-Provider.

---

## Related

[[React Pattern/Summary pattern]] · [[React Pattern/Compound Components]] · [[React Pattern/Provider pattern]] · [[React Architecture]] · [[React code smells]]
