[[Streaming]] [[WebRTC]] [[ICE (Interactive Connectivity Establishment)]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]]

# WebRTC Get Started Guide

> Capture devices → local preview → peer connection — fix constraints before you debug ICE.

## Mental model

**Say it in one breath:** Before ICE and signaling matter, you must open the right camera/mic, apply constraints that the device can meet, show a local preview, then attach tracks to an `RTCPeerConnection`.

```txt
enumerateDevices / devicechange
        │
        ▼
getUserMedia(constraints) ──► MediaStream
        │
        ├──► <video>.srcObject = stream   (local preview)
        └──► pc.addTrack(track, stream)   (send to peer)
                    │
                    ▼
         offer/answer + ICE  ([[WebRTC Signaling channels]],
                              [[ICE (Interactive Connectivity Establishment)]])
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **enumerateDevices** | List cameras/mics/speakers | “I pick deviceId after listing inputs.” |
| --- | --- | --- |
| **devicechange** | Hot-plug event | “USB cam plugged in — refresh the dropdown.” |
| **constraints** | What you ask the device for | “Exact deviceId + min width/height + echoCancellation.” |
| **MediaStream** | Bundle of tracks | “Tracks go to preview and to the PeerConnection.” |
| **srcObject** | Attach stream to `<video>` | “Local preview is not the remote peer yet.” |
| **addTrack** | Publish to the PC | “Tracks must exist before createOffer.” |

### Order that saves hours

1. **Secure context** — HTTPS or `localhost` (getUserMedia blocked otherwise).
2. **List devices** — after a permission grant, labels appear.
3. **Open with constraints** — match a real `deviceId`; avoid impossible min size.
4. **Preview locally** — prove capture before blaming ICE.
5. **PeerConnection** — STUN/TURN + signaling; see [[WebRTC]] and [[ICE (Interactive Connectivity Establishment)]].

## Standard config / commands

### Capture + local preview

```js
async function playLocalPreview() {
  const stream = await navigator.mediaDevices.getUserMedia({
    audio: { echoCancellation: true },
    video: { width: { ideal: 1280 }, height: { ideal: 720 } },
  })
  document.querySelector('video#localVideo').srcObject = stream
  return stream
}
```

### List cameras / mics

```js
async function getConnectedDevices(kind) {
  const devices = await navigator.mediaDevices.enumerateDevices()
  return devices.filter((d) => d.kind === kind) // 'videoinput' | 'audioinput' | 'audiooutput'
}

const cameras = await getConnectedDevices('videoinput')
console.log(cameras.map((c) => ({ id: c.deviceId, label: c.label })))
```

### devicechange (hot-plug)

```js
async function refreshCameraSelect() {
  const cameras = await getConnectedDevices('videoinput')
  const select = document.querySelector('select#availableCameras')
  select.innerHTML = ''
  for (const camera of cameras) {
    const opt = document.createElement('option')
    opt.value = camera.deviceId
    opt.textContent = camera.label || `Camera ${camera.deviceId.slice(0, 8)}`
    select.add(opt)
  }
}

navigator.mediaDevices.addEventListener('devicechange', () => {
  refreshCameraSelect().catch(console.error)
})
```

### Open a specific camera

```js
async function openCamera(cameraId, minWidth, minHeight) {
  return navigator.mediaDevices.getUserMedia({
    audio: { echoCancellation: true },
    video: {
      deviceId: { exact: cameraId },
      width: { min: minWidth, ideal: minWidth },
      height: { min: minHeight, ideal: minHeight },
    },
  })
}
```

### PeerConnection (after capture works)

```js
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'turn:turn.example.com:3478', username: 'u', credential: 'p' },
  ],
})

stream.getTracks().forEach((t) => pc.addTrack(t, stream))
pc.onicecandidate = (e) => e.candidate && signaling.send({ type: 'candidate', candidate: e.candidate })

const offer = await pc.createOffer()
await pc.setLocalDescription(offer)
signaling.send({ type: 'offer', sdp: pc.localDescription })
```

| Knob | Why it matters |

| `deviceId: { exact }` | Pins the camera the user selected |
| --- | --- |
| `ideal` vs `min` | `min` fails hard if unsupported; `ideal` negotiates down |
| `echoCancellation` | Stops laptop mic hearing speaker output |
| STUN + TURN in `iceServers` | Capture OK ≠ connect OK across NATs |

Debug: browser console for `OverconstrainedError`; `chrome://webrtc-internals` only after PC exists.

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `getUserMedia` NotAllowedError | Permissions / insecure origin | HTTPS; user gesture; reset site permissions |
| `OverconstrainedError` | Impossible width/height or bad deviceId | Soften to `ideal`; re-enumerate after grant |
| Empty device labels | Called enumerate before permission | Call getUserMedia once, then enumerate |
| Black `<video>` | `srcObject` not set / muted autoplay | Set `srcObject`; `video.play()`; muted for autoplay policy |
| Works in preview, remote silent | Tracks not on PC / signaling | `addTrack` before offer; fix [[WebRTC Signaling channels]] |
| Stuck connecting | ICE only | See [[ICE (Interactive Connectivity Establishment)]]; add TURN |
| Camera list stale after USB plug | No `devicechange` listener | Refresh enumerateDevices on event |

## Gotchas

> [!WARNING]
> **Typos in constraints kill capture** — `video` not `vide`; `echoCancellation` not `echoCancallation`. Failures look like “WebRTC broken” but never reach ICE.

> [!WARNING]
> **Labels are blank until permission** — privacy rule; design UX around a first grant.

> [!WARNING]
> **Stopping tracks** — `track.stop()` releases the hardware LED; forgetting leaves the camera “on” after hangup.

> [!WARNING]
> **Replace track mid-call** — use `sender.replaceTrack()` (or renegotiate); don’t assume a new getUserMedia alone updates the remote.

> [!WARNING]
> **Signaling ≠ media** — local preview success does not prove STUN/TURN; configure [[TURN server (Traversal Using Relays around NAT)]] for production.

## When NOT to use

- **Server-side only ingest** — [[RTMP]] / SRT / WHIP into origin; no browser getUserMedia.
- **VOD progressive download** — plain HTTP file/Byte stream; not a PeerConnection.
- **Debugging ICE first** — if local preview fails, fix devices/constraints before touching candidates.

## Related

[[WebRTC]] [[WebRTC Signaling channels]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]] [[SDP (Session Description Protocol)]]
