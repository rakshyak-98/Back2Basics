```ts
type CountryPopulation = Record<string, number>;
```
- `Record` utility type in TypeScript create an object type with specified keys and value types.
- `K extends keyof any` means K can be any valid object property key type (string, number, or symbol)
- `T` is the type of values that will be stored.
- `[P in K]` uses a mapped type to iterate over all possible values of K
The result is an object type where every key from K maps to a value of type T

> [!INFO] we can assign default type parameter
```ts
interface Response<ResBody = any>
```

## declare keyword
- it is used to tell the compiler that a variable or property exists but is defined elsewhere.


### Typescript name-space definition
- specify `.d.ts` file location in `tsconfig.json` under the `include` or `typeRoots` field.

```ts
declare const APP_VERSION: string;
declare function logMessgae(messgae: string): void;
```
- used when variables or functions are globally available

```ts
declare module 'my-library' {
	export function greet(name: stirng): string;
	export const version: string;
}
```
- define the shape of a module when using `import/export`

#### Namespace declaration
```ts
declare namespace MathUtils {
	function add(a: number, b: number): number;
	function subtract(a: number; b: number): number;
}
```
- for grouping related declarations

```ts
declare module "*.json" {
	const value: any
	export default value;
}
```
