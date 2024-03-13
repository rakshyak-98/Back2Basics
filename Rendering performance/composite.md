Compositing is where the painted parts of the page are put together for displaying on screen.
since the part of the page were potentially drawn onto multiple layers, they need to be applied to the screen in the correct order.
- especially important for elements that overlap another.
#### factors affect page performance:
1. number of compositor layers to need to be managed.
2. the properties that you use for animations.
- Stick to transform and opacity changes for your animations.
- promote moving elements with `will-change` or `translateZ`.
- avoid overusing promotion rules; layers requires memory and management.