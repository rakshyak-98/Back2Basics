[[Feature implementation/Push notification integration]] [[Prisma]]

# Bar code generate feature

> Server generates barcode images (e.g. with `bwip-js`) and serves them over HTTP so clients display scannable codes without local encoder libraries.





## Interview Relevance
Interviewers ask input validation (symbology + payload), caching, and why generation often lives on the server for consistency.

## Sources
- [bwip-js documentation](https://github.com/metafloor/bwip-js) — deep-dive
- [Wikipedia — Barcode](https://en.wikipedia.org/wiki/Barcode) — overview

## Key Concepts
- **Symbology:** Code128, QR, EAN, … → choose for retail vs inventory vs tickets.
- **Payload validation:** length/charset constraints per symbology.
- **Image response:** PNG/SVG with cache headers.
- **Idempotent URL:** same input → same bytes for CDN caching.

## Technical Details
```txt
Client → GET /barcodes?type=code128&text=SKU123 → bwip-js → image/png
```

```js
// sketch
app.get("/barcodes", async (req, res) => {
  const png = await bwipjs.toBuffer({
    bcid: req.query.type,
    text: req.query.text,
    scale: 3,
    includetext: true,
  });
  res.type("png").send(png);
});
```

Reject unknown `bcid` and oversized `text` to avoid CPU abuse.

## Real-World Applications
Warehouse labels, ticket QR codes, and receipt footnotes generated at print time.

**Example:** Mobile app shows a membership QR — server signs/encodes so clients cannot mint arbitrary valid codes without auth.

## Pros/Cons or Trade-offs
- **Pro:** One encoder version for all clients.
- **Con:** CPU cost on the server; cache aggressively.

## Comparison
- vs client-side generation: offline capable but inconsistent libraries.
- vs pre-rendered assets: static files win for fixed catalogs; dynamic wins for user-specific codes.

## Mistakes to Avoid
- Trusting raw query text without length limits.
- Generating on every request with no cache for hot codes.
- Using the wrong symbology for the scanner fleet.
