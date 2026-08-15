[[NodeJS]] [[React/React data management]] [[Packages/npm packages]] [[zustand]]

# normalizr

> flatten nested API JSON into `{ entities, result }` by schema — dedupe by id; pairs with Redux but works standalone.

## Interview Relevance

Interviewers probe **normalizr** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Wikipedia — normalizer](https://en.wikipedia.org/wiki/normalizer) — overview

## Core Definition

APIs often return **nested graphs** (posts with embedded authors and comments). Updating one entity forces copying whole trees. **normalizr** maps response shapes to **entity tables** keyed by id:

## Key Concepts

- APIs often return **nested graphs** (posts with embedded authors and comments). Updating one entity forces copying whole trees. **normalizr** maps response shapes to **entity ta…
- Only fields described in the **schema** are normalized; everything else is copied as-is onto the entity. Relationships use `schema.Entity` references or arrays of entities.

## Technical Details

APIs often return **nested graphs** (posts with embedded authors and comments). Updating one entity forces copying whole trees. **normalizr** maps response shapes to **entity tables** keyed by id:

```
API response                    normalized store
{ posts: [{ id:1, author:{…} }]   entities: { posts:{1:…}, users:{9:…} }
                                 result: [1]
```

Only fields described in the **schema** are normalized; everything else is copied as-is onto the entity. Relationships use `schema.Entity` references or arrays of entities.

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

## Real-World Applications

In production APIs and tooling, **normalizer** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Schema must match API exactly** — renamed fields need `processStrategy` or API adapter layer; **Arrays without entity schema stay nested** — only declared relations normalize.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (flatten nested API JSON into `{ entities, result }` by schema — dedupe by id; pa…).
- **Con / when not:** **Flat list with no shared references** — store array directly.
- **Con / when not:** **GraphQL with normalized cache** — Apollo/Relay already dedupe; don't double-normalize.
- **Con / when not:** **Real-time partial patches** — merge strategy may be simpler with Immer + id map by hand.

## Comparison

vs [[React/React data management]]: know when each applies — do not treat them as interchangeable. vs [[Packages/npm packages]]: know when each applies — do not treat them as interchangeable. vs [[zustand]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Schema must match API exactly** — renamed fields need `processStrategy` or API adapter layer.
- **Arrays without entity schema stay nested** — only declared relations normalize.
- **Over-normalizing tiny payloads** — overhead not worth it for flat CRUD lists.
- **Duplicate entities:** check Unstable id (missing or composite); fix: Set `idAttribute`; ensure API returns stable ids
- **Nested data not flat:** check Field not in schema; fix: Add Entity reference to schema
- **Undefined entity merge:** check Wrong result shape; fix: Log `result` keys vs reducer expectations
- **Stale nested objects:** check Partial normalize; fix: Normalize full subgraph or merge carefully
- **Performance on huge payloads:** check Deep nesting; fix: Paginate API; normalize incrementally
