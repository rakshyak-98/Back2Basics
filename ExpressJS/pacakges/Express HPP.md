[[express concepts]] [[Express middleware]] [[express query handler]] [[XSRF (cross-site request forgery)]]

# Express HPP

> HTTP Parameter Pollution (HPP) is when duplicate query or body keys (`?id=1&id=2`) parse inconsistently — `hpp` middleware drops polluted duplicates so validation sees one value.

```txt
        Express HPP ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use HPP to see if you understand parser ambiguity, WAF bypass pa…

## Sources
- [hpp on npm](https://www.npmjs.com/package/hpp) — overview
- [OWASP — HTTP Parameter Pollution](https://owasp.org/www-community/attacks/HTTP_Parameter_Pollution) — deep-dive
- [Express — req.query](https://expressjs.com/en/4x/api.html#req.query) — overview

## Key Concepts
- **Pollution:** `?role=user&role=admin` — ambiguous arrays vs scalars.
- **Whitelist:** keys that must remain arrays (`tag`, `id[]`) stay multi-value.
- **Mount order:** after `express.json()` / `express.urlencoded()` so body keys are covered.
- **Not a WAF:** still validate types and enforce authorization on the chosen value.


- **Core:** Different stacks treat duplicate keys as last-wins, first-wins, or arrays

## Technical Details
```txt
?role=user&role=admin  →  sanitize  →  single role value
```

```js
import hpp from 'hpp'
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(hpp({ whitelist: ['tag'] }))
```

| Option | When to use |
|--------|-------------|
| Whitelist | Legitimate multi-value keys (`?tag=a&tag=b`) |
| Mount order | After body parsers |
| Scope | Query and body — apply consistently |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Legitimate multi-value params stripped | Over-aggressive HPP | Whitelist those keys |
| Arrays still appear | HPP not mounted | Confirm middleware order |
| Bypass via POST body | Only query sanitized | Apply after body parsers |

## Mistakes to Avoid
- **Mistake:** Mounting `hpp` before body parsers so POST pollution remains
- **Mistake:** Forgetting to whitelist intentional multi-value parameters
- **Mistake:** Treating HPP as sufficient security without authentication and a…
- **Mistake:** Comparing query values with loose equality against arrays

## Pros/Cons or Trade-offs
- **Pro:** Cheap normalization that removes a whole class of parser surprises.
- **Con:** Blind use breaks legitimate multi-select filters without a whitelist.
- **Con:** Does not stop authorization bugs if you trust the remaining value.

## Comparison
- vs input schema validation ([[express query handler]]): HPP cleans shape
- vs [[XSRF (cross-site request forgery)]]: CSRF is cross-site action
- vs WAF rules: complementary — WAF may see a different parse than Node.


### Use cases
- Public search and filter APIs, role query params on admin tools, and any endp…

- **Example:** Middleware checks `req.query.role === 'admin'` while an attacker…
