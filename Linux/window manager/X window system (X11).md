[[x11]] [[display server]] [[windowing system]]

# X window system (X11)

> The X Window System (X11) is a network-transparent windowing protocol — the X server owns the display; clients send drawing requests over UNIX socket or TCP.

This note lives under `window manager/` as the protocol reference; operational commands are in [[x11]].

## Architecture

```
X client (app) ──X protocol──► X server ──► GPU
         ▲                           │
         └──── events (input) ───────┘
Window manager (WM) is another client with special privileges.
```

## Displays

`DISPLAY=:0` — local seat 0. `hostname:10.0` — SSH forwarded display.

## Security

- **xhost** — coarse allow list (avoid `+` in production).
- **xauth** — cookie-based auth for remote X forwarding.
- Prefer Wayland or SSH `-Y` sparingly; X11 has no isolation between clients.

## Related

[[x11]] · [[WM_CLASS]] · [[wayland]]

## Sources

- [X.Org Foundation](https://www.x.org/wiki/)
- Scheifler & Gettys, X Window System
