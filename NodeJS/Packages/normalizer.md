[[NodeJS]] [[React/React data management]] [[Packages/npm packages]]

# normalizr

> One-line: flatten nested API JSON into `{ entities, result }` by schema — dedupe by id; pairs with Redux but works standalone.

## Mental model

APIs often return **nested graphs** (posts with embedded authors and comments). Updating one entity forces copying whole trees. **normalizr** maps response shapes to **entity tables** keyed by id:

```
API response                    normalized store
{ posts: [{ id:1, author:{…} }]   entities: { posts:{1:…}, users:{9:…} }
                                 result: [1]
```

Only fields described in the **schema** are normalized; everything else is copied as-is onto the entity. Relationships use `schema.Entity` references or arrays of entities.

## Standard config / commands

### Schema + normalize

```javascript
import { normalize, schema } from 'normalizr';

const user = new schema.Entity('users');
const comment = new schema.Entity('comments', { author: user });
const post = new schema.Entity('posts', {
  author: user,
  comments: [comment],
});

const data = {
  posts: [{ id: '1', title: 'Hi', author: { id: '9', name: 'Ada' }, comments: [] }],
};

const { entities, result } = normalize(data, { posts: [post] });
// entities.users['9'], entities.posts['1'], result.posts === ['1']
```

### Without Redux (pure transform)

```javascript
function mergePosts(state, apiPayload) {
  const { entities, result } = normalize(apiPayload, { posts: [post] });
  return {
    users: { ...state.users, ...entities.users },
    posts: { ...state.posts, ...pickIds(state.posts, result.posts, entities.posts) },
  };
}
```

### idAttribute / processStrategy

```javascript
const file = new schema.Entity('files', {}, {
  idAttribute: 'uuid',
  processStrategy: (value) => ({ ...value, fetchedAt: Date.now() }),
});
```

### denormalize (read path)

```javascript
import { denormalize } from 'normalizr';
const postWithAuthor = denormalize(result.posts[0], post, entities);
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate entities | Unstable id (missing or composite) | Set `idAttribute`; ensure API returns stable ids |
| Nested data not flat | Field not in schema | Add Entity reference to schema |
| Undefined entity merge | Wrong result shape | Log `result` keys vs reducer expectations |
| Stale nested objects | Partial normalize | Normalize full subgraph or merge carefully |
| Performance on huge payloads | Deep nesting | Paginate API; normalize incrementally |

## Gotchas

> [!WARNING]
> **Schema must match API exactly** — renamed fields need `processStrategy` or API adapter layer.

> [!WARNING]
> **Arrays without entity schema stay nested** — only declared relations normalize.

> [!WARNING]
> **Over-normalizing tiny payloads** — overhead not worth it for flat CRUD lists.

## When NOT to use

- **Flat list with no shared references** — store array directly.
- **GraphQL with normalized cache** — Apollo/Relay already dedupe; don't double-normalize.
- **Real-time partial patches** — merge strategy may be simpler with Immer + id map by hand.

## Related

[[React/React data management]] [[zustand]] [[Packages/npm packages]] [[NodeJS]]
