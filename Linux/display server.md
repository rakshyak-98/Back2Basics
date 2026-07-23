[[x11]] [[wayland]] [[windowing system]] [[Linux display manager]] [[compositors]]

# Display server

> One-line: **The process that owns the framebuffer and multiplexes GUI clients** — every pixel and input event passes through it. When the screen freezes, blame the server stack before the app.

## Mental model

A **display server** sits between hardware (GPU, monitor, keyboard) and **clients** (Firefox, terminal, IDE). Clients don't draw directly on VRAM; they speak a **display protocol** (X11, Wayland) to the server, which composites and presents frames.

```
Input devices ──► Display server ──► GPU/compositor ──► monitor
                        ▲
                   GUI clients (toolkit → protocol)
```

| Server | Protocol | Typical stack |
|--------|----------|---------------|
| Xorg | X11 | i3, Openbox, GNOME-on-X |
| Wayland compositor | Wayland | GNOME Shell, KDE, Sway |
| Mir (legacy Ubuntu) | Mir | Rare today |

**Not the same as:**

- **Window manager** — decorates/focuses windows (often embedded in compositor on Wayland).
- **Display manager** — login greeter (GDM, LightDM) — starts *before* your session.
- **Desktop environment** — full product (GNOME, KDE).

## Standard config / commands

**Identify what you're running:**

```bash
echo $XDG_SESSION_TYPE          # wayland or x11
loginctl show-session $(loginctl | awk '/tty/ {print $1; exit}') -p Type
ps -e | grep -E 'Xorg|wayland|mutter|kwin|sway'
```

**X11 display variable:**

```bash
echo $DISPLAY    # :0, :1 — which X server socket
xauth list       # see [[x11]] — cookies for that display
```

**Wayland:**

```bash
echo $WAYLAND_DISPLAY   # wayland-0
```

**When switching stacks:** logout → gear icon on greeter → "GNOME on Xorg" vs "GNOME" — see [[Linux display manager]].

**Remote GUI:** SSH `-X`/`-Y` forwards to **X11** display server on your laptop — Wayland forwarding is limited; often need XWayland on remote or pure CLI.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen after login | Switch TTY Ctrl+Alt+F3; journal | Broken driver; nomodeset; reinstall GPU driver |
| Apps can't connect to display | `echo $DISPLAY` / `$WAYLAND_DISPLAY` | `export DISPLAY=:0`; run from user session, not SSH without forward |
| Only root GUI works | Permissions on `/tmp/.X11-unix` | Wrong user; xhost +local: (avoid in prod) |
| Screen tear / vsync | Compositor on/off | Enable compositor; Wayland often fixes tear |
| High CPU in compositor | `top` mutter/kwin | Extension bug; disable extensions; driver issue |
| Mixed X11/Wayland apps | `$XDG_SESSION_TYPE` | Force app to native or XWayland; see app flags |

## Gotchas

> [!WARNING]
> **`xhost +` on shared machine** — any local user can sniff/draw on your display. Use `xauth` + SSH forwarding instead ([[x11]]).

> [!WARNING]
> **NVIDIA + Wayland** — historically painful; verify driver + compositor support before fleet migration.

- **Two display servers** — Xorg and Wayland compositor don't share one `$DISPLAY`; apps hardcoded to X fail on pure Wayland without XWayland.
- **Headless servers** — no display server needed; don't install Xorg "just because."

## When NOT to use

- **Server-side rendering workloads** — use GPU compute (CUDA/Vulkan) without a display server when possible.
- **Debugging network services** — use [[ss]], [[journalctl]]; display stack irrelevant on headless nodes.

## Related

[[x11]] [[wayland]] [[windowing system]] [[Linux display manager]] [[compositors]] [[WM_CLASS]]
