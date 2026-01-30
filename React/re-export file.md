> [!WARNING]
> If you publish an npm package → avoid export * completely in the public index.ts. Use explicit exports.

> [!NOTE]
> You have ~10–30 API functions → yes, create barrels — but use explicit re-exports (`export { x } from './x'`) instead of `export *`.

```text
src/api/hotels/
├── index.ts                ← the barrel / re-export file
├── getHotels.ts
├── getHotelById.ts
├── createHotel.ts
├── types.ts                ← shared interfaces / types
└── constants.ts            ← paths, query keys, etc.
```

`index.ts` content

```ts
// src/api/hotels/index.ts

// Re-export functions (explicit = safer)
export { getHotels } from './getHotels';
export { getHotelById } from './getHotelById';
export { createHotel } from './createHotel';

// Re-export types (wildcard is usually fine here)
export * from './types';

// Re-export constants / helpers
export { hotelKeys, API_PATHS } from './constants';

// Optional: one facade / service class
export { HotelsService } from './HotelsService';  // if you have one

```

Usage anywhere in the app

```ts
import { getHotels, getHotelById, hotelKeys } from "@/api/hotels";
```
