[[x11]] [[display server]] [[windowing system]] [[WM_CLASS]] [[wayland]]

# X window system (X11)

> Network-transparent windowing protocol — the X server owns the display; clients send drawing requests over a UNIX socket or TCP.

```txt
        X window system (X ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Architecture question: clients, server, and WM as another client

## Sources
- [X.Org Foundation](https://www.x.org/wiki/) — overview
- Scheifler & Gettys, *X Window System* — deep-dive

## Key Concepts
- **X protocol:** client drawing requests and server input events.
- **WM as client:** special privileges for decoration/focus.
- **Display names:** `:0` local seat; `host:10.0` SSH forwarded.
- **Auth:** prefer `xauth` cookies; avoid coarse `xhost +`.


- **Core:** This note under `window manager/` is the protocol reference

## Technical Details
```
X client (app) ──X protocol──► X server ──► GPU
         ▲                           │
         └──── events (input) ───────┘
Window manager (WM) is another client with special privileges.
```

- `DISPLAY=:0` — local seat 0.
- `hostname:10.0` — SSH forwarded display.

- **xhost:** — coarse allow list (avoid `+` in production).
- **xauth:** — cookie-based auth for remote X forwarding.
- Prefer Wayland for isolation; use SSH `-Y` sparingly

## Mistakes to Avoid
- **Mistake:** Equating “X11 is insecure” with “never use X”
- **Mistake:** Using `xhost +` as a “quick fix” on multi-user hosts

## Pros/Cons or Trade-offs
- **Pro:** Network-transparent design enabled remote GUI decades early.
- **Con:** Security model assumes cooperative clients on a shared server.

## Comparison
- vs [[x11]]: ops/commands note vs this protocol/architecture note.
- vs [[wayland]]: modern isolation-oriented compositor model.


### Use cases
- Explain why an SSH-forwarded GUI needs matching cookies and why two apps on t…
