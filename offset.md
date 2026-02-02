offset -> how far to move -> from a known starting place.

|Context|What "offset" means|Typical unit|Example|
|---|---|---|---|
|**Arrays / Lists**|How many elements from the beginning (index 0)|Number of elements|In array `["a","b","c","d"]`, `'d'` has offset **3** (or index 3)|
|**Memory / Pointers**|Number of **bytes** to add to a base memory address to reach a location|Bytes|`base + 12` → 12 bytes after the start|
|**Struct / Class fields**|Byte distance from start of object to a particular field|Bytes|In a `struct Person { int age; char name[20]; }` → `name` offset might be 4 bytes|
|**File reading/writing**|Byte position from the beginning (or current position) of the file|Bytes|`seek(offset=1024)` → jump to byte 1024 in the file|
|**Assembly / Low-level**|Value added to a base register to get effective address|Bytes / words|`mov eax, [ebx + 8]` → offset = 8 bytes|
|**Buffer / String slicing**|Starting position within a buffer or string|Bytes or characters|`substr(str, offset=5, len=3)`|
|**2D arrays / images / matrices**|Row offset × width + column offset|Elements or bytes|Pixel at (y=10, x=4) in 1920×1080 image → offset = 10×1920 + 4 pixels|