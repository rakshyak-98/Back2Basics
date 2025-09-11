In your code, the **clipped container (`div` with width: `${position}%`)** resizes correctly, but inside it, the `<img>` is still `w-full h-full` — so Chrome stretches it relative to the _clipped box_, while Firefox stretches relative to the _parent container_.

## Fix

