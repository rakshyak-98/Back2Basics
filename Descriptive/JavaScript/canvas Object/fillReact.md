"does not change the current path" means that invoking `fillReact()` doesn't affect any existing path that has been defined using other drawing methods, such as `moveTo()`, `lineTo()` or `arc()`.
- This is important because drawing methods in a canvas context often rely on the current path to determine where to draw.
### Current path
- path represents a sequence of connected lines or shapes that define what should be drawn on the canvas.
>[!NOTE] When using `fillReact()` any previously defined path (if any) remains unchanged. This means that the rectangle drawn by `fillReact()` is not considered part of any path.