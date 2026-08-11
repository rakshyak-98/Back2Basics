[[Streaming]] [[ABR]] [[HLS]] [[MPD]] [[CMAF]] [[Manifest (streaming)]]

# DASH (Dynamic Adaptive Streaming over HTTP)

> DASH serves the same idea as HLS over HTTP — an [[MPD]] menu plus segments — as an open MPEG standard.

---

## Mental model

**Say it in one breath:** Player downloads an XML MPD, picks a Representation, then GETs init + media segments — quality can change mid-play.

```txt
GET manifest.mpd  ([[MPD]])
        │
  Period → AdaptationSet → Representation (bitrate rung)
        │
  SegmentTemplate / List / Base
        │
  init.mp4 + seg_N.m4s  ([[CMAF]] typical) ──► decode & play
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MPD** | XML root playlist | “DASH starts with the Media Presentation Description.” |
| **Period** | Time slice of the show | “Live and VoD are Periods on a timeline.” |
| **AdaptationSet** | Group of same media type | “Video Adaptations hold the ABR ladder.” |
| **Representation** | One quality rung | “Each Representation is a bitrate/resolution choice.” |
| **SegmentTemplate** | URL pattern with `$Number$` | “We don’t list every file; the template builds URLs.” |
| **Dynamic vs static** | Live refresh vs fixed VoD | “Dynamic MPD must be re-fetched; static is complete.” |

### How the story goes (4 steps)

1. **Encode** — [[ABR]] ladder into shared fMP4 when possible ([[CMAF]]).
2. **Describe** — generate [[MPD]] with Representations + timing.
3. **Fetch** — player picks Representation from bandwidth + buffer.
4. **Adapt** — next segment from another Representation at a switch point.

> [!INFO]
> Like [[HLS]], DASH rides **plain HTTP** through CDNs and firewalls. Unlike HLS, Apple Safari does **not** play DASH natively — plan dual packaging or HLS-only for iOS.

### Tooling you will hear

| Tool | Role |
|------|------|
| Bitmovin / Shaka packager | Package + play |
| AWS Elemental MediaConvert / MediaPackage | Managed ladder + MPD |
| ffmpeg + mp4box / Bento4 | DIY segment + MPD |

---

## Standard config / commands

### Minimal static VoD MPD (one Representation)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" type="static"
     mediaPresentationDuration="PT10M"
     profiles="urn:mpeg:dash:profile:isoff-live:2011">
  <Period>
    <AdaptationSet mimeType="video/mp4" contentType="video">
      <Representation id="720p" bandwidth="3000000" width="1280" height="720"
                      codecs="avc1.64001f">
        <SegmentTemplate media="seg_$Number$.m4s" initialization="init.mp4"
          startNumber="1" duration="120" timescale="30"/>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
```

`duration="120"` @ `timescale="30"` → 4 s segments.

### Live dynamic knobs

```xml
<MPD type="dynamic" minimumUpdatePeriod="PT2S"
     suggestedPresentationDelay="PT6S"
     timeShiftBufferDepth="PT30M"
     availabilityStartTime="2026-07-22T11:00:00Z">
```

| Knob | Why it matters |
|------|----------------|
| `bandwidth` on Representation | ABR math — include audio if muxed |
| `minimumUpdatePeriod` | How often live players re-GET the MPD |
| `suggestedPresentationDelay` | Distance from live edge (stability vs latency) |
| `BaseURL` | CDN prefix; wrong → 404 storm |
| `ContentProtection` | Widevine / PlayReady hooks ([[DRM]] / [[EME]]) |
| Shared `.m4s` with HLS | [[CMAF]] — one store, two manifests |

```bash
curl -s "https://origin/manifest.mpd" | xmllint --format -
# Player: Shaka / dash.js stats for Representation switches
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on every segment | `$Number$` / `BaseURL` wrong | Fix template paths; CDN prefix |
| Safari won’t play | No HLS sibling | Ship [[HLS]] or dual [[CMAF]] package |
| Live buffer grows / drifts | Stale dynamic MPD at CDN | `Cache-Control: no-cache` on MPD |
| Always lowest quality | `bandwidth` too high | Match real encode ([[bitrate streaming]]) |
| Init loop / decode fail | Bad init or `presentationTimeOffset` | Regenerate from packager |
| DRM fail | Missing PSSH / license | Align [[DRM]] + [[EME]] |
| Parse error | Broken XML / namespace | Validate `xmlns`; escape entities |

---

## Gotchas

> [!WARNING]
> **Hand-edited MPD drifts from segments** — treat the MPD as a generated artifact, not a hand-tuned config forever.

> [!WARNING]
> **Caching a dynamic MPD like VoD** — viewers stick on a dead live edge.

> [!WARNING]
> **DASH-only greenfield kills iOS** — always ask “where does Safari play?”

> [!WARNING]
> **`bandwidth` forgetting audio** — player thinks the rung is cheaper than it is → rebuffer.

---

## When NOT to use

- **iOS / Safari-first with no dual package** — use [[HLS]] (or HLS+DASH via [[CMAF]]).
- **Interactive sub-second** — [[WebRTC]], not segment DASH.
- **Legacy Apple-only TS devices** — HLS TS path may be mandatory.

---

## Related

[[Streaming]] [[MPD]] [[HLS]] [[HLS vs. DASH]] [[ABR]] [[CMAF]] [[Manifest (streaming)]] [[DRM]] [[EME]] [[bitrate streaming]]
