## after navigation refresh page not_found error

create an entry in `vercel.json`
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}

```