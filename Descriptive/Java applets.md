[[Descriptive]] [[JavaScript]] [[web capabilities]] [[TLS (Transport Layer Security)]] [[CORS (Cross Origin Request Sharing)]]

# Java applets

> Historical browser plug-in model (1990s–2010s) — **removed from all major browsers** because the security boundary was unsalvageable.

```txt
        Java applets ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Applets are historical

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Technical Details
### Recognize legacy artifacts

```html
<!-- Dead pattern — do not revive -->
<applet code="PayApplet.class" archive="pay.jar" width="400" height="300">
  <param name="account" value="...">
</applet>
```

```bash
# Archaeology only — modern JDK has no plugin
# javap -c PayApplet.class   # inspect bytecode if migrating
```

### Migration checklist (when you inherit applet docs)

```txt
1. Identify business function (signing, printing, device access)
2. Map to modern API: Web Crypto, WebUSB ( gated ), native app, or server-side
3. Remove JRE install requirements from runbooks
4. Audit PCI/SOC controls that assumed applet isolation
```

## Mistakes to Avoid
> [!WARNING]
> **Do not recommend applet revival** for any new system — compliance and browser support are zero.

> [!WARNING]
> **Java Web Start** followed same fate — not a drop-in for applets in 2026.

> [!WARNING]
> **Internal wikis still link JRE 8 32-bit** — update onboarding docs to prevent wasted eng days.

| Symptom | Check | Fix |
|---------|-------|-----|
| "Java blocked" / plugin missing | Browser version | Retire feature; no plugin reinstall path |
| Enterprise site requires Java 6 | Legacy vendor | Escalate vendor rewrite; isolate in Citrix/VDI temp |
| Security scan flags applet | Compliance | Document decommission; remove HTML embed |
| Signed jar trust prompts | Old cert chain | Not fixable in browser — replace integration |

## Pros/Cons or Trade-offs
- **Always** — for any new feature. Full stop.
