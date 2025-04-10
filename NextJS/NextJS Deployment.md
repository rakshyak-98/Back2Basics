### Static HTML Export
[static export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)

>[!INFO] Since Next.js supports this static export, it can be deployed and hosted on any web server that can serve HTML/CSS/JS static assets.


## Error
### 🔹 `generateStaticParams()`

It’s a **Next.js-specific function** used in **App Router** for dynamic routes (e.g., `[id]`) when doing **static site generation** (`output: 'export'` or `getStaticPaths` in old Pages Router).

---

### 🔧 Purpose:

Tells Next.js at **build time** what params (`id`, `slug`, etc.) to pre-render.

---

### 📍Location:

Must be **exported** from the same file as the route:  
`/app/blog-details/[id]/page.tsx`

```ts
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }];
}
```

---

### 🧠 Notes:

- Runs at **build time only**
    
- Equivalent of `getStaticPaths` (Pages Router)
    
- Required for **static export** if using `[param]` routes
    

Let me know if you want a minimal working setup example.