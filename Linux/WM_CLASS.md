[[Linux window manager]] [[i3 Window Manager Starter Guide]] [[x11]] [[wayland]]

# WM_CLASS

> WM_CLASS is an X11 property (instance, class) that window managers use to apply rules — placement, workspace, floating, and focus behavior.

```txt
        WM_CLASS ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Desktop/Linux niche: shows you can debug window rules with `xprop` and that W…

## Sources
- [ICCCM — WM_CLASS](https://tronche.com/gui/x/icccm/sec-4.html#s-4.1.4) — deep-dive
- [i3 — class and window title](https://i3wm.org/docs/userguide.html#using_window_properties) — overview

## Key Concepts
- **Instance vs class:** First string instance, second class — rules usually match class.
- **xprop:** Click-to-inspect X properties on a window.
- **WM rules:** assign workspace, floating, sticky, inhibit focus steal.
- **Wayland gap:** Native Wayland clients use `app_id`, not WM_CLASS.


- **Core:** Format: two strings

## Technical Details
```bash
xprop WM_CLASS
# WM_CLASS(STRING) = "firefox", "Firefox"
```

- Click a window after running `xprop`.

- i3 example:

```
assign [class="Firefox"] workspace 3
for_window [class=".*"] title ".*Meet.*" floating enable
```

## Mistakes to Avoid
- **Mistake:** Matching on title alone for long-lived rules
- **Mistake:** Assuming Wayland-native apps answer `xprop WM_CLASS`
- **Mistake:** Case-sensitive class mismatches (`Firefox` vs `firefox`)

## Pros/Cons or Trade-offs
- **Pro:** Stable matching without fragile window titles.
- **Con:** Titles change with language/content; class is stabler but apps can set odd values.
- **Trade-off:** Regex rules are powerful and easy to over-match.

## Comparison
- vs window title rules: titles are user-visible and volatile


### Use cases
- Pinning browsers to workspace 3, floating video call windows, and fixing “rul…
