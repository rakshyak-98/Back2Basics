[[Streaming]] [[ABR]] [[HLS]] [[MPD]] [[CMAF]] [[Manifest (streaming)]] [[HLS vs. DASH]] [[DRM]] [[EME]] [[bitrate streaming]]

# DASH (Dynamic Adaptive Streaming over HTTP)

> DASH serves the same idea as HLS over HTTP — an [[MPD]] menu plus segments — as an open MPEG standard.





## Interview Relevance
Interviewers probe whether you can walk DASH end-to-end — not just name it. Signal fluency with **MPD**, **Period**, **AdaptationSet**, **Representation** and when you would pick a different path.

## Sources
- [Wikipedia — DASH](https://en.wikipedia.org/wiki/DASH) — overview
- [DASH Industry Forum](https://dashif.org/) — overview
- [ISO/IEC 23009-1 DASH](https://www.iso.org/standard/83314.html) — deep-dive

## Core Definition
Like [[HLS]], DASH rides **plain HTTP** through CDNs and firewalls. Unlike HLS, Apple Safari does **not** play DASH natively — plan dual packaging or HLS-only for iOS.

## Key Concepts
- **MPD:** XML root playlist — “DASH starts with the Media Presentation Description.”
- **Period:** Time slice of the show — “Live and VoD are Periods on a timeline.”
- **AdaptationSet:** Group of same media type — “Video Adaptations hold the ABR ladder.”
- **Representation:** One quality rung — “Each Representation is a bitrate/resolution choice.”
- **SegmentTemplate:** URL pattern with `$Number$` — “We don’t list every file; the template builds URLs.”
- **Dynamic vs static:** Live refresh vs fixed VoD — “Dynamic MPD must be re-fetched; static is complete.”

**Flow:**

1. **Encode** — [[ABR]] ladder into shared fMP4 when possible ([[CMAF]]).
2. **Describe** — generate [[MPD]] with Representations + timing.
3. **Fetch** — player picks Representation from bandwidth + buffer.
4. **Adapt** — next segment from another Representation at a switch point.

### Tooling you will hear

| Tool | Role |
|------|------|
| Bitmovin / Shaka packager | Package + play |
| AWS Elemental MediaConvert / MediaPackage | Managed ladder + MPD |
| ffmpeg + mp4box / Bento4 | DIY segment + MPD |

## Technical Details
```txt
GET manifest.mpd  ([[MPD]])
        │
  Period → AdaptationSet → Representation (bitrate rung)
        │
  SegmentTemplate / List / Base
        │
  init.mp4 + seg_N.m4s  ([[CMAF]] typical) ──► decode & play
```

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

## Real-World Applications
Like [[HLS]], DASH rides **plain HTTP** through CDNs and firewalls. Unlike HLS, Apple Safari does **not** play DASH natively — plan dual packaging or HLS-only for iOS.

Used wherever DASH sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **iOS / Safari-first with no dual package** — use [[HLS]] (or HLS+DASH via [[CMAF]]).
- **Con / skip when:** **Interactive sub-second** — [[WebRTC]], not segment DASH.
- **Con / skip when:** **Legacy Apple-only TS devices** — HLS TS path may be mandatory.

## Comparison
- vs [[HLS]]: **iOS / Safari-first with no dual package** — use [[HLS]] (or HLS+DASH via [[CMAF]]).
- vs [[WebRTC]]: **Interactive sub-second** — [[WebRTC]], not segment DASH.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on every segment | `$Number$` / `BaseURL` wrong | Fix template paths; CDN prefix |
| Safari won’t play | No HLS sibling | Ship [[HLS]] or dual [[CMAF]] package |
| Live buffer grows / drifts | Stale dynamic MPD at CDN | `Cache-Control: no-cache` on MPD |
| Always lowest quality | `bandwidth` too high | Match real encode ([[bitrate streaming]]) |
| Init loop / decode fail | Bad init or `presentationTimeOffset` | Regenerate from packager |
| DRM fail | Missing PSSH / license | Align [[DRM]] + [[EME]] |
| Parse error | Broken XML / namespace | Validate `xmlns`; escape entities |

- **Hand-edited MPD drifts from segments** — treat the MPD as a generated artifact, not a hand-tuned config forever.
- **Caching a dynamic MPD like VoD** — viewers stick on a dead live edge.
- **DASH-only greenfield kills iOS** — always ask “where does Safari play?”
- **`bandwidth` forgetting audio** — player thinks the rung is cheaper than it is → rebuffer.
