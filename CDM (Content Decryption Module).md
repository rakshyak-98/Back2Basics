[[DRM]]

# CDM (Content Decryption Module)

> CDM (Content Decryption Module) — decrypts DRM media inside a secure player sandbox.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** CDM — plain job, how I run it, how I know it’s broken.


CDM (Content Decryption Module) -> is the secure software (or hardware-baked component) responsible for decrypting DRM-protected media during playback
```txt
Encrypted Video
       |
       v
 Media Player
       |
       v
     CDM  <------ License Server
       |             ^
       |             |
       +---- Uses decryption keys
       |
       v
Decrypted frames (inside secure environment)
       |
       v
Video Decoder -> Display
```
Responsibilities
- Authenticate with the DRM system
- Process the DRM license received from the license server.
- Store decryption keys securely.
- Decrypt encrypted video/audio segments.
- Enforce DRM policies:
	- Expiration
	- Offline playback
	- HD/UHD restrictions
	- Screen recording prevention
	- HDCP requirements
Playback Flow
1. User requests video.
2. Player downloads (manifest MPD/HLS), encrypted media segments
3. Player sends license request.
4. License server returns license + decryption keys.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **CDM** | Core idea of this note | “I can explain CDM without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[DRM]]
