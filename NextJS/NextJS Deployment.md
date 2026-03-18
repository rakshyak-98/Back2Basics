> [!NOTE]
> No, NextJS cannot be deployed like a plan React (CRA) project with a static `index.html`

### Static HTML Export

[static export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)

> [!INFO] You can use [`next export`](https://nextjs.org/docs/advanced-features/static-html-export) to generate a completely static site, if *you have no need for any of the dynamic features that Next.js offers.*

>[!INFO] Since Next.js supports this static export, it can be deployed and hosted on any web server that can serve HTML/CSS/JS static assets.

```txt
✓ Collecting page data
```
- Executes `getStaticProps()` or `getServerSideProps()` of reach route.
- collect data needed for reading pages.

```txt
✓ Generating static pages (5/5)
```
- NextJS rendered 5 pages into static HTML + JSON (using [[SSG]]).
- these are served directly from the CDN or filesystem.

```txt
✓ Collecting build traces
```
- Traces which files are needed by each page.
- Helps deployment platforms like vercel optimize cold starts / routing.

```txt
✓ Finalizing page optimization

```
- performs tree-shaking, minification, dead-code removal.
- Deduplicates and chunks JS/CSS assets.
- Optimizes fonts and images.

```txt
Route (app)                                 Size  First Load JS
┌ ○ /                                    25.4 kB         126 kB
└ ○ /_not-found                            977 B         102 kB

```
- `Route (app)` Lists each app route build using the App router `app/` directory.
- `Size` raw size of the static.
- `First Load JS` JS sent or first load of the page, including page + shared chunks.

- `○` → **Static HTML** (SSG).
- `●` → **Server-Side Rendered** (SSR).
- `λ` → **API route**.
- `⊕` → **ISR (Incremental Static Regeneration)**.
- `◌` → **Edge functions**.

```txt
+ First Load JS shared by all             101 kB
  ├ chunks/4bd1b696-9d0cc6a253e018b5.js  53.2 kB
  ├ chunks/684-0c284bc1235c0e67.js       45.9 kB
  └ other shared chunks (total)          1.93 kB

```
- `First load JS share by all` -> JS used across all pages. Loaded once on first navigation.
- `chunks/...` -> Auto-generated JS chunks. Includes things like shared components, layout, dependencies.
- `other shared chunks` -> smaller utility / runtime files shared by all routes.

```txt
○  (Static)  prerendered as static content

```
- explains what `○` means -> the route is fully pre-rendered at build time.
- These pages are not server-rendered, so they load faster and scale better.
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


## Transfer only the `.next` folder to the server
> [!INFO]
> No, your NextJS frontend app will not be able to run if you
> - Run `next build` (creates `.next`).
> - then delete `node_modules).`
> The `.next` directory contains the compiled output, but not the runtime dependencies.
- when you run `next start` it needs:
- `next` package itself
- other dependencies (e.g., React, middleware, API handlers)
All of these are in `node_modules`

Exceptions (Not Applicable to development)
`next export` [read more](https://nextjs.org/docs/app/guides/static-exports)


## Deployment NextJS with pm2 + Nginx

- NextJS need server (Node.js) to run;

> [!INFO]
> However your NextJS project doesn't use any server-side features like `getServerSideProps`, API routes or middleware, you can export it sa static HTML.

```js next.ocn
const nextConfig = {
	output: "exprot"
}
```