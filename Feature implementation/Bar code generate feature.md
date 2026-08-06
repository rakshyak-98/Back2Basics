[[Feature implementation]]

# Bar code generate feature

> One-line: what / why for **Bar code generate feature** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```shell
npm install express bwip-js
```
```js
const express = require('express');
const bwipjs = require('bwip-js');
const app = express();
app.get("/barcode", (req, res) => {
	cosnt {code} = req.query;
	bwipjs.toBuffer({
		bcid: 'code128', // Barcode type
		text: code,
		scale: 3,
		height: 10,
		includetext: true,
		textalign: 'center',
	}, (err, png) => {
		if(err){
			return res.status(500).send('Error generating barcode');
		}
		res.setHeader('Content-Type', 'image/png');
		res.send(png);
	})
})
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
