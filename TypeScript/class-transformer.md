[[typescript types]] [[typescript]] [[typescript extend types]] [[npm]]

# class-transformer

> NestJS-era library that maps plain JSON to class instances (`plainToInstance`) and back — often paired with `class-validator` for DTO pipelines.

## Interview Relevance

Interviewers ask about `class-transformer` to see if you know TypeScript types erase at runtime — decorators and `reflect-metadata` rehydrate instances, and `excludeExtraneousValues` silently drops fields without `@Expose`.

## Sources

- [class-transformer README](https://github.com/typestack/class-transformer) — deep-dive
- [NestJS — Validation](https://docs.nestjs.com/techniques/validation) — overview
- [TypeScript Handbook — Decorators](https://www.typescriptlang.org/docs/handbook/decorators.html) — overview

## Core Definition

`class-transformer` converts plain objects (typical HTTP JSON) into class instances and serializes instances back to plain objects, driven by decorators (`@Expose`, `@Type`, `@Exclude`) and options such as `excludeExtraneousValues`.

## Key Concepts

- **`plainToInstance`:** hydrate a DTO class from JSON.
- **`instanceToPlain`:** serialize instances for responses.
- **`@Expose` / `@Exclude`:** field allow/deny policy.
- **`@Type`:** nested class transformation (otherwise nested stays plain).
- **`reflect-metadata` + `emitDecoratorMetadata`:** required for decorator-driven metadata.
- **Pair with validation:** transform does not assert business rules — use `class-validator` or a schema library.

## Technical Details

```txt
JSON ──plainToInstance(Dto)──► Dto instance ──validate──► ok/err
```

```ts
import { plainToInstance, Type, Expose } from 'class-transformer'

class Address {
  @Expose() city!: string
}

class UserDto {
  @Expose() email!: string
  @Type(() => Address) @Expose() address!: Address
}

const user = plainToInstance(UserDto, body, { excludeExtraneousValues: true })
```

| API | Job |
|-----|-----|
| `plainToInstance` | Hydrate |
| `instanceToPlain` | Serialize |
| `@Expose` / `@Exclude` | Field policy |
| `@Type` | Nested classes |

| Knob | Why it matters |
|------|----------------|
| `excludeExtraneousValues` | Need `@Expose` or fields drop |
| `enableImplicitConversion` | Coerce strings→numbers |
| `reflect-metadata` | Required with decorators |

| Symptom | Check | Fix |
|---------|-------|-----|
| Fields undefined | Missing `@Expose` + exclude flag | Expose or disable exclude |
| Nested plain objects | No `@Type` | Add `@Type(() => Nested)` |
| Decorators noop | No emit metadata / reflect | Enable `tsconfig` + import reflect |
| Validation skipped | Only transformed | Run `class-validator` |

## Real-World Applications

NestJS controllers enable `ValidationPipe` with `transform: true` so request bodies become DTO class instances before handlers run.

**Example:** All DTO fields are `undefined` after transform because `excludeExtraneousValues: true` was set without `@Expose` on each property.

## Pros/Cons or Trade-offs

- **Pro:** Familiar class/DTO style in NestJS ecosystems; nested object mapping with `@Type`.
- **Con:** Decorator + reflect toolchain is heavier than Zod/Yup parse pipelines.
- **Con:** Silent field drops with `excludeExtraneousValues` surprise teams.

## Comparison

- vs Zod/Yup: one schema can parse and validate without classes or reflect-metadata.
- vs TypeScript types alone: types erase; class-transformer operates at runtime.
- vs plain interfaces: interfaces never exist at runtime — no instance methods or decorators.

## Mistakes to Avoid

- Assuming a typed `body: UserDto` parameter is already a class instance without transform.
- Enabling `excludeExtraneousValues` without `@Expose` on every allowed field.
- Forgetting `emitDecoratorMetadata` / `reflect-metadata` so decorators do nothing.
- Skipping validation after transform and trusting the shape.
