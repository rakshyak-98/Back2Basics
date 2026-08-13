[[NextJS]]

# NextJS Deployment

> NextJS Deployment — executes getStaticProps() or getServerSideProps() of reach route.

---

## How it works


> [!NOTE]
> No, NextJS cannot be deployed like a plan React (CRA) project with a static `index.html`
### Static HTML Export
[static export](https://nextjs.org/docs/application/building-your-application/deploying/static-exports)
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
- Optimizes fon

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **NextJS Deployment** | This note’s core idea | “I explain NextJS Deployment in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---


## Configuration and commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Runtime error | stack / overlay | Null-check; fix import |
| Build fail | deps / tsconfig | Align versions; clear cache |
| Auth/CORS | network tab | Headers and tokens |

---


## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---


## When not to use

- Skip when a simpler existing approach already fits.

---


## Related

[[NextJS]]

## Sources

- [Wikipedia — NextJS Deployment](https://en.wikipedia.org/wiki/NextJS_Deployment)
