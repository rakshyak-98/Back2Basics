- in typescript a feature that allows developers to define the structure and types of external JavaScript libraries without implementing them.
- particularly useful for integrating third-party libraries that do not have TypeScript definitions or were not originally written in TypeScript.
- also know as declarative modules, enable you to describe the shape and structure of an external module.

#### How to declare an Ambient Module
- to declare an ambient module you use the `declare module` syntax followed by the module name.
```typescript
declare moudle `example-module` {
	export function exampleFunction(param: string): number;
	export const exampleVariable: string;
}
```

##### Using ambient module
```typescript
import { exmapleFunction, exampleVariable } from 'exmaple-module';

cosnt result = exampleFunction('test');
console.log(exampleVariable)
```