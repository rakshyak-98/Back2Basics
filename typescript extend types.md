### User proper module augmentation
- create a file named `express.d.ts` in the root of your project or inside a `@types` folder.

```ts
declare module "express" {
	interface Response {
		success: (data: any) => void;
	}
}
```
> [!INFO] typescript treats this as a new module declaration, not an augmentation.
- it replaces Express types instead of extending them.
- As a result `Request`, `NextFunction`, etc., are no longer available when you try to import them.

```ts
import "express";

declare module "express" {
	interface Response {
		success: (data: any) => void;
	}
}
```
- `import "express"` Ensures that existing express types (`Request`, `Response`, etc.) are available.
	- extend only what you need `Response.success`, without losing anything.
