[[orm]] [[mysql]] [[mysql connection]]

# sequalizer

> Sequelize model hooks — run code around validate/save so invariants (slug, password hash) stay in one place.

---

## Index

- [[#Mental model]]
- [[#Interview map (words you can say)]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Hooks fire on model lifecycle events; bulk `update`/`destroy` skip them unless `individualHooks: true`; hash passwords in `beforeSave` only when `changed('password')`.

```txt
save/validate ──► beforeSave hook ──► DB write
bulk update ──► hooks skipped (default) ──► need individualHooks
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Hook** | Lifecycle callback on the model | “Hash password in beforeSave, not in every route.” |
| **individualHooks** | Run hooks per row on bulk ops | “Default bulk update skips hooks.” |
| **changed(field)** | Dirty check | “Avoid double-hashing on profile update.” |
| **addHook** | Attach after init | “Same as hooks: { … } in init.” |

---

## Standard config / commands

```js
Product.addHook('beforeValidate', (product) => {
  if (product.name) {
    product.slug = product.name.toLowerCase().replace(/ /g, '-')
  }
})

User.init({
  username: DataTypes.STRING,
  password: { type: DataTypes.STRING, allowNull: false },
}, {
  sequelize,
  modelName: 'user',
  hooks: {
    beforeSave: async (user) => {
      if (user.changed('password')) {
        user.password = await bcrypt.hash(user.password, 10)
      }
    },
  },
})
```

| Knob | Why it matters |
|------|----------------|
| `individualHooks: true` | Bulk update/destroy runs per-row hooks |
| `changed('password')` | Prevents hashing an already-hashed value |
| Hook body weight | Keep light — no email/PDF in hooks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slug/hash missing on bulk update | Hooks skipped | `individualHooks: true` or loop saves |
| Login fails after profile edit | Double bcrypt | Guard with `changed('password')` |
| Seeds send emails | Side effects in hooks | Move I/O out; feature-flag hooks |
| Hook order surprises | Multiple hooks same event | Document order; consolidate |

---

## Gotchas

> [!WARNING]
> **Bulk ops ≠ instance hooks** — the #1 Sequelize production footgun.

> [!WARNING]
> **Migrations/seeds fire hooks** — don’t put notifications inside `beforeCreate`.

---

## When NOT to use

- **Cross-service workflows** — use domain services/outbox, not model hooks.
- **Query-heavy logic** — hooks that query half the DB on every save will melt.

---

## Related

[[mysql connection]] [[mysql]] [[database seeding]] [[migration]]
