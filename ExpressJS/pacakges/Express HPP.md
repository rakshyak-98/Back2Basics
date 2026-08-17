[[express concepts]] [[Express middleware]] [[express query handler]] [[XSRF (cross-site request forgery)]]

# Express HPP

> HTTP Parameter Pollution (HPP) is when duplicate query or body keys (`?id=1&id=2`) parse inconsistently — `hpp` middleware drops polluted duplicates so validation sees one value.





## Interview Relevance
Interviewers use HPP to see if you understand parser ambiguity, WAF bypass patterns, and that sanitizing duplicates is not a substitute for authorization checks.

## Sources
- [hpp on npm](https://www.npmjs.com/package/hpp) — overview
- [OWASP — HTTP Parameter Pollution](https://owasp.org/www-community/attacks/HTTP_Parameter_Pollution) — deep-dive
- [Express — req.query](https://expressjs.com/en/4x/api.html#req.query) — overview

## Core Definition
Different stacks treat duplicate keys as last-wins, first-wins, or arrays. Attackers send conflicting values hoping a gateway sees one value and the application another. `hpp` normalizes to a single value (with optional whitelist for legitimate multi-value keys).

## Key Concepts
- **Pollution:** `?role=user&role=admin` — ambiguous arrays vs scalars.
- **Whitelist:** keys that must remain arrays (`tag`, `id[]`) stay multi-value.
- **Mount order:** after `express.json()` / `express.urlencoded()` so body keys are covered.
- **Not a WAF:** still validate types and enforce authorization on the chosen value.

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

## Real-World Applications
Public search and filter APIs, role query params on admin tools, and any endpoint where qs/body parsers turn duplicates into arrays that break `===` checks.

**Example:** Middleware checks `req.query.role === 'admin'` while an attacker sends `role=user&role=admin` and an older parser yields an array that passes a buggy `includes` check — HPP plus strict schema validation closes the gap.

## Pros/Cons or Trade-offs
- **Pro:** Cheap normalization that removes a whole class of parser surprises.
- **Con:** Blind use breaks legitimate multi-select filters without a whitelist.
- **Con:** Does not stop authorization bugs if you trust the remaining value.

## Comparison
- vs input schema validation ([[express query handler]]): HPP cleans shape; Zod/Joi enforce type and allowlists.
- vs [[XSRF (cross-site request forgery)]]: CSRF is cross-site action; HPP is same-request parameter ambiguity.
- vs WAF rules: complementary — WAF may see a different parse than Node.

## Mistakes to Avoid
- Mounting `hpp` before body parsers so POST pollution remains.
- Forgetting to whitelist intentional multi-value parameters.
- Treating HPP as sufficient security without authentication and authorization checks.
- Comparing query values with loose equality against arrays.
