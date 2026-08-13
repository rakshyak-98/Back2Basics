[[Linux window manager]] [[i3 Window Manager Starter Guide]] [[x11]]

# WM_CLASS

> WM_CLASS is an X11 property (instance, class) that window managers use to apply rules — placement, workspace, floating, and focus behavior.

Format: two strings — **instance** (often program name) and **class** (often binary name). Wayland compositors may expose different hints; XWayland apps still set WM_CLASS.

## Query

```bash
xprop WM_CLASS
# WM_CLASS(STRING) = "firefox", "Firefox"
```

Click a window after running `xprop` and clicking the target.

## i3 example

```
assign [class="Firefox"] workspace 3
for_window [class=".*"] title ".*Meet.*" floating enable
```

## Related

[[i3 Window Manager Starter Guide]] · [[Linux window manager]] · [[x11]]

## Sources

- [ICCCM — WM_CLASS](https://tronche.com/gui/x/icccm/sec-4.html#s-4.1.4)
- [i3 — class and window title](https://i3wm.org/docs/userguide.html#using_window_properties)
