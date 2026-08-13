[[Feature implementation]] [[ExpressJS]] [[npm]]

# Bar code generate feature

> Generate barcode images server-side with `bwip-js` — expose an HTTP endpoint that accepts a code value and returns a PNG; validate input length and charset to avoid abuse.

---

## Server endpoint

```shell
npm install express bwip-js
```

```js
const express = require('express');
const bwipjs = require('bwip-js');
const app = express();

app.get('/barcode', (req, res) => {
  const { code } = req.query;
  if (!code || String(code).length > 128) {
    return res.status(400).send('Invalid code');
  }
  bwipjs.toBuffer({
    bcid: 'code128',
    text: String(code),
    scale: 3,
    height: 10,
    includetext: true,
    textalign: 'center',
  }, (err, png) => {
    if (err) {
      return res.status(500).send('Error generating barcode');
    }
    res.setHeader('Content-Type', 'image/png');
    res.send(png);
  });
});
```

| Option | Role |
|--------|------|
| `bcid` | Barcode symbology (`code128`, `qrcode`, etc.) |
| `scale` / `height` | Output dimensions |
| `includetext` | Human-readable label under bars |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| 500 on generate | Invalid charset for symbology | Validate input; pick matching `bcid` |
| Huge images | High `scale` on long text | Cap length; tune dimensions |
| Abuse / CPU spike | Unauthenticated open endpoint | Rate limit; auth for production |

---

## Related

[[Feature implementation]] · [[ExpressJS]]
