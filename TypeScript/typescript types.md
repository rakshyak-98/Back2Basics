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
