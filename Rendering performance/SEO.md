[[Descriptive/web development]] [[Rendering performance/INP]] [[Nginx/nginx SPA deployment]] [[Security/content security policy]]

# SEO (Search Engine Optimization)

> Make content discoverable, crawlable, and eligible for rich results — technical + content signals — **Google Search Essentials**.

## Mental model

Search engines **crawl** URLs, **index** content, **rank** for queries. SEO spans:

```
Technical (crawl, speed, mobile) + Content (intent, E-E-A-T) + Links (authority)
```

Modern baseline includes **Core Web Vitals** ([[Rendering performance/INP]], LCP, CLS) as quality signals — not the only ranking factor.

```
Googlebot → robots.txt → fetch HTML → render (JS) → index → rank
```

## Standard config / commands

### Non-negotiable technical checklist

```html
<title>Unique page title — brand</title>
<meta name="description" content="155 char summary">
<link rel="canonical" href="https://example.com/page">
<meta name="robots" content="index,follow">

<meta property="og:title" content="…">
<meta property="og:image" content="https://…/og.png">
```

### robots.txt

```text
User-agent: *
Disallow: /admin/
Sitemap: https://example.com/sitemap.xml
```

### Structured data (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "…",
  "datePublished": "2026-01-15"
}
</script>
```

### SSR/SSG for SPAs

- Critical content in **initial HTML** — Google renders JS but slower and not guaranteed for all bots
- See [[Nginx/nginx SPA deployment]] for prerender/static fallbacks

### Measure

```bash
# PageSpeed Insights API / UI — field + lab
# Google Search Console — coverage, CWV, queries
npx lighthouse https://example.com --only-categories=seo,performance
```

References:

- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pages not indexed | Search Console coverage | robots/noindex; canonical to wrong URL |
| Duplicate titles | CMS defaults | Unique `<title>` per URL |
| Soft 404 | Thin content + 200 | Real content or 404 status |
| CWV poor | CrUX report | Fix LCP/INP/CLS per rendering notes |
| JS content missing in index | View rendered HTML | SSR/prerender critical content |
| hreflang wrong | International targeting | Valid language/region pairs |

## Gotchas

> [!WARNING]
> **`noindex` in staging** leaking to prod via env mistake — instant de-indexing.

- **Canonical to homepage** on all pages — common SPA bug; each URL needs self-canonical unless duplicate.
- **Infinite faceted URLs** — crawl budget waste; `noindex` or consolidate params.
- **AI-generated thin pages** — quality beats volume; manual review for E-E-A-T.

## When NOT to use

- Don't SEO spam internal tools behind auth — `noindex` and save effort.
- Keyword stuffing — hurts readability and can trigger quality demotion.

## Related

[[Descriptive/web development]] [[Rendering performance/INP]] [[Nginx/nginx SPA deployment]] [[Security/https]]
