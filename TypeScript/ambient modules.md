- In TypeScript, you can describe the shape of a JavaScript library without writing its code.
- Useful when a library has no `@types` package or was written in plain JS.
- Also called **declaration modules** — you only declare types, not implementations.

#### How to declare an ambient module

Use `declare module` plus the module name:

```typescript
declare module `example-module` {
	export function exampleFunction(param: string): number;
	export const exampleVariable: string;
}
```

```typescript
import { exampleFunction, exampleVariable } from 'example-module';

const result = exampleFunction('test');
console.log(exampleVariable)
```
