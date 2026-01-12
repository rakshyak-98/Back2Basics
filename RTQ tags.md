- It shows how RTK Query knows which queries should be invalidated/refetched when you use tags.

```text
    provided: {
      tags: {
        Posts: {
          __internal_without_id: [
            'getAllPosts(undefined)'
          ]
        }
      },
      keys: {
        'getAllPosts(undefined)': [
          {
            type: 'Posts'
          }
        ]
      }
    },
```

## What does "providing" a tag mean?

- if someone later invalidates the `Posts` tag.
