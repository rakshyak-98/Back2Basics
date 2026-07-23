[[Data structure/dsa genera formula]] [[ML/Model/Linear regression]] [[javascript]] [[general]]

# Percentage calculation

> Mental math and code patterns for `%` of a value, change, and reverse-percent — **on-call sizing + discount math without a calculator**.

## Mental model

**Percent = parts per hundred.** Three operations cover 90% of production math:

```
Part   = Whole × (Rate / 100)
Rate   = (Part / Whole) × 100
Whole  = Part / (Rate / 100)
```

**Percent change:** `(new − old) / old × 100` — use **old** as baseline unless stated otherwise.

```
240 whole, find 15%:
  10% of 240 = 24   (move decimal left 1)
  5%  of 240 = 12   (half of 10%)
  15%       = 36
```

## Standard config / commands

### Quick mental table (anchor on 10%)

| % | Trick | Example on 240 |
|---|-------|----------------|
| 5% | 10% ÷ 2 | 12 |
| 15% | 10% + 5% | 36 |
| 20% | 10% × 2 | 48 |
| 30% | 10% × 3 | 72 |
| 33⅓% | ÷ 3 | 80 |
| 40% | 10% × 4 | 96 |
| 60% | 50% + 10% | 144 |
| 66⅔% | ×2 then ÷ 3 | 160 |
| 125% | 100% + 25% | 300 |

### JavaScript (money — use integers or decimal lib)

```javascript
// Prefer integer cents
const pctOf = (wholeCents, rate) => Math.round(wholeCents * rate / 100);

// Display
const formatPct = (n, d) => ((n - d) / d * 100).toFixed(2) + '%';

// Reverse: price after 20% off was $80 → original?
const original = 80 / (1 - 20 / 100); // 100
```

### SQL share of total

```sql
SELECT category,
       100.0 * SUM(amount) / SUM(SUM(amount)) OVER () AS pct
FROM sales
GROUP BY category;
```

### Error / margin percent (ops)

```javascript
const errorRate = (errors / requests) * 100;
const slaBudgetMs = latencyP99 * 0.01; // 1% of p99 as micro-budget example
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Off-by-one cent | Float `0.1 + 0.2` | Integer cents or `decimal.js` |
| Wrong baseline in change % | Denominator | Use old value for growth; specify clearly in dashboards |
| Percentages sum to 99.9% | Rounding per row | Round last row to 100% or use largest remainder |
| "50% faster" confusion | Relative vs absolute | 50% faster = half the time, not zero time |
| Tip/tax double-applied | Compound order | Define order: pre-tax vs post-tax |

## Gotchas

> [!WARNING]
> **Percentage points ≠ percent change.** Rate 5% → 7% is **+2 percentage points**, not +2% (that's +40% relative change).

- **Stacked discounts:** 20% off then 10% off ≠ 30% off — multiply complements: `0.8 × 0.9 = 0.72`.
- **Uptime:** 99.9% allows ~43 min/month downtime — don't advertise "100%".
- **Chart axes** starting above zero exaggerate percent moves.

## When NOT to use

- Statistical significance — use proper tests, not raw % delta on tiny samples.
- GPU/memory "percent" in monitoring — know if it's of host, cgroup limit, or pod request.

## Related

[[Data structure/dsa genera formula]] [[javascript]] [[general]] [[ML/Model/Linear regression]]
