[[NodeJS]] [[React/React data management]] [[Packages/npm packages]] [[zustand]]

# normalizr

> flatten nested API JSON into `{ entities, result }` by schema — dedupe by id; pairs with Redux but works standalone.

```txt
        normalizr ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **normalizr** to see if you understand what it does operat…

## Sources
- [Wikipedia — normalizer](https://en.wikipedia.org/wiki/normalizer) — overview

## Key Concepts
- **APIs often:** APIs often return **nested graphs** (posts with embedded authors and comments)
- **Only fields:** Only fields described in the **schema** are normalized


- **Core:** APIs often return **nested graphs** (posts with embedded authors and comments)

## Technical Details
- APIs often return **nested graphs** (posts with embedded authors and comments…
- Updating one entity forces copying whole trees.
- **normalizr:** maps response shapes to **entity tables** keyed by id:

```
API response                    normalized store
{ posts: [{ id:1, author:{…} }]   entities: { posts:{1:…}, users:{9:…} }
                                 result: [1]
```

- Only fields described in the **schema** are normalized
- Relationships use `schema.Entity` references or arrays of entities.

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

## Mistakes to Avoid
- **Mistake:** **Schema must match API exactly**
- **Mistake:** **Arrays without entity schema stay nested**
- **Mistake:** **Over-normalizing tiny payloads**
- **Mistake:** **Duplicate entities:** check Unstable id (missing or composite)
- **Mistake:** **Nested data not flat:** check Field not in schema
- **Mistake:** **Undefined entity merge:** check Wrong result shape
- **Mistake:** **Stale nested objects:** check Partial normalize
- **Mistake:** **Performance on huge payloads:** check Deep nesting

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (flatten nested API JSON into `{ entities, result }` by schema — dedupe by id; pa…).
- **Con / when not:** **Flat list with no shared references**
- **Con / when not:** **GraphQL with normalized cache**
- **Con / when not:** **Real-time partial patches**

## Comparison
- vs [[React/React data management]]: know when each applies


### Use cases
- In production APIs and tooling, **normalizer** shows up whenever teams ship N…
