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

### Type constraints
- restrictions placed on generic types to ensure they meet certain requirements.
- defined using the `extends` keyword in generic type parameters.
```ts
function getLength<T extends {length: number}>(args: T) : number {
	return arr.length;
}
```
- here `T` is constrained to types that have a `length` property. This prevents passing types that don't have `lenght` like `number`.

```ts
interface Animal {
	name: string;
}

class Dog implements Animal {
	name: string;
	constructor(name: string){
		this.name = name;
	}
}

function printName<T extends Animal>(obj: T) {
	console.log(obj.name);
}
const dog = new Dog("Buddy");
printName(dog) // Works

```

### Extract type from another type
the `infer` keyword is used withing conditional types to infer (extract) a type from another type.
- the `infer` keyword is typically used inside `extends` clauses in conditional types.

```ts
type ReturnTypeOf<T> = T extends (...args: any[]) => infer R ? R : never;
type ExampleFunction = () => string;
type Result = ReturTypeOf<ExampleFunction>; // Result is inferred as string

```

```ts
type ElementType<T> = T extends (infer U)[] ? U : never;
type ArrayType = string[];
type Element = ElementType<ArrayType>; // Element is inferred as string

```