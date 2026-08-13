[[window manager]] [[x11]] [[wayland]] [[compositors]]

# X window system (X11)

> X11 is the classic Unix display protocol — clients speak X to an X server (Xorg) that owns screens and input.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `DISPLAY` selects the server; Xauth cookies authorize; a WM manages windows on that server.

```txt
client ($DISPLAY=:0) ──X11 proto──► Xorg ──► DRM/KMS
         │                              │
       xauth                         WM (i3…)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **X server** | Owns hardware display | “Xorg is the common implementation.” |
| **DISPLAY** | host:display.screen | “`:0` is local seat 0.” |
| **Xauth** | MIT-MAGIC-COOKIE | “SSH -X forwards the cookie.” |
| **XWayland** | X apps on Wayland | “Compat layer, not pure X.” |
| **extension** | RandR, XInput, GLX… | “Features bolted onto core X.” |

---

## Standard config / commands

```bash
echo $DISPLAY
xdpyinfo | head
xrandr
xprop   # click window
xauth list
# nested test server
Xephyr :1 -ac &
DISPLAY=:1 openbox &
```

| Knob | Why it matters |
|------|----------------|
| `DISPLAY` | Wrong value → “cannot open display” |
| Cookie | Authorization failures |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| cannot open display | `$DISPLAY` / xauth | Export `:0`; merge cookie |
| SSH -X fails | sshd X11Forwarding | Enable; use `-Y` cautiously |
| Blank screen | GPU driver / modeset | Kernel cmdline; vendor driver |
| Apps ugly/slow remote | Network X | Prefer Waypipe/VNC; compress |

---

## Gotchas

> [!WARNING]
> **Network X is chatty and cleartext** historically — tunnel or don’t use over WAN.

> [!WARNING]
> **Root X clients** with shared cookie are a classic privilege footgun.

---

## When NOT to use

- **New desktop stacks** — prefer Wayland sessions.
- **Headless render** — use offscreen/OSMesa/EGL without a full Xorg when possible.

---

## Related

[[x11]] [[wayland]] [[Linux window manager]] [[compositors]] [[display server]]
