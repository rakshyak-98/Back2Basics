[[Descriptive/web development]] [[Rendering performance/INP]] [[Rendering performance/critical rendering path]] [[Nginx/nginx SPA deployment]] [[Security/content security policy]]

# SEO

> Search Engine Optimization — make pages crawlable, understandable, and eligible to rank (and for rich results) without harming users.

## Interview Relevance

Full-stack interviews mix technical SEO with performance: crawl/index basics, canonicalization, SPA rendering, and Core Web Vitals ([[Rendering performance/INP]], LCP, CLS) as quality signals.

## Sources

- [Google — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) — overview
- [Google — Search Essentials](https://developers.google.com/search/docs/essentials) — deep-dive
- [Wikipedia — Search engine optimization](https://en.wikipedia.org/wiki/Search_engine_optimization) — overview

## Core Definition

Search engines discover URLs, render or parse content, index it, then rank for queries. SEO is the set of technical and content practices that help the right pages get found without violating quality guidelines.

## Key Concepts

- **Crawl → index → rank:** bots fetch URLs (respecting `robots.txt`), interpret content, store documents, then score relevance/quality.
- **Technical baseline:** unique titles, meta descriptions, canonical URLs, mobile-usable layout, HTTPS, sane status codes.
- **Rendering:** Google can run JavaScript, but critical content in initial HTML (SSR/SSG/prerender) is more reliable — see [[Nginx/nginx SPA deployment]].
- **Core Web Vitals:** field performance is a ranking *signal among many* — fix [[Rendering performance/INP]] / LCP / CLS on money pages.
- **Structured data:** JSON-LD (`schema.org`) can enable rich results when markup matches visible content.

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

## Real-World Applications

Marketing SPA was a blank shell for bots: added prerender for key routes, self-referencing canonicals, and fixed LCP/INP — organic landing pages started appearing in Search Console coverage.

## Pros/Cons or Trade-offs

- **Pro:** Technical hygiene compounds — crawl budget and CWV help users and bots.
- **Con:** Chasing vanity keywords with thin pages burns trust and crawl budget.

## Comparison

- vs paid ads: SEO is organic discovery; slower feedback, different measurement.
- vs [[Rendering performance/critical rendering path]]: CRP optimizes first paint for humans; SEO also needs crawlable content and metadata.

## Mistakes to Avoid

- Canonicalizing every route to the homepage in an SPA.
- Shipping `noindex` from staging into production via shared templates.
- Keyword stuffing / doorway pages — quality systems demote them.
- SEO-tuning authenticated internal tools — `noindex` and save the effort.
