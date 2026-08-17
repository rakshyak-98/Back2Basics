[[Descriptive/web development]] [[Rendering performance/INP]] [[Rendering performance/critical rendering path]] [[Nginx/nginx SPA deployment]] [[Security/content security policy]]

# SEO

> Search Engine Optimization — make pages crawlable, understandable, and eligible to rank (and for rich results) without harming users.

```txt
        SEO ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Full-stack reviews mix technical SEO with performance: crawl/index basics,…

## Sources
- [Google — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) — overview
- [Google — Search Essentials](https://developers.google.com/search/docs/essentials) — deep-dive
- [Wikipedia — Search engine optimization](https://en.wikipedia.org/wiki/Search_engine_optimization) — overview

## Key Concepts
- **Crawl → index → rank:** bots fetch URLs (respecting `robots.txt`), interpret content, store documents…
- **Technical baseline:** unique titles, meta descriptions, canonical URLs, mobile-usable layout, HTTPS…
- **Rendering:** Google can run JavaScript, but critical content in initial HTML (SSR/SSG/prer…
- **Core Web Vitals:** field performance is a ranking *signal among many*
- **Structured data:** JSON-LD (`schema.org`) can enable rich results when markup matches visible co…


- **Core:** Search engines discover URLs, render or parse content, index it, then rank fo…

## Technical Details
```
Googlebot → robots.txt → fetch HTML → render (JS) → index → rank
```

```html
<title>Unique page title — brand</title>
<meta name="description" content="Clear 1–2 sentence summary">
<link rel="canonical" href="https://example.com/page">
<meta name="robots" content="index,follow">
```

```text
User-agent: *
Disallow: /admin/
Sitemap: https://example.com/sitemap.xml
```

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Example",
  "datePublished": "2026-01-15"
}
</script>
```

```bash
npx lighthouse https://example.com --only-categories=seo,performance
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Not indexed | Search Console coverage | Remove `noindex`; fix robots/canonical |
| Duplicate titles | CMS defaults | Unique `<title>` per URL |
| Soft 404 | Thin body + HTTP 200 | Real content or proper 404 |
| JS content missing | View rendered HTML | SSR/prerender critical path |
| Staging `noindex` in production | Meta/robots on live | Guard by environment configuration carefully |

## Mistakes to Avoid
- **Mistake:** Canonicalizing every route to the homepage in an SPA
- **Mistake:** Shipping `noindex` from staging into production via shared templ…
- **Mistake:** Keyword stuffing / doorway pages — quality systems demote them
- **Mistake:** SEO-tuning authenticated internal tools

## Pros/Cons or Trade-offs
- **Pro:** Technical hygiene compounds — crawl budget and CWV help users and bots.
- **Con:** Chasing vanity keywords with thin pages burns trust and crawl budget.

## Comparison
- vs paid ads: SEO is organic discovery; slower feedback, different measurement.
- vs [[Rendering performance/critical rendering path]]: CRP optimizes first paint for humans


### Use cases
- Marketing SPA was a blank shell for bots: added prerender for key routes, sel…
