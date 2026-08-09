[[Streaming]] [[HLS]] [[DASH]] [[CMAF]] [[ABR]] [[MPD]]

# HLS vs. DASH

> HLS and DASH both do ABR over HTTP — pick by device reach, then share segments with CMAF when you need both.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Same job (adaptive HTTP streaming); different playlist shape and default ecosystems — Apple leans HLS; open MPEG is DASH.

```txt
                    ┌── HLS  → .m3u8  → Safari / iOS / many TVs
 Encoder / packager ┤
                    └── DASH → .mpd   → Android / Chrome / Smart TVs
                              ▲
                         [[CMAF]] .m4s shared
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **HLS** | Apple’s HTTP Live Streaming | “HLS is the safe default wherever Safari matters.” |
| **DASH** | MPEG Dynamic Adaptive Streaming over HTTP | “DASH is the open MPD-based ABR protocol.” |
| **Manifest** | Playlist metadata | “HLS uses m3u8; DASH uses MPD XML.” |
| **CMAF** | Shared fMP4 segments | “One segment store, two manifests — that’s CMAF.” |
| **Native vs MSE** | OS player vs JS/MSE | “Safari plays HLS natively; DASH usually needs MSE.” |
| **LL-HLS / low-latency DASH** | Live delay cutters | “Latency is a packaging choice, not ‘DASH is always faster’.” |

### Side-by-side (say this table out loud)

| Topic | [[HLS]] | [[DASH]] |
|-------|---------|----------|
| Spec owner | Apple (RFC 8216 + extensions) | MPEG / ISO open standard |
| Manifest | `.m3u8` text | `.mpd` XML ([[MPD]]) |
| Classic segments | MPEG-TS or fMP4 | fMP4 / ISO BMFF |
| Apple devices | Native, required path | No native Safari DASH |
| Codec flexibility | Strong, Apple-guided | Broad profiles |
| Typical live latency | Higher unless LL-HLS | Can be low with short segments / CMAF |
| Industry default | “Works on iPhone” | “Works on Android + open tooling” |

### Decision in one line

- Need **Safari / iOS** → ship [[HLS]] (add DASH only if you must).
- Need **max open / Android-centric** → [[DASH]], still offer HLS for Apple.
- Need **both without double storage** → [[CMAF]] shared `.m4s` + dual manifests.

---

## Standard config / commands

### Dual-package layout (what good looks like)

```txt
/origin/title/
  init.mp4
  video_720p_00001.m4s   # shared
  video_720p_00002.m4s
  master.m3u8            # HLS
  manifest.mpd           # DASH BaseURL → same .m4s
```

### Player pick (product sketch)

```js
// Interview answer: feature-detect, don’t hard-code one protocol
const useHls = supportsNativeHls() || !supportsMseDash()
load(useHls ? '/master.m3u8' : '/manifest.mpd')
```

| Knob | Why it matters |
|------|----------------|
| One encode ladder | Same [[ABR]] rungs in both manifests |
| Aligned GOP / duration | Clean switches in either player |
| DRM mapping | FairPlay↔HLS, Widevine↔DASH (often both) |
| CDN cache keys | Don’t cache live manifests like VoD |
| Relative segment URLs | Survive CDN/proxy path rewrites |

```bash
# Sanity: both manifests resolve the same first media object
curl -sI "https://cdn/.../video_720p_00001.m4s"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| iOS black, Android fine | Only DASH published | Add [[HLS]] or CMAF dual |
| Android fine in app, Safari fails same URL | Feeding `.mpd` to Safari | Detect and serve `.m3u8` |
| Double CDN bill | Separate TS + DASH files | Move to [[CMAF]] shared segments |
| HLS sync, DASH A/V drift | Different segment durations | One packager timeline |
| DRM works on one protocol only | Key system / PSSH mismatch | Multi-DRM pack; see [[DRM]] |
| “DASH is lower latency” but measured same | Same segment size both sides | Shorten segments or enable LL features |
| ABR differs wildly between players | Different `BANDWIDTH` / Representation | Align advertised bitrates |

---

## Gotchas

> [!WARNING]
> **“DASH is open so we skip HLS”** — you just lost Safari unless you dual-package.

> [!WARNING]
> **Old blog: HLS = TS only, DASH = always lower latency** — modern HLS is fMP4/CMAF; latency is packaging, not brand name.

> [!WARNING]
> **Two ladders, two GOPs** — “HLS vs DASH” bugs are often encode drift, not protocol dogma.

> [!WARNING]
> **Citation bingo in design docs** — interviewers want device matrix + CMAF plan, not Mux-vs-Wowza link dumps.

---

## When NOT to use

- **This comparison as a runtime switch every request** — pick packaging once; feature-detect at the player.
- **Ultra-low-latency calls** — neither replaces [[WebRTC]].
- **Single internal mezzanine** — protocol choice belongs at **egress**, not archive.

---

## Related

[[HLS]] [[DASH]] [[CMAF]] [[ABR]] [[MPD]] [[Manifest (streaming)]] [[DRM]] [[MPEG-TS]] [[Streaming]]
