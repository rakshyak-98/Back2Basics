[[react hooks]] [[Managing complex component structure]] [[React code smells]] [[Separate functional logic from persentation components]]

# Summary pattern

> Pack component logic into **custom hooks** so the component body is mostly JSX — "summarize" behavior above the return — **React community pattern (hooks era)**.

---

## Mental model

```txt
Before:
  function Page() {
    // 40 lines useEffect, useMemo, handlers
    return <div>...</div>;
  }

After (Summary):
  function usePage() { /* 40 lines */ return { data, actions }; }
  function Page() {
    const { data, actions } = usePage();
    return <PageView data={data} {...actions} />;
  }
```

The hook is the **summary** of behavior; the component **presents** it. Enables:

- Unit test hook with `@testing-library/react` `renderHook`
- Reuse same logic across mobile/desktop views
- Clear separation from [[Separate functional logic from persentation components]]

Not the Gang of Four **Summary** (short object interface) — naming collision in this vault only.

---

## Standard config / commands

```tsx
function useRoomManager(roomId: string) {
  const { data: room, isLoading, error } = useRoomQuery(roomId);
  const [draft, setDraft] = useState("");
  const update = useUpdateRoomMutation();

  const save = useCallback(async () => {
    await update.mutateAsync({ roomId, name: draft });
  }, [roomId, draft, update]);

  useEffect(() => {
    if (room) setDraft(room.name);
  }, [room]);

  return { room, isLoading, error, draft, setDraft, save, isSaving: update.isPending };
}

export function RoomManager({ roomId }: { roomId: string }) {
  const vm = useRoomManager(roomId);
  if (vm.isLoading) return <Spinner />;
  if (vm.error) return <ErrorState error={vm.error} />;
  return <RoomManagerView {...vm} />;
}
```

### Naming convention

- `useFeatureName` — hook
- `FeatureNameView` — pure presentation (optional)
- Export hook from `useFeatureName.ts` colocated with screen

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hook 300+ lines | Multiple domains mixed | Split `useRoomData` + `useRoomForm` |
| Unstable return object | New `{}` each render | `useMemo` return bundle or destructure fields |
| Can't test without router | Hook calls `useNavigate` | Inject navigate param or wrapper in test |
| Duplicate hooks same fetch | Copy-paste | Move to shared feature hook |
| Rules of hooks error | Hook inside if | Call hook unconditionally at top |

---

## Gotchas

> [!WARNING]
> **God hook** — summary pattern doesn't mean one hook per app; split by concern.

> [!WARNING]
> **Leaking QueryClient details** — return `{ rooms, save }`, not raw `useQuery` result unless needed.

---

## When NOT to use

- **Trivial 10-line component** — inline state is clearer.
- **Shared library API** — export hook + headless component, not only internal summary.
- **Class components (legacy)** — HOC/render props instead ([[Render props]]).

---

## Related

[[react hooks]] · [[Managing complex component structure]] · [[Separate functional logic from persentation components]] · [[React Pattern/data fetching component]]
