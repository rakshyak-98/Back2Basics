# Work Log — DRM Streaming Demo

**Project:** Browser DRM playback demo (streaming origin + Widevine + license server)  
**Period:** June 2026

---

## Brief introduction

I built a demo for playing **DRM-protected streams** in the browser. The system connects a **streaming media server** (origin), a **multi-DRM license provider** (Widevine), an **HTML5 adaptive player**, and a **Node.js/Express** backend.

The Node server has two responsibilities: **generate license tokens** for Widevine playback, and **reverse-proxy the streaming origin** under a local path so the browser can load manifests and segments from the same origin without CORS issues. A simple web UI lets you choose stream name and protocol (DASH/HLS) and play encrypted content in a Widevine-capable browser.

---

## What I created

| Component         | Description                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| **Backend API**   | Express server with a license-token endpoint and a streaming reverse proxy with manifest URL rewriting |
| **Web player**    | Shaka Player page with stream/protocol controls, DRM status overlay, and Widevine configuration        |
| **Documentation** | Setup guide, core features, decryption flow, and troubleshooting notes                                 |

**Key capabilities:**

- License token generation endpoint for Widevine license requests
- Proxied DASH (`.mpd`) and HLS (`.m3u8`) manifest delivery
- Same-origin segment fetching through the proxy

---

## Tech stack

### Backend

- **Node.js**
- **TypeScript** — compiled and run as production JavaScript
- **Express** — HTTP server and routing
- **Node.js `crypto`** — AES-256-CBC policy encryption, SHA-256 integrity hash
- **dotenv** — environment-based configuration
- **cors** — cross-origin support

### Frontend

- **HTML5 / vanilla JavaScript**
- **Shaka Player** — DASH/HLS playback and DRM orchestration
- **W3C EME (Encrypted Media Extensions)** — browser DRM API
- **Widevine CDM** — `com.widevine.alpha` key system

### Streaming & DRM (external services)

- **Streaming media server** — origin for encrypted DASH/HLS output
- **Multi-DRM license service** — Widevine license delivery
- **CENC** — Common Encryption for segment-level protection

### Protocols & standards

- **MPEG-DASH** (primary for browser Widevine)
- **HLS** (supported; Widevine in browsers is less consistent)
- **License token v2 format** — JSON token with encrypted policy and SHA-256 hash

### Tooling

- **tsx** — dev-time TypeScript execution
- **npm** — dependency and script management

---

## What I learned

### 1. DRM architecture (end-to-end)

- The **manifest** is usually **plaintext** and carries DRM metadata (`ContentProtection`, key IDs, PSSH).
- **Media segments** are **encrypted** (CENC) on the wire.
- The **application server does not decrypt video** — it issues authorization tokens; decryption happens in the browser CDM after the license server returns keys.

### 2. License token generation

I implemented a v2-style license token flow:

1. Build a playback policy JSON
2. Encrypt the policy with **AES-256-CBC**
3. Compute a **SHA-256 hash** over a defined concatenation of token fields
4. Package fields into JSON and **base64-encode** the result

The token is sent as a **custom HTTP header** on Widevine license requests. It is separate from packaging/key-exchange tokens used elsewhere in the DRM workflow.

### 3. Widevine + Shaka integration

- Configure Widevine key system (`com.widevine.alpha`)
- Point license requests to the license server URL
- Attach the generated token in player DRM request headers
- Load encrypted manifests through the same-origin proxy

### 4. Same-origin proxy pattern for streaming

- Cross-origin manifest/segment access causes browser CORS failures.
- Manifests may contain **absolute upstream URLs**, causing the player to bypass the proxy on refresh.
- Solution: proxy streaming traffic and **rewrite manifest URLs in memory** to keep all playback requests on one origin.

### 5. Structured DRM debugging

I used a staged troubleshooting approach:

| Stage              | Focus                                                 |
| ------------------ | ----------------------------------------------------- |
| Manifest           | Verify MPD/M3U8 availability via proxy                |
| Segments           | Verify init/media segment reachability                |
| License            | Verify token endpoint and credential/config alignment |
| Origin consistency | Ensure player does not switch to upstream origin URLs |

### 6. Configuration alignment

Playback depends on consistent configuration across packaging and playback:

- Content ID in token must match packaged content ID
- Site credentials (site key/access key) must match license provider settings
- Streaming origin must be reachable from the backend proxy

### 7. Protocol choices

- **DASH + Widevine** is the most reliable browser path.
- **HLS + Widevine** is platform-dependent.

---

## Summary

I delivered a working **browser DRM playback demo** covering token generation, streaming proxy design, client-side EME integration, and operational debugging. The work gave me hands-on experience with **multi-DRM licensing**, **adaptive streaming**, and **secure content delivery** in an integrated playback pipeline.
