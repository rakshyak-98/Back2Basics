[[Streaming]] [[DRM]] [[HLS]] [[DASH]] [[Pallycon(DoveRunner)]] [[streaming license]] [[EME]] [[CMAF]] [[flussonic]] [[Manifest (streaming)]]

# CPIX

> CPIX (Content Protection Information Exchange) is XML that hands your packager the keys and PSSH needed to encrypt media.





## Interview Relevance
Interviewers probe whether you can walk CPIX end-to-end — not just name it. Signal fluency with **CPIX**, **KID**, **CEK / PlainValue**, **PSSH** and when you would pick a different path.

## Sources
- [Wikipedia — CPIX](https://en.wikipedia.org/wiki/CPIX) — overview

## Key Concepts
- **CPIX:** XML format to exchange protection keys — “Packager speaks CPIX to the KMS.”
- **KID:** Key identifier — “Manifest and license both name the same KID.”
- **CEK / PlainValue:** The actual content encryption key (often Base64) — “Packager needs the raw key to encrypt; players get it via license.”
- **PSSH:** DRM-system init data — “We copy PSSH into DASH ContentProtection.”
- **CENC:** Common encryption of samples — “One ciphertext; multiple DRM wrappers.”
- **SPEKE:** AWS-style key exchange (CPIX-based) — “MediaConvert asks SPEKE; SPEKE returns CPIX-like material.”

specification: [DASH-IF CPIX](https://dashif.org/docs/CPIX2.3/Cpix.html). CPIX is the **key delivery document** for packaging — not the player license token ([[streaming license]]).

### Critical XML pieces

| Element | You need it for |
|---------|-----------------|
| `kid` | Identify which key; must match license requests |
| `pskc:PlainValue` / Secret | CEK for the encryptor (Base64) |
| `PSSH` | Widevine/PlayReady (etc.) signaling in the manifest |
| Content / Usage rules | Which tracks / periods this key covers |

**Without manifest signaling**, the player never knows which license server or KID to use — encryption alone is not enough.

## Technical Details
```txt
Packager / transcoder
        │  GET/POST CPIX (content id, DRM systems)
        ▼
   DRM KMS (DoveRunner, SPEKE, Axinom, …)
        │  returns cpix:CPIX XML
        ▼
   Extract: KID + CEK + PSSH (+ system IDs)
        │
        ▼
   Encrypt segments (CENC) + write ContentProtection / #EXT-X-KEY
```

Conceptual flow (vendor URL/authentication vary):

```bash
# 1) Fetch CPIX for content id (auth headers per vendor)
curl -sS -H "Authorization: Bearer $TOKEN" \
  "$CPIX_URL?contentId=movie42" -o keys.cpix.xml

# 2) Feed KID / key / PSSH into packager (Shaka Packager sketch)
packager \
  'in=video.mp4,stream=video,output=video.mp4' \
  --enable_raw_key_encryption \
  --keys "label=sd:key_id=${KID}:key=${CEK}" \
  --pssh "${PSSH_HEX}" \
  --mpd_output manifest.mpd
```

| Knob | Why it matters |
|------|----------------|
| Content id | Must match what license tokens later request |
| DRM system list in request | Missing FairPlay ⇒ no FPS signaling |
| Key period / rotation | Live needs rotating KIDs; VoD often one key |
| Clear vs encrypted audio | Policy may leave audio clear; document it |
| Who may see PlainValue | Only packager/KMS path — never the browser |

Wire into [[flussonic]], Shaka Packager, FFmpeg+openssl workflows, or AWS Elemental via SPEKE.

## Real-World Applications
Used wherever CPIX sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Clear (unencrypted) delivery** — no KMS; skip CPIX.
- **Con / skip when:** **Vendor proprietary-only key API with no CPIX** — use their packager plugin docs instead of forcing XML.
- **Con / skip when:** **Player-side experiments** — CPIX is packaging/KMS; use [[EME]] samples for playback tests.
- **Con / skip when:** **One-off remux with `-c copy`** — no new encryption ⇒ no new CPIX fetch.

## Comparison
- vs [[EME]]: **Player-side experiments** — CPIX is packaging/KMS; use [[EME]] samples for playback tests.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Packager can’t encrypt | CPIX 401/403 or empty `PlainValue` | Fix KMS credentials / site id; confirm content id |
| Player license OK, still black | KID in manifest ≠ KID used to encrypt | Re-package from same CPIX doc; don’t mix key batches |
| DASH plays, HLS fails (or reverse) | PSSH / `#EXT-X-KEY` only on one output | Request both systems in CPIX; enable both packager outputs |
| “Unsupported key system” | PSSH for wrong DRM | Align system IDs with client CDMs |
| Key works then dies mid-live | Rotation without updating packager | Sync key period; reload CPIX on rotate |
| SPEKE timeout on MediaConvert | KMS endpoint / VPC | Network path to key provider; retry + alarms |

- **CPIX ≠ license token** — CPIX feeds the **packager**. The player uses a separate [[streaming license]] / `pallycon-customdata-v2` style token.
- **Never ship `PlainValue` to the client** — CEK belongs in the packager/KMS trust boundary; CDMs receive keys only via license response.
- **PSSH omitted from MPD/m3u8** — encryptors that only set keys but skip ContentProtection leave players guessing.
- **Clock and content-id drift** — license servers reject tokens whose content id doesn’t match the KID set from CPIX.
