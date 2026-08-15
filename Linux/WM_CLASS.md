[[Linux window manager]] [[i3 Window Manager Starter Guide]] [[x11]] [[wayland]]

# WM_CLASS

> WM_CLASS is an X11 property (instance, class) that window managers use to apply rules — placement, workspace, floating, and focus behavior.

## Interview Relevance
Desktop/Linux niche: shows you can debug window rules with `xprop` and that Wayland apps may not expose the same hints (XWayland still does).

## Sources
- [ICCCM — WM_CLASS](https://tronche.com/gui/x/icccm/sec-4.html#s-4.1.4) — deep-dive
- [i3 — class and window title](https://i3wm.org/docs/userguide.html#using_window_properties) — overview

## Core Definition
Format: two strings — **instance** (often program name) and **class** (often binary name). Window managers match on class/instance/title. Wayland compositors use different app-ids; XWayland apps still set WM_CLASS.

## Key Concepts
- **Instance vs class:** First string instance, second class — rules usually match class.
- **xprop:** Click-to-inspect X properties on a window.
- **WM rules:** assign workspace, floating, sticky, inhibit focus steal.
- **Wayland gap:** Native Wayland clients use `app_id`, not WM_CLASS.

## Technical Details

```bash
xprop WM_CLASS
# WM_CLASS(STRING) = "firefox", "Firefox"
```

Click a window after running `xprop`.

i3 example:
```
assign [class="Firefox"] workspace 3
for_window [class=".*"] title ".*Meet.*" floating enable
```

## Real-World Applications
Pinning browsers to workspace 3, floating video call windows, and fixing “rule never matches” by reading the real class string (often capitalized differently than the binary name).

## Pros/Cons or Trade-offs
- **Pro:** Stable matching without fragile window titles.
- **Con:** Titles change with language/content; class is stabler but apps can set odd values.
- **Trade-off:** Regex rules are powerful and easy to over-match.

## Comparison
vs window title rules: titles are user-visible and volatile. vs Wayland `app_id`: same idea, different property. Related: [[i3 Window Manager Starter Guide]], [[Linux window manager]].

## Mistakes to Avoid
- Matching on title alone for long-lived rules.
- Assuming Wayland-native apps answer `xprop WM_CLASS`.
- Case-sensitive class mismatches (`Firefox` vs `firefox`).
