<!-- note-strategy: operational -->
[[Linux]] [[X Desktop Group]]

# Linux Templates Directory

> `Templates/` (often `~/Templates`) holds starter files that file managers offer via “Create Document” — empty doc skeletons, not system `/etc` templates.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** drop a file in `~/Templates`; Nautilus/Dolphin “Create Document” copies it next to you.

```txt
~/Templates/Invoice.odt
      │
      └─ file manager → Create Document → ./Invoice.odt
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Templates dir** | User skeleton docs | “XDG user dir, not `/etc`.” |
| **xdg-user-dirs** | Standard folders | “`xdg-user-dir TEMPLATES`.” |
| **Create Document** | FM action | “Copies template into cwd.” |
| **skel** | `/etc/skel` | “Different — new-user homes.” |
| **empty file** | Zero-byte template | “Still shows up as a type.” |

---

## Standard config / commands

```bash
xdg-user-dir TEMPLATES
mkdir -p "$(xdg-user-dir TEMPLATES)"
cp ~/Forms/offer.md "$(xdg-user-dir TEMPLATES)/"
# ~/.config/user-dirs.dirs → XDG_TEMPLATES_DIR
cat ~/.config/user-dirs.dirs
```

| Knob | Why it matters |
|------|----------------|
| `XDG_TEMPLATES_DIR` | Override path |
| File extension | Determines icon/app |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Menu empty | Dir missing/empty | Create dir; add files |
| Wrong path | `user-dirs.dirs` | Fix XDG_TEMPLATES_DIR; `xdg-user-dirs-update` |
| No menu in FM | Non-XDG FM | Use FM’s own template feature |
| Template opens not copied | Misclick | Use Create Document, not Open |

---

## Gotchas

> [!WARNING]
> **`/etc/skel` ≠ Templates** — skel seeds new homes; Templates is a per-user convenience.

> [!WARNING]
> **Cloud-synced Templates** can fight with local path expectations.

---

## When NOT to use

- **Code scaffolding** — use cookiecutter/copier, not FM templates.
- **Server provisioning** — use configuration management, not desktop Templates.

---

## Related

[[X Desktop Group]] [[user management]] [[Linux file management]]
