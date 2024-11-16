### Types
- You can define global level types, to use types without importing them and still use them in your code.
#### Global types
```typescript
declare type MyType = {
	name: string;
	age: number
}
```
```typescript
const person: MyType = {
	name: "john",
	age: 32
}
```

#### Ambient Modules
- 

## Namespaces
- used to organize and share code across multiple files.
- allow you to group related functionality into a single unit and prevent naming conflicts.