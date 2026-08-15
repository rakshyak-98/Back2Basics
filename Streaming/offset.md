[[Streaming]] [[MPD]] [[Manifest (streaming)]] [[DASH]] [[HLS]] [[Byte stream]] [[MPEG-TS]] [[CMAF]]

# offset

> An offset is how far you move from a known start — bytes in a file, or time from a timeline base in live DASH/HLS.

## Interview Relevance

Interviewers probe whether you can walk offset end-to-end — not just name it. Signal fluency with **Byte offset**, **presentationTimeOffset**, **suggestedPresentationDelay**, **Range request** and when you would pick a different path.

## Sources

- [Wikipedia — offset](https://en.wikipedia.org/wiki/offset) — overview

## Key Concepts

- **Byte offset:** Bytes from start of file/object — “We seek to offset 1024 in the segment file.”
- **presentationTimeOffset:** DASH time shift on a Representation — “PTO aligns segment timeline to the Period.”
- **suggestedPresentationDelay:** How far behind live edge to play — “We sit a few seconds off the edge for stability.”
- **Range request:** HTTP partial GET by bytes — “CDN serves bytes=start-end from the object.”
- **Index / element offset:** Position in an array (not bytes) — “Don’t confuse index 3 with byte 3.”
- **Base + offset addressing:** Classic pointer math — “Effective address = base register + offset.”
- **Context:** What “offset” means — Unit
- **Segment / object:** Position inside `.m4s` / `.ts` / MP4 — Bytes
- **DASH MPD:** `presentationTimeOffset` on timeline — Timescale ticks
- **Live edge:** Delay from availability time — Seconds
- **File / VOD seek:** Jump into progressive or archive file — Bytes or time
- **Buffers / parsers:** Start index in a byte buffer — Bytes
- **Generic arrays:** Elements from index 0 — Count

### Contexts you’ll meet (streaming first)

| Context | What “offset” means | Unit | Example |
|---------|---------------------|------|---------|
| **Segment / object** | Position inside `.m4s` / `.ts` / MP4 | Bytes | `Range: bytes=0-1023` init probe |
| **DASH MPD** | `presentationTimeOffset` on timeline | Timescale ticks | Align mid-roll Period |
| **Live edge** | Delay from availability time | Seconds | `suggestedPresentationDelay=PT6S` |
| **File / VOD seek** | Jump into progressive or archive file | Bytes or time | Player seek bar → byte map |
| **Buffers / parsers** | Start index in a byte buffer | Bytes | PES parse from `base + n` |
| **Generic arrays** | Elements from index 0 | Count | `'d'` at offset 3 in `[a,b,c,d]` |

## Technical Details

```txt
Base ──────────────────────────────►
      |---- offset ----|
                       ▼
                    target (byte / PTS / live edge delay)
```

### HTTP byte range (CDN / origin)

```bash
curl -sI -H "Range: bytes=0-65535" "https://cdn.example.com/seg_100.m4s"
# Expect 206 Partial Content + Content-Range
```

### DASH timing offsets (live)

```xml
<MPD type="dynamic" suggestedPresentationDelay="PT6S"
     availabilityStartTime="2026-07-22T11:00:00Z">
  <Period>
    <AdaptationSet>
      <Representation>
        <!-- presentationTimeOffset shifts media timeline onto Period -->
        <SegmentTemplate timescale="90000" presentationTimeOffset="900000" …/>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
```

### Local file seek (ops / debug)

```bash
# Skip first 1 MiB of a capture
dd if=capture.ts bs=1M skip=1 | ffprobe -i pipe:0
```

| Knob | Why it matters |
|------|----------------|
| `presentationTimeOffset` | Wrong PTO → A/V jump or init loop |
| `suggestedPresentationDelay` | Too small → rebuffer at live edge; too big → “laggy live” |
| Byte `Range` support on CDN | Players and packagers probe objects |
| Timescale units | Off-by-factor bugs look like random drift |
| 0-based vs 1-based indexes | API docs lie; verify with a hex dump |

## Real-World Applications

Used wherever offset sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **“Offset” as a substitute for a real timestamp API** — prefer PTS/DTS or media time in player code.
- **Con / skip when:** **Hand-computing PTO in production** — let the packager own timeline math.
- **Con / skip when:** **Byte offsets into encrypted samples without cleartext maps** — use container indexes the DRM stack expects.

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| Seek lands on wrong frame | Byte vs time map; moov/sidx | Fix index; regenerate sidx |
| Live plays then jumps back | PTO / Period@start mismatch | Regenerate [[MPD]] from packager |
| Constant live rebuffer | `suggestedPresentationDelay` too aggressive | Increase delay a few seconds |
| 200 instead of 206 on Range | Origin/CDN ignores Range | Enable byte-range; don’t gzip `.m4s` |
| Init segment “loop” | Bad `@presentationTimeOffset` | Correct PTO; see [[MPD]] triage |
| Parser reads garbage | Used element index as byte offset | Multiply by element size / use bytes |
| Multi-period splice glitch | Offset between Periods | Set explicit Period `@start` |

- **Index ≠ byte offset** — `arr[3]` is the fourth element; file offset 3 is the fourth **byte**.
- **Timescale math** — `presentationTimeOffset` is in timescale ticks, not wall-clock seconds unless timescale is 1.
- **Gzip on media + Range** — many stacks break partial content; keep segments identity-encoded.
- **Signed URLs and Range** — some CDNs require the signature to cover range behavior; test 206 paths.
