[[DASH]] [[Manifest (streaming)]] [[HLS vs. DASH]] [[CMAF]] [[ABR]] [[DRM]] [[EME]]

# MPD (Media Presentation Description)

> DASH manifest XML — **ISO/IEC 23009-1** index for adaptive HTTP streaming; player reads this before any segment.

---

## Mental model

The **MPD** is the **root document** for **[[DASH]]** playback. It describes **Periods** (timeline slices), **AdaptationSets** (video/audio/subtitle tracks), and **Representations** (bitrate rungs). Players fetch the MPD, pick a Representation, then request **segments** via `SegmentTemplate`, `SegmentList`, or `SegmentBase`.

```txt
GET manifest.mpd
    │
Parse Period / AdaptationSet / Representation
    │
Estimate bandwidth + buffer ──► pick Representation (720p @ 3 Mbps)
    │
GET init.mp4 + seg_1.m4s + seg_2.m4s … ([[CMAF]] fMP4 typical)
```

| Element | Purpose |
|---------|---------|
| **Period** | Time window (live sliding or VoD full) |
| **AdaptationSet** | Group of same content type (video H.264) |
| **Representation** | One ladder rung (`bandwidth`, `width`, `codecs`) |
| **SegmentTemplate** | URL pattern `$Number$`, duration, timescale |
| **ContentProtection** | [[DRM]] PSSH / license hints for [[EME]] |

**Static MPD** (VoD): full timeline known. **Dynamic MPD** (live): `type="dynamic"`, `availabilityStartTime`, `minimumUpdatePeriod`, `timeShiftBufferDepth`.

---

## Standard config / commands

### Minimal static VoD MPD (single representation)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" type="static" mediaPresentationDuration="PT10M"
     profiles="urn:mpeg:dash:profile:isoff-live:2011">
  <Period>
    <AdaptationSet mimeType="video/mp4" codecs="avc1.64001f" contentType="video">
      <Representation id="720p" bandwidth="3000000" width="1280" height="720">
        <SegmentTemplate media="seg_$Number$.m4s" initialization="init.mp4"
          startNumber="1" duration="120" timescale="30"/>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
```

`duration="120"` @ `timescale="30"` → 4 second segments.

### Multi-bitrate AdaptationSet (ABR)

```xml
<AdaptationSet contentType="video" codecs="avc1.640028" maxWidth="1920" maxHeight="1080">
  <Representation id="1080" bandwidth="5800000" width="1920" height="1080"/>
  <Representation id="720"  bandwidth="3000000" width="1280" height="720"/>
  <SegmentTemplate media="$RepresentationID$/seg_$Number$.m4s"
    initialization="$RepresentationID$/init.mp4" duration="120" timescale="30"/>
</AdaptationSet>
```

### Live dynamic MPD attributes

```xml
<MPD type="dynamic" publishTime="2026-07-22T12:00:00Z"
     minimumUpdatePeriod="PT2S" suggestedPresentationDelay="PT6S"
     timeShiftBufferDepth="PT30M" availabilityStartTime="2026-07-22T11:00:00Z">
```

| Attribute | Why |
|-----------|-----|
| `minimumUpdatePeriod` | How often player re-fetches MPD |
| `suggestedPresentationDelay` | Live edge offset from availability |
| `timeShiftBufferDepth` | DVR window |

### Widevine ContentProtection snippet

```xml
<ContentProtection schemeIdUri="urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed" value="cenc"/>
```

Pair with Shaka/Bitmovin + license server — see [[DRM]] / [[EME]].

### Validate & debug

```bash
curl -s "https://origin/manifest.mpd" | xmllint --format -
# Shaka Player debug: chrome://media-internals or player.getStats()
mpd-parser-cli manifest.mpd   # @streaming/mpd-parser npm, if available
```

### Shared segments with HLS

Same `init.mp4` + `.m4s` files — [[CMAF]] — map HLS `#EXT-X-MAP` URI to MPD `initialization`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Player 404 segments | `$Number$` base URL wrong | `BaseURL` element; CDN path prefix |
| Live drift / buffer grow | `publishTime` stale | Packager must refresh dynamic MPD |
| ABR always lowest | `bandwidth` too high vs actual | Match encoded bitrates ([[bitrate streaming]]) |
| Init segment loop | Wrong `@presentationTimeOffset` | Regenerate MPD from packager |
| DRM session fail | Missing PSSH in init | Re-pack with CENC; verify [[EME]] |
| Period gap at splice | Multi-period VoD | `#EXT-X-DISCONTINUITY` equivalent — `Period@start` |
| MPD parse error | XML namespace | Valid `xmlns`; escape special chars |

---

## Gotchas

> [!WARNING]
> **Hand-edited MPD vs packager output** — drift causes segment index mismatch; treat MPD as generated artifact.

> [!WARNING]
> **`bandwidth` excludes audio** — combine video+audio bandwidth or separate AdaptationSets correctly.

> [!WARNING]
> **Dynamic MPD cached at CDN** — must not cache like VoD; `Cache-Control: no-cache`.

> [!WARNING]
> **Segment timeline `@timescale`** — off-by-one timescale bugs → micro-stutter every N segments.

---

## When NOT to use

- **Safari-primary without HLS** — ship [[HLS]] or dual manifest ([[HLS vs. DASH]]).
- **Sub-second live** — DASH segment model adds latency; LL-HLS or WebRTC.
- **Raw TS progressive** — use HLS TS manifests instead.

---

## Related

[[DASH]] [[Manifest (streaming)]] [[HLS]] [[CMAF]] [[ABR]] [[DRM]] [[EME]] [[HLS vs. DASH]]
