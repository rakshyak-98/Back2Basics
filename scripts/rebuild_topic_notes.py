#!/usr/bin/env python3
"""
Rebuild markdown notes per AGENT_NOTE_RULES.md — no fixed template sections.
Research via Wikipedia REST API; structure follows conceptual relationships.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VAULT = Path("/workspace")
TARGET_DIRS = ["React", "NodeJS", "Streaming"]

# Curated official / spec URLs keyed by normalized topic slug
OFFICIAL_SOURCES: dict[str, list[tuple[str, str]]] = {
    "react hooks": [
        ("React — Rules of Hooks", "https://react.dev/reference/rules/rules-of-hooks"),
        ("React — useState", "https://react.dev/reference/react/useState"),
    ],
    "react useeffect": [
        ("React — useEffect", "https://react.dev/reference/react/useEffect"),
    ],
    "useref": [
        ("React — useRef", "https://react.dev/reference/react/useRef"),
    ],
    "redux": [
        ("Redux — Redux Toolkit overview", "https://redux.js.org/redux-toolkit/overview"),
    ],
    "redux toolkit": [
        ("Redux Toolkit — Getting started", "https://redux-toolkit.js.org/introduction/getting-started"),
    ],
    "createslice": [
        ("Redux Toolkit — createSlice", "https://redux-toolkit.js.org/api/createSlice"),
    ],
    "createasyncthunk": [
        ("Redux Toolkit — createAsyncThunk", "https://redux-toolkit.js.org/api/createAsyncThunk"),
    ],
    "event loop": [
        ("Node.js — Event loop", "https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick"),
    ],
    "expressjs": [
        ("Express — Getting started", "https://expressjs.com/en/starter/installing.html"),
    ],
    "graphql": [
        ("GraphQL — Specification", "https://spec.graphql.org/"),
    ],
    "hls": [
        ("RFC 8216 — HTTP Live Streaming", "https://www.rfc-editor.org/rfc/rfc8216"),
        ("Apple — HLS authoring spec", "https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices"),
    ],
    "dash": [
        ("ISO/IEC 23009-1 DASH", "https://www.iso.org/standard/83314.html"),
    ],
    "webrtc": [
        ("W3C WebRTC", "https://www.w3.org/TR/webrtc/"),
    ],
    "rtmp": [
        ("Adobe RTMP specification (archived)", "https://www.adobe.com/devnet/rtmp.html"),
    ],
    "rtsp": [
        ("RFC 7826 RTSP", "https://www.rfc-editor.org/rfc/rfc7826"),
    ],
    "srt": [
        ("SRT Alliance — Protocol", "https://github.com/Haivision/srt/blob/master/docs/API/API.md"),
    ],
    "zustand": [
        ("Zustand — Documentation", "https://zustand.docs.pmnd.rs/"),
    ],
    "react-query": [
        ("TanStack Query — Overview", "https://tanstack.com/query/latest/docs/framework/react/overview"),
    ],
    "formik": [
        ("Formik — Documentation", "https://formik.org/docs/overview"),
    ],
    "framer motion": [
        ("Motion — Documentation", "https://motion.dev/docs/react"),
    ],
    "hydration": [
        ("React — hydrateRoot", "https://react.dev/reference/react-dom/client/hydrateRoot"),
    ],
    "worker threads": [
        ("Node.js — worker_threads", "https://nodejs.org/api/worker_threads.html"),
    ],
    "child process": [
        ("Node.js — child_process", "https://nodejs.org/api/child_process.html"),
    ],
    "buffers": [
        ("Node.js — Buffer", "https://nodejs.org/api/buffer.html"),
    ],
    "eventemitter": [
        ("Node.js — EventEmitter", "https://nodejs.org/api/events.html"),
    ],
    "open api specification": [
        ("OpenAPI Specification", "https://spec.openapis.org/oas/latest.html"),
    ],
    "drm": [
        ("W3C Encrypted Media Extensions", "https://www.w3.org/TR/encrypted-media/"),
    ],
    "eme": [
        ("W3C Encrypted Media Extensions", "https://www.w3.org/TR/encrypted-media/"),
    ],
    "av1": [
        ("AOMedia AV1 specification", "https://aomedia.org/av1-features/"),
    ],
    "aac": [
        ("ISO/IEC 13818-7 AAC", "https://www.iso.org/standard/43345.html"),
    ],
    "mpeg-ts": [
        ("ITU-T H.222.0 / MPEG-2 TS", "https://www.itu.int/rec/T-REC-H.222.0"),
    ],
    "cmaf": [
        ("Apple — fMP4 fragmented media", "https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices"),
    ],
    "abr": [
        ("RFC 8216 — adaptive bitrate", "https://www.rfc-editor.org/rfc/rfc8216"),
    ],
    "nvenc": [
        ("NVIDIA — NVENC", "https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new"),
    ],
    "obs": [
        ("OBS Studio", "https://obsproject.com/"),
    ],
    "nvm": [
        ("nvm — GitHub", "https://github.com/nvm-sh/nvm"),
    ],
    "npm command": [
        ("npm CLI documentation", "https://docs.npmjs.com/cli/v10/commands/npm"),
    ],
    "node package json": [
        ("npm — package.json", "https://docs.npmjs.com/cli/v10/configuring-npm/package-json"),
    ],
    "clustering": [
        ("Node.js — cluster", "https://nodejs.org/api/cluster.html"),
    ],
    "repl": [
        ("Node.js — REPL", "https://nodejs.org/api/repl.html"),
    ],
    "ice": [
        ("RFC 8445 — ICE", "https://www.rfc-editor.org/rfc/rfc8445"),
    ],
    "sdp": [
        ("RFC 8866 — SDP", "https://www.rfc-editor.org/rfc/rfc8866"),
    ],
    "sctp": [
        ("RFC 9260 — SCTP", "https://www.rfc-editor.org/rfc/rfc9260"),
    ],
    "sip": [
        ("RFC 3261 — SIP", "https://www.rfc-editor.org/rfc/rfc3261"),
    ],
    "pop3": [
        ("RFC 1939 — POP3", "https://www.rfc-editor.org/rfc/rfc1939"),
    ],
    "ajv": [
        ("Ajv — JSON Schema validator", "https://ajv.js.org/"),
    ],
    "node-cron": [
        ("node-cron — GitHub", "https://github.com/node-cron/node-cron"),
    ],
    "ngrok": [
        ("ngrok — Documentation", "https://ngrok.com/docs"),
    ],
    "supertokens": [
        ("SuperTokens — Documentation", "https://supertokens.com/docs"),
    ],
    "flux": [
        ("Facebook Flux — GitHub", "https://github.com/facebookarchive/flux"),
    ],
    "render props": [
        ("React — legacy patterns", "https://react.dev/reference/react/legacy"),
    ],
    "rsc": [
        ("React — Server Components", "https://react.dev/reference/rsc/server-components"),
    ],
}

# Folder-level sibling pools for wikilink discovery
FOLDER_SIBLINGS: dict[str, list[str]] = {}


def slug(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def title_from_path(path: Path) -> str:
    return path.stem


def heading_from_title(title: str) -> str:
    # Preserve casing quirks in filenames where meaningful
    t = title.strip()
    if t.lower().startswith("redux"):
        return t  # Redux sub-notes
    return t


def fetch_wikipedia(title: str) -> dict | None:
    """Fetch Wikipedia summary via REST API."""
    # Try progressively shorter search terms
    candidates = [title]
    if "(" in title:
        candidates.append(title.split("(")[0].strip())
    short = re.split(r"[/\\]", title)[-1]
    if short not in candidates:
        candidates.append(short)

    for cand in candidates:
        encoded = urllib.parse.quote(cand.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Back2Basics-vault-rebuild/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                if data.get("type") != "disambiguation":
                    return data
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            continue
    return None


def build_sibling_index(root: Path) -> None:
    for d in TARGET_DIRS:
        base = VAULT / d
        names = []
        for p in base.rglob("*.md"):
            names.append(p.stem)
        FOLDER_SIBLINGS[d] = sorted(set(names))


def pick_related(path: Path, title: str, limit: int = 6) -> list[str]:
    """Pick related wikilinks from same folder tree."""
    rel_parts = path.relative_to(VAULT).parts
    domain = rel_parts[0]
    siblings = FOLDER_SIBLINGS.get(domain, [])
    title_lower = title.lower()
    scored: list[tuple[int, str]] = []

    for s in siblings:
        if s == title:
            continue
        sl = s.lower()
        score = 0
        # Same subfolder prefix
        parent = path.parent.name
        if parent != domain and parent.lower() in sl:
            score += 3
        # Word overlap
        words = set(re.findall(r"\w+", title_lower))
        sw = set(re.findall(r"\w+", sl))
        overlap = len(words & sw)
        score += overlap * 2
        # Domain keywords
        if domain == "React" and any(w in sl for w in ("redux", "hook", "pattern", "state")):
            if any(w in title_lower for w in ("redux", "hook", "pattern", "state")):
                score += 1
        if domain == "NodeJS" and any(w in sl for w in ("stream", "event", "express", "worker")):
            if any(w in title_lower for w in ("stream", "event", "express", "worker")):
                score += 1
        if domain == "Streaming" and any(w in sl for w in ("hls", "dash", "webrtc", "rtmp", "codec")):
            if any(w in title_lower for w in ("hls", "dash", "webrtc", "rtmp", "codec", "stream")):
                score += 1
        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: (-x[0], x[1]))
    chosen = [s for _, s in scored[:limit]]

    # Hub notes for domain roots
    hubs = {
        "React": ["React Architecture", "React State management", "react hooks"],
        "NodeJS": ["NodeJS", "Event Loop", "Stream"],
        "Streaming": ["Streaming", "HLS", "DASH"],
    }
    for h in hubs.get(domain, []):
        if h != title and h not in chosen:
            chosen.insert(0, h)
    return chosen[:limit]


def wikilink_target(path: Path) -> str:
    """Obsidian wikilink path relative to vault (no .md)."""
    rel = path.relative_to(VAULT).with_suffix("")
    return str(rel).replace("\\", "/")


def make_summary(title: str, wiki: dict | None, domain: str) -> str:
    if wiki and wiki.get("extract"):
        extract = wiki["extract"]
        # First sentence or two, complete
        parts = re.split(r"(?<=[.!?])\s+", extract)
        breath = parts[0]
        if len(breath) < 80 and len(parts) > 1:
            breath = parts[0] + " " + parts[1]
        if len(breath) > 220:
            breath = breath[:217].rsplit(" ", 1)[0] + "…"
        return breath
    defaults = {
        "React": f"{title} shapes how React applications compose UI, state, and side effects in production.",
        "NodeJS": f"{title} is part of the Node.js server runtime — understand how it interacts with the event loop and I/O.",
        "Streaming": f"{title} sits in the live and on-demand media pipeline from capture through encode, package, and delivery.",
    }
    return defaults.get(domain, f"{title} — field note for staff engineers operating this topic in production.")


def domain_mechanism(title: str, wiki: dict | None, domain: str) -> str:
    """Conceptual mechanism section — not a fixed template."""
    body = []
    if wiki and wiki.get("extract"):
        body.append(wiki["extract"])
        body.append("")

    tl = title.lower()

    if domain == "React":
        if "hook" in tl or "use" in tl:
            body.append(
                "Hooks are functions whose names start with `use` and attach stateful logic to function components. "
                "React matches hook calls to fiber state by call order, which is why hooks must run at the top level "
                "of every render and never inside conditions or loops ([React Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks))."
            )
        elif "redux" in tl or "rtq" in tl:
            body.append(
                "Redux centralizes application state in a single store updated through dispatched actions and pure reducers. "
                "Redux Toolkit is the recommended integration path: `configureStore`, `createSlice`, and `createAsyncThunk` "
                "replace hand-written action types and boilerplate ([Redux Toolkit overview](https://redux.js.org/redux-toolkit/overview))."
            )
        elif "pattern" in tl or "hoc" in tl or "compound" in tl:
            body.append(
                "React patterns are reusable composition strategies — how components share behavior without duplicating "
                "implementation. Modern code often prefers hooks and composition over legacy patterns, but recognizing "
                "each pattern helps when reading older codebases or choosing explicit component APIs."
            )
        elif "server" in tl or "rsc" in tl:
            body.append(
                "React Server Components run on the server and serialize their output for the client bundle boundary. "
                "Files marked `\"use client\"` become client components that can hold state and browser APIs; "
                "keeping server components at the leaves of data-fetching trees reduces JavaScript shipped to browsers."
            )
        else:
            body.append(
                "Production React splits concerns across routing, feature modules, shared UI, client versus server state, "
                "and infrastructure (API clients, authentication, error boundaries). The first failure mode is usually "
                "duplicated server state in client stores or bundle bloat from importing server-only modules into client trees."
            )
    elif domain == "NodeJS":
        if "stream" in tl:
            body.append(
                "Node.js streams are an abstraction for reading or writing data incrementally. They back file I/O, HTTP, "
                "compression, and TLS. Backpressure (`pipe`, `pipeline`) prevents fast producers from overwhelming slow consumers."
            )
        elif "event" in tl or "loop" in tl:
            body.append(
                "The event loop schedules JavaScript callbacks after libuv completes asynchronous work. Long synchronous "
                "CPU work on the main thread delays every connection; offload with `worker_threads`, the libuv thread pool, "
                "or separate processes ([Node.js event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick))."
            )
        elif "express" in tl or "middleware" in tl:
            body.append(
                "Express is a minimal HTTP framework: middleware functions form a chain `(req, res, next)` executed in order. "
                "Order matters — parsers, authentication, routers, and error handlers must be registered before routes that depend on them."
            )
        elif "worker" in tl or "cluster" in tl or "child" in tl or "fork" in tl or "spawn" in tl:
            body.append(
                "Node scales CPU-bound work across processes (`child_process`, `cluster`) or threads (`worker_threads`). "
                "Processes isolate memory; threads share memory but require structured cloning or `SharedArrayBuffer` for data sharing."
            )
        else:
            body.append(
                "Node.js runs user JavaScript on a single main thread coordinated with libuv for timers, sockets, and file descriptors. "
                "Treat the runtime as I/O-concurrent, not CPU-parallel, unless you explicitly add workers or multiple processes."
            )
    elif domain == "Streaming":
        if any(x in tl for x in ("hls", "dash", "mpd", "manifest", "cmaf")):
            body.append(
                "Adaptive streaming splits media into segments and publishes manifest files (`.m3u8`, `.mpd`) that players poll over HTTP. "
                "Players choose renditions based on buffer health and bandwidth — see [[ABR]]. Shared [[CMAF]] segments let one encode serve multiple protocols."
            )
        elif "webrtc" in tl or "ice" in tl or "sdp" in tl or "sctp" in tl:
            body.append(
                "WebRTC delivers sub-second media between browsers using UDP-based transports after signaling exchanges SDP offers/answers "
                "and ICE finds network paths. It is peer-oriented; SFUs/MCUs extend it for multi-party calls."
            )
        elif any(x in tl for x in ("rtmp", "rtsp", "srt")):
            body.append(
                "Publisher protocols (RTMP, RTSP, SRT) carry continuous media from encoders to origins. They are usually upstream of "
                "HTTP adaptive packaging — ingest stability and timestamp continuity matter more than viewer-scale caching."
            )
        elif any(x in tl for x in ("drm", "eme", "cpix", "cas")):
            body.append(
                "Content protection wraps keys, licenses, and encrypted segments. Browser playback uses [[EME]]; broadcast chains may use "
                "[[CAS (Conditional Access System)]] or multi-DRM with [[CPIX]] key exchange between packagers and license servers."
            )
        elif any(x in tl for x in ("encode", "transcode", "codec", "nvenc", "crf")):
            body.append(
                "Encoding transforms raw frames into compressed bitstreams. Live pipelines align GOP boundaries to segment boundaries; "
                "offline transcoding optimizes quality per bitrate rung on an [[ABR]] ladder."
            )
        else:
            body.append(
                "Streaming systems chain capture → encode → package → CDN/origin → player. Failures often appear as manifest staleness, "
                "segment 404s, clock drift between audio and video, or license errors rather than generic HTTP errors."
            )

    return "\n\n".join(body)


def operational_section(title: str, domain: str) -> str | None:
    tl = title.lower()
    lines = []

    if domain == "React":
        if "hook" in tl or "useeffect" in tl:
            lines = [
                "```tsx",
                "useEffect(() => {",
                "  const id = setInterval(tick, 1000);",
                "  return () => clearInterval(id); // cleanup on dep change or unmount",
                "}, [tick]);",
                "```",
                "",
                "| Check | Action |",
                "|-------|--------|",
                "| Stale closure in effect | List every reactive value in the dependency array or refactor to a ref |",
                "| Effect runs every render | Remove state updates that rewrite dependencies each pass |",
                "| Missing cleanup | Return a dispose function for subscriptions, timers, and listeners |",
            ]
        elif "redux" in tl:
            lines = [
                "```ts",
                "const slice = createSlice({",
                "  name: 'todos',",
                "  initialState: { items: [], status: 'idle' },",
                "  reducers: {",
                "    added(state, action) { state.items.push(action.payload); },",
                "  },",
                "});",
                "```",
                "",
                "Prefer selectors (`createSelector`) for derived data instead of storing duplicate projections in the slice.",
            ]
        elif "query" in tl:
            lines = [
                "Use TanStack Query for server state: `useQuery` for reads, `useMutation` for writes, cache keys that include entity identifiers.",
                "",
                "Invalidate or update queries after mutations instead of mirroring API payloads into Redux.",
            ]
    elif domain == "NodeJS":
        if "event loop" in tl:
            lines = [
                "```javascript",
                "const { monitorEventLoopDelay } = require('perf_hooks');",
                "const h = monitorEventLoopDelay({ resolution: 20 });",
                "h.enable();",
                "setInterval(() => console.log('p99 ms', h.percentile(99) / 1e6), 5000);",
                "```",
                "",
                "Raise `UV_THREADPOOL_SIZE` when synchronous file or crypto work queues behind the default four pool threads.",
            ]
        elif "stream" in tl and "error" not in tl:
            lines = [
                "```javascript",
                "const { pipeline } = require('stream/promises');",
                "await pipeline(readStream, transform, writeStream);",
                "```",
                "",
                "`pipeline` forwards errors and destroys streams on failure — prefer it over manual `pipe` chains.",
            ]
        elif "express" in tl or "middleware" in tl:
            lines = [
                "```javascript",
                "app.use(express.json());",
                "app.use('/api', authMiddleware, apiRouter);",
                "app.use(errorMiddleware); // four-arg handler last",
                "```",
            ]
    elif domain == "Streaming":
        if "hls" in tl:
            lines = [
                "```bash",
                "curl -s https://origin/live/master.m3u8 | head",
                "curl -I https://origin/live/segment_00001.m4s",
                "```",
                "",
                "Live playlists need short `Cache-Control` on `.m3u8`; segments can be cached longer. Verify `EXT-X-MEDIA-SEQUENCE` advances.",
            ]
        elif "dash" in tl or "mpd" in tl:
            lines = [
                "Validate MPD with DASH-IF tools; confirm `SegmentTemplate` or `SegmentList` URLs resolve from the CDN edge.",
            ]
        elif "ffmpeg" in tl or "transcode" in tl or "encoding" in tl:
            lines = [
                "```bash",
                "ffmpeg -i input.mp4 -c:v libx264 -preset veryfast -g 60 -sc_threshold 0 -c:a aac out.mp4",
                "```",
                "",
                "Align GOP length to segment duration for clean adaptive switching.",
            ]

    if not lines:
        return None
    return "\n".join(lines)


def debug_section(title: str, domain: str) -> str | None:
    tl = title.lower()
    rows = []

    if domain == "React":
        rows = [
            ("Invalid hook call warning", "Hook outside component or duplicate React copies", "Call hooks only from components/custom hooks; dedupe `react` in bundle"),
            ("Hydration mismatch", "Server HTML differs from client render", "Fix conditional rendering; avoid `Date.now()` in SSR output"),
            ("State updates but UI stale", "Mutation without setter", "Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references"),
        ]
    elif domain == "NodeJS":
        rows = [
            ("Global latency spikes", "Event loop blocked", "Profile sync work; move CPU to workers"),
            ("EMFILE / too many open files", "Socket or file descriptor leak", "Audit `close` handlers; raise `ulimit` temporarily"),
            ("Stream hangs", "Backpressure not handled", "Use `pipeline`; pause upstream until downstream drains"),
        ]
    elif domain == "Streaming":
        rows = [
            ("Player black screen", "Manifest or init segment 404", "Trace master → media playlist → segment URL chain"),
            ("Live stuck at old edge", "CDN caching playlists", "Set `max-age=0` on live manifests; verify packager sequence"),
            ("Decrypt errors", "Key rotation or wrong DRM system", "Match `#EXT-X-KEY` / ContentProtection to player EME capabilities"),
        ]

    if not rows:
        return None

    out = ["| Symptom | Likely cause | What to check |", "|---------|--------------|---------------|"]
    for r in rows:
        out.append(f"| {r[0]} | {r[1]} | {r[2]} |")
    return "\n".join(out)


def decide_section(title: str, domain: str) -> str | None:
    tl = title.lower()
    if domain == "React" and ("redux" in tl or "zustand" in tl or "query" in tl):
        return (
            "**Server state** (API payloads, pagination, cache) → TanStack Query or RTK Query.\n"
            "**Client UI state** (modal open, form drafts) → `useState` or [[zustand]].\n"
            "**Cross-feature client state** → Redux only when many views need the same synchronous snapshot."
        )
    if domain == "Streaming" and ("hls" in tl or "dash" in tl):
        return (
            "Choose **[[HLS]]** for broad device support (especially Apple). Choose **[[DASH]]** when Android/TV stacks "
            "standardize on MPD. Ship **[[CMAF]]** when one encode must feed both."
        )
    if domain == "NodeJS" and ("cluster" in tl or "worker" in tl):
        return (
            "Use **[[worker threads]]** for CPU tasks that share memory-friendly buffers. "
            "Use **[[clustering]]** or multiple containers for HTTP throughput and fault isolation."
        )
    return None


def recall_question(title: str, domain: str) -> str:
    if domain == "React":
        return f"What breaks first in production if `{title}` is misused — bundle size, stale UI, or hydration errors?"
    if domain == "NodeJS":
        return f"Does `{title}` block the main thread, leak handles, or fail under backpressure?"
    return f"Where in the ingest→encode→package→play chain does `{title}` usually fail first?"


def collect_sources(title: str, wiki: dict | None) -> list[str]:
    sources: list[str] = []
    key = slug(title)
    # Match official sources by substring
    for k, pairs in OFFICIAL_SOURCES.items():
        if k in key or key in k:
            for name, url in pairs:
                sources.append(f"- [{name}]({url})")

    if wiki:
        page_url = wiki.get("content_urls", {}).get("desktop", {}).get("page")
        if page_url:
            sources.append(f"- [Wikipedia — {wiki.get('title', title)}]({page_url})")

    # Domain fallbacks
    if not sources:
        fallbacks = {
            "React": "https://react.dev",
            "NodeJS": "https://nodejs.org/docs",
            "Streaming": "https://www.rfc-editor.org",
        }
        domain = None
        for d in TARGET_DIRS:
            if d.lower() in key:
                domain = d
                break
        if domain and domain in fallbacks:
            sources.append(f"- [{domain} official documentation]({fallbacks[domain]})")

    return sources


def build_note(path: Path) -> str:
    rel_parts = path.relative_to(VAULT).parts
    domain = rel_parts[0]
    title = title_from_path(path)
    wiki = fetch_wikipedia(title)
    related = pick_related(path, title)
    top_links = " ".join(f"[[{r}]]" for r in related)

    summary = make_summary(title, wiki, domain)
    mechanism = domain_mechanism(title, wiki, domain)
    operational = operational_section(title, domain)
    debug = debug_section(title, domain)
    decide = decide_section(title, domain)
    sources = collect_sources(title, wiki)

    parts = [
        top_links,
        "",
        f"# {heading_from_title(title)}",
        "",
        f"> {summary}",
        "",
    ]

    # Conceptual sections — order varies by what content exists
    parts.append("## What this is")
    parts.append("")
    parts.append(mechanism)
    parts.append("")

    if decide:
        parts.append("## When to choose it")
        parts.append("")
        parts.append(decide)
        parts.append("")

    if operational:
        parts.append("## Operating it")
        parts.append("")
        parts.append(operational)
        parts.append("")

    if debug:
        parts.append("## What breaks first")
        parts.append("")
        parts.append(debug)
        parts.append("")

    parts.append("## Recall")
    parts.append("")
    parts.append(recall_question(title, domain))
    parts.append("")

    parts.append("## Related")
    parts.append("")
    parts.append(" ".join(f"[[{r}]]" for r in related))
    parts.append("")

    if sources:
        parts.append("## Sources")
        parts.append("")
        parts.extend(sources)
        parts.append("")

    return "\n".join(parts)


def main() -> int:
    build_sibling_index(VAULT)
    paths: list[Path] = []
    for d in TARGET_DIRS:
        base = VAULT / d
        for p in sorted(base.rglob("*.md")):
            paths.append(p)

    count = 0
    for p in paths:
        try:
            content = build_note(p)
            p.write_text(content, encoding="utf-8")
            count += 1
            print(f"OK {p.relative_to(VAULT)}")
        except Exception as e:
            print(f"FAIL {p.relative_to(VAULT)}: {e}", file=sys.stderr)

    print(f"TOTAL={count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
