[[Redux]] [[Redux/Redux Thunk]] [[Redux toolkit]]

# Redux createAsyncThunk

> RTK helper that turns an async function into pending/fulfilled/rejected actions — wire loading and errors in the slice.

---

## Mental model

**Say it in one breath:** You write the async work once; RTK dispatches lifecycle actions you handle in `extraReducers` (or `builder`).

```txt
dispatch(fetchUser(id))
  → pending → fulfilled|rejected
slice listens → status/data/error
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **createAsyncThunk** | Async action creator | “Generates three action types for me.” |
| **rejectWithValue** | Typed error payload | “Put API error body on `action.payload`.” |
| **condition** | Skip if in flight | “Dedup duplicate loads.” |

## Standard config / commands

```ts
export const fetchUserById = createAsyncThunk(
  'user/fetchById',
  async (userId: string, { rejectWithValue }) => {
    const res = await fetch(`/api/users/${userId}`)
    if (!res.ok) return rejectWithValue(await res.text())
    return res.json()
  },
)

const userSlice = createSlice({
  name: 'user',
  initialState: { data: null as User | null, status: 'idle', error: null as string | null },
  reducers: {},
  extraReducers: (b) => {
    b.addCase(fetchUserById.pending, (s) => { s.status = 'loading' })
    b.addCase(fetchUserById.fulfilled, (s, a) => { s.status = 'succeeded'; s.data = a.payload })
    b.addCase(fetchUserById.rejected, (s, a) => { s.status = 'failed'; s.error = String(a.payload ?? a.error.message) })
  },
})
```

| Knob | Why it matters |
|------|----------------|
| `thunkAPI.signal` | Abort on unmount / newer request |
| `condition` | Prevent double-fetch |
| `serializeError` | Control what lands in rejected |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Always `rejected` with opaque error | Threw non-serializable | `rejectWithValue` plain data |
| Race shows wrong user | No abort | Pass `signal` to fetch; ignore stale |
| Pending stuck forever | Unhandled throw outside | Ensure promise settles; catch network |
| Type errors on payload | Generic args missing | `createAsyncThunk<Returned, Arg, { rejectValue }>` |

---

## Gotchas

> [!WARNING]
> **Throw vs rejectWithValue** — bare `throw` still rejects, but payload shape differs; be consistent.

> [!WARNING]
> **Prefer RTK Query** when the feature is mostly CRUD cache — less hand-written status fields.

---

## When NOT to use

- **Sync updates** — plain `createSlice` reducers.
- **Server-state-heavy apps** — [[Redux/Redux createApi]] / [[react-query]].

---

## Related

[[Redux/Redux Thunk]] [[Redux toolkit]] [[Redux/Redux createSlice]]
