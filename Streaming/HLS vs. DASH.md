[[Streaming]] [[HLS]] [[DASH]] [[CMAF]] [[ABR]] [[MPD]] [[Manifest (streaming)]] [[DRM]] [[MPEG-TS]]

# HLS vs. DASH

> HLS and DASH both do ABR over HTTP — pick by device reach, then share segments with CMAF when you need both.

```txt
        HLS vs. DASH ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk HLS vs. DASH end-to-end

## Sources
- [Wikipedia — HLS vs. DASH](https://en.wikipedia.org/wiki/HLS_vs._DASH) — overview

## Key Concepts
- **HLS:** Apple’s HTTP Live Streaming
- **DASH:** MPEG Dynamic Adaptive Streaming over HTTP
- **Manifest:** Playlist metadata — “HLS uses m3u8; DASH uses MPD XML.”
- **CMAF:** Shared fMP4 segments — “One segment store, two manifests — that’s CMAF.”
- **Native vs MSE:** OS player vs JS/MSE — “Safari plays HLS natively; DASH usually needs MSE.”
- **LL-HLS / low-latency DASH:** Live delay cutters
- **Topic:** [[HLS]] — [[DASH]]
- **Spec owner:** Apple (RFC 8216 + extensions) — MPEG / ISO open standard
- **Manifest:** `.m3u8` text — `.mpd` XML ([[MPD]])
- **Classic segments:** MPEG-TS or fMP4 — fMP4 / ISO BMFF
- **Apple devices:** Native, required path — No native Safari DASH
- **Codec flexibility:** Strong, Apple-guided — Broad profiles
- **Typical live latency:** Higher unless LL-HLS — Can be low with short segments / CMAF
- **Industry default:** “Works on iPhone” — “Works on Android + open tooling”

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

- **Need:** Safari:** Need **Safari / iOS** → ship [[HLS]] (add DASH only if you must).
- **Need:** max:** Need **max open / Android-centric** → [[DASH]], still offer HLS for Ap…
- **Need:** both:** Need **both without double storage** → [[CMAF]] shared `.m4s` + dual …

## Technical Details
```txt
                    ┌── HLS  → .m3u8  → Safari / iOS / many TVs
 Encoder / packager ┤
                    └── DASH → .mpd   → Android / Chrome / Smart TVs
                              ▲
                         [[CMAF]] .m4s shared
```

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

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| iOS black, Android fine | Only DASH published | Add [[HLS]] or CMAF dual |
| Android fine in app, Safari fails same URL | Feeding `.mpd` to Safari | Detect and serve `.m3u8` |
| Double CDN bill | Separate TS + DASH files | Move to [[CMAF]] shared segments |
| HLS sync, DASH A/V drift | Different segment durations | One packager timeline |
| DRM works on one protocol only | Key system / PSSH mismatch | Multi-DRM pack; see [[DRM]] |
| “DASH is lower latency” but measured same | Same segment size both sides | Shorten segments or enable LL features |
| ABR differs wildly between players | Different `BANDWIDTH` / Representation | Align advertised bitrates |

- **Mistake:** **“DASH is open so we skip HLS”**
- **Mistake:** **Old blog: HLS = TS only, DASH = always lower latency**
- **Mistake:** **Two ladders, two GOPs**
- **Mistake:** **Citation bingo in design docs**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **This comparison as a runtime switch every request**
- **Con / skip when:** **Ultra-low-latency calls**
- **Con / skip when:** **Single internal mezzanine**

## Comparison
- vs [[WebRTC]]: **Ultra-low-latency calls** — neither replaces [[WebRTC]].


### Use cases
- Used wherever HLS vs
