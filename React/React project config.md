```typescript vite.d.ts
/// <reference types="vite/client" />
/// <reference types="react" />
/// <reference types="node" />
```
- Remember, for this to work, you need to have the corresponding `@types` packages installed in your project. For instance, `@types/react` for React types or `@types/node` for Node.js types.
- This method is particularly useful for including ambient type declarations that don't get automatically picked up by TypeScript's module resolution system.
