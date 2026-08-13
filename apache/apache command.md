<!-- note-strategy: reference -->
[[apache]]

# apache command

> apache command — enables the Apache module named mod_rewrite.

---

## Index

- [[#Quick reference]]
- [[#Common commands]]
- [[#Options / flags]]
- [[#Mental model]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

## Common commands

```bash
# …
```

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Mental model

**Say it in one breath:** apache command — enables the Apache module named mod_rewrite.

```bash
sudo a2enmod rewrite;
```
- enables the Apache module named `mod_rewrite`.
- `mod_rewrite` is a built-in Apache module that allows rewriting requested URLs on the fly.
- it commonly used to convert clean URLs like `/blog/post-title` into actual internal file paths like `index.php?post=post-title`.
- it was likely disabled by default on your system, which is common for Apache installs.


---

## Examples

```bash
# …
```

## Related

[[apache]]
