[[Streaming]] [[ABR]] [[HLS]] [[MPD]] [[CMAF]] [[Manifest (streaming)]] [[HLS vs. DASH]] [[DRM]] [[EME]] [[bitrate streaming]]

# DASH (Dynamic Adaptive Streaming over HTTP)

> DASH serves the same idea as HLS over HTTP — an [[MPD]] menu plus segments — as an open MPEG standard.

```txt
        DASH (Dynamic Adap ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk DASH end-to-end

## Sources
- [Wikipedia — DASH](https://en.wikipedia.org/wiki/DASH) — overview
- [DASH Industry Forum](https://dashif.org/) — overview
- [ISO/IEC 23009-1 DASH](https://www.iso.org/standard/83314.html) — deep-dive

## Key Concepts
- **MPD:** XML root playlist — “DASH starts with the Media Presentation Description.”
- **Period:** Time slice of the show — “Live and VoD are Periods on a timeline.”
- **AdaptationSet:** Group of same media type — “Video Adaptations hold the ABR ladder.”
- **Representation:** One quality rung — “Each Representation is a bitrate/resolution choice.”
- **SegmentTemplate:** URL pattern with `$Number$`
- **Dynamic vs static:** Live refresh vs fixed VoD

**Flow:**

- **Note:** 1. **Encode** — [[ABR]] ladder into shared fMP4 when possible ([[CMAF]]).
- **Note:** 2. **Describe** — generate [[MPD]] with Representations + timing.
- **Note:** 3. **Fetch** — player picks Representation from bandwidth + buffer.
- **Note:** 4. **Adapt** — next segment from another Representation at a switch point.

### Tooling you will hear

| Tool | Role |
|------|------|
| Bitmovin / Shaka packager | Package + play |
| AWS Elemental MediaConvert / MediaPackage | Managed ladder + MPD |
| ffmpeg + mp4box / Bento4 | DIY segment + MPD |


- **Core:** Like [[HLS]], DASH rides **plain HTTP** through CDNs and firewalls. Unlike HL…

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

- `duration="120"` @ `timescale="30"` → 4 s segments.

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

- **Mistake:** **Hand-edited MPD drifts from segments**
- **Mistake:** **Caching a dynamic MPD like VoD**
- **Mistake:** **DASH-only greenfield kills iOS**
- **`bandwidth` forgetting audio**::** → rebuffer

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **iOS / Safari-first with no dual package**
- **Con / skip when:** **Interactive sub-second**
- **Con / skip when:** **Legacy Apple-only TS devices**

## Comparison
- vs [[HLS]]: **iOS / Safari-first with no dual package** — use [[HLS]] (or HLS+DASH via [[CMAF]]).
- vs [[WebRTC]]: **Interactive sub-second** — [[WebRTC]], not segment DASH.


### Use cases
- Like [[HLS]], DASH rides **plain HTTP** through CDNs and firewalls. Unlike HL…

- Used wherever DASH sits in an ingest → package → CDN → player path
