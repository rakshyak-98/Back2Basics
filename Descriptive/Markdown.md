[[Descriptive]]

# Markdown

> Markdown — short field notes on what it is and how to use it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Read from markdown file]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

…

## Standard config / commands

…

## Read from markdown file

```js
import { remark } from "remark";
import { visit } from "unist-util-visit";
import fs from "fs";

const md = fs.readFileSync("README.md", "utf-8");
const tree = remark().parse(md);

// Extract all SQL code blocks
const sqlBlocks = [];
visit(tree, "code", (node) => {
  if (node.lang === "sql") {
    sqlBlocks.push(node.value.replace(/\n/g, " ").replace(/\s+/g, " ").trim());
  }
});

console.log("SQL Blocks:", sqlBlocks);

// Ready for API JSON body
const jsonBody = JSON.stringify({ query: sqlBlocks[0] });
console.log("JSON Body:", jsonBody);

```

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
