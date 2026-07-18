turn binary data (like images, files, PDFs) into plain text so it can be safely sent over the internet or stored in places that only allow text.

> [!INFO]
> You cannot paste raw photo bytes (binary data) into an email or JSON. So Base64 converts that photo into a long string of letters, numbers, and symbols
> Base64 strings are ~33% larger than the original file.

**Image in HTML**
```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ..." />
```

### How It Works (Simple Math)

- Normal text uses **8 bits per character** (1 byte)
- Base64 uses **64 safe characters**: A–Z, a–z, 0–9, +, / (and = for padding)

It takes **3 bytes** of binary data (24 bits) → splits into **4 characters** (6 bits each)

## Error (Payload too large)
- You're getting `PayloadTooLargeError` because you're sending base64-encoded images (data:image/...) in the request body as JSON.

> [!NOTE]
> Base64 increases image size by ~33%, and 10 images × 2MB each = ~26MB+ → way over Express's default `100KB` limit for json() parser.

### Fix: **Send images as File objects using `FormData` + multipart/form-data**

**Never send base64 strings in JSON for large images.** **Always use multipart/form-data for file uploads.**