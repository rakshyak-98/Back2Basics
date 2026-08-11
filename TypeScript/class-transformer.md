[[TypeScript]] [[typescript types]] [[npm]]

# class-transformer

> `class-transformer` — map plain JSON ↔ class instances (`plainToInstance`); often paired with `class-validator` in NestJS DTOs.

---

## Mental model

**Say it in one breath:** Decorators describe how fields transform. At runtime you hydrate classes so methods/validators work — TypeScript types alone don’t.

```txt
JSON ──plainToInstance(Dto)──► Dto instance ──validate──► ok/err
```

| API | Job |
|-----|-----|
| `plainToInstance` | Hydrate |
| `instanceToPlain` | Serialize |
| `@Expose` / `@Exclude` | Field policy |
| `@Type` | Nested classes |

---

## Standard config / commands

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

| Knob | Why it matters |
|------|----------------|
| `excludeExtraneousValues` | Need `@Expose` or fields drop |
| `enableImplicitConversion` | Coerce strings→numbers |
| `reflect-metadata` | Required with decorators |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Fields undefined | Missing `@Expose` + exclude flag | Expose or disable exclude |
| Nested plain objects | No `@Type` | Add `@Type(() => Nested)` |
| Decorators noop | No `emitDecoratorMetadata` / reflect | Enable tsconfig + import reflect |
| Validation skipped | Only transformed | Run `class-validator` |

---

## Gotchas

> [!WARNING]
> **Types erased** — without transform, `body` is still plain.

> [!WARNING]
> **`excludeExtraneousValues` surprise** — silent drops.

> [!WARNING]
> **ESM + decorators** — toolchain support varies; check Nest defaults.

---

## When NOT to use

- **Zod/Yup pipelines** — one schema may be enough.
- **Functional DTOs** — plain types + parsers.
- **Browser bundles allergic to reflect** — prefer zod.

---

## Related

[[typescript types]] [[typescript]] [[npm]]
