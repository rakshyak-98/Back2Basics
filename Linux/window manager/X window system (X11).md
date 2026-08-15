[[x11]] [[display server]] [[windowing system]] [[WM_CLASS]] [[wayland]]

# X window system (X11)

> Network-transparent windowing protocol — the X server owns the display; clients send drawing requests over a UNIX socket or TCP.

## Interview Relevance

Architecture question: clients, server, and WM as another client; `DISPLAY` naming; xauth vs xhost security.

## Sources

- [X.Org Foundation](https://www.x.org/wiki/) — overview
- Scheifler & Gettys, *X Window System* — deep-dive

## Core Definition

This note under `window manager/` is the protocol reference; day-to-day commands live in [[x11]].

## Key Concepts

- **X protocol:** client drawing requests and server input events.
- **WM as client:** special privileges for decoration/focus.
- **Display names:** `:0` local seat; `host:10.0` SSH forwarded.
- **Auth:** prefer `xauth` cookies; avoid coarse `xhost +`.

## Technical Details

```
X client (app) ──X protocol──► X server ──► GPU
         ▲                           │
         └──── events (input) ───────┘
Window manager (WM) is another client with special privileges.
```

`DISPLAY=:0` — local seat 0. `hostname:10.0` — SSH forwarded display.

Security:

- **xhost** — coarse allow list (avoid `+` in production).
- **xauth** — cookie-based auth for remote X forwarding.
- Prefer Wayland for isolation; use SSH `-Y` sparingly — X11 has weak isolation between clients.

## Real-World Applications

Explain why an SSH-forwarded GUI needs matching cookies and why two apps on the same X server can historically screenshot each other.

## Pros/Cons or Trade-offs

- **Pro:** Network-transparent design enabled remote GUI decades early.
- **Con:** Security model assumes cooperative clients on a shared server.

## Comparison

- vs [[x11]]: ops/commands note vs this protocol/architecture note.
- vs [[wayland]]: modern isolation-oriented compositor model.

## Mistakes to Avoid

- Equating “X11 is insecure” with “never use X” — context is shared-server snooping, not TLS.
- Using `xhost +` as a “quick fix” on multi-user hosts.
