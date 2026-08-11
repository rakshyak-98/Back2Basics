[[Descriptive]] [[JavaScript]] [[web capabilities]]

# Java applets

> Historical browser plug-in model (1990s–2010s) — **removed from all major browsers** because the security boundary was unsalvageable.

---

## Mental model

```txt
Browser page → <applet> → JVM plugin in browser process → bytecode + full OS API
```

Applets ran **untrusted remote code** with near-native privileges inside the user's browser. Sandboxing relied on the Java SecurityManager — repeatedly bypassed via deserialization bugs, reflection, and JRE flaws.

**Timeline for SEs:**
- **Pre-2015:** enterprise apps (banking, intranet) still shipped `.jar` applets
- **2017:** Oracle deprecated the Java browser plugin
- **2021+:** browsers removed NPAPI/plugin support entirely

**Replacement patterns:** static web apps, [[JavaScript]] SPAs, WebStart (also dead), desktop installers, or **WebAssembly** for compute-heavy client work — none replicate "download bytecode and run with legacy JRE in Chrome."

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Java blocked" / plugin missing | Browser version | Retire feature; no plugin reinstall path |
| Enterprise site requires Java 6 | Legacy vendor | Escalate vendor rewrite; isolate in Citrix/VDI temp |
| Security scan flags applet | Compliance | Document decommission; remove HTML embed |
| Signed jar trust prompts | Old cert chain | Not fixable in browser — replace integration |

---

## Gotchas

> [!WARNING]
> **Do not recommend applet revival** for any new system — compliance and browser support are zero.

> [!WARNING]
> **Java Web Start** followed same fate — not a drop-in for applets in 2026.

> [!WARNING]
> **Internal wikis still link JRE 8 32-bit** — update onboarding docs to prevent wasted eng days.

---

## When NOT to use

- **Always** — for any new feature. Full stop.

---

## Related

[[JavaScript]] · [[web capabilities]] · [[TLS (Transport Layer Security)]] · [[CORS (Cross Origin Request Sharing)]]
