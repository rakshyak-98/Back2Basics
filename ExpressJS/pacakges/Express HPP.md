[[ExpressJS]] [[express concepts]] [[XSRF (cross-site request forgery)]] [[Express middleware]]

# Express HPP

> HTTP Parameter Pollution (HPP) happens when duplicate query or body keys (`?id=1&id=2`) are parsed inconsistently — `hpp` middleware removes polluted duplicates so your validation sees a single value.

---

## Attack shape

```txt
?role=user&role=admin  →  sanitize  →  single role value
```

Different stacks treat duplicate keys as last-wins, first-wins, or arrays. An attacker may send conflicting values hoping the WAF sees one value and your application sees another.

---

## Usage

```js
import hpp from 'hpp'
app.use(hpp()) // typically after body parsers
```

| Option | When to use |
|--------|-------------|
| Whitelist | Legitimate multi-value keys (e.g. `?tag=a&tag=b`) |
| Mount order | After `express.json()` and `express.urlencoded()` |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Legitimate multi-value params stripped | Over-aggressive HPP | Whitelist those keys |
| Arrays still appear | HPP not mounted | Confirm middleware order |
| Bypass via POST body | Only query sanitized | Apply consistently to body |

HPP middleware is **not** a WAF — still validate types and enforce authorization.

---

## Related

[[express concepts]] · [[Express middleware]] · [[XSRF (cross-site request forgery)]]
