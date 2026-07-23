[[Design pattern]] [[Design pattern/Bridge]] [[NodeJS/Express middleware]] [[MongoDB/mongoose middleware]]

# Dependency Injection

> Supply dependencies from outside instead of hard-coding `new` inside a class — testability and modular wiring — **IoC container vs manual constructor inject**.

## Mental model

**Without DI:** class creates its own DB client → tight coupling, hard to mock.

**With DI:** caller passes interface → swap impl in tests, config, or runtime.

```
┌─────────────┐     constructs      ┌──────────────┐
│  Composition│ ──────────────────► │  UserService │
│  Root/main  │   injects IUserRepo │  repo: IUser │
└─────────────┘                     └──────┬───────┘
                                           │
                                           ▼
                                    PostgresUserRepo
                                    (or InMemory in tests)
```

| Style | Tradeoff |
|-------|----------|
| **Constructor inject** | Explicit required deps — preferred |
| **Setter inject** | Optional deps — can forget |
| **Service locator** | Hidden global — avoid in new code |
| **Framework DI** | NestJS, Spring — ceremony vs convention |

## Standard config / commands

### Manual constructor injection (TypeScript)

```typescript
interface UserRepo {
  findById(id: string): Promise<User | null>;
}

class UserService {
  constructor(private repo: UserRepo) {}

  async getUser(id: string) {
    return this.repo.findById(id);
  }
}

// composition root (main.ts)
const repo = new PostgresUserRepo(pool);
const service = new UserService(repo);
```

### Test double

```typescript
const fakeRepo: UserRepo = {
  findById: async (id) => ({ id, name: 'Test' }),
};
const svc = new UserService(fakeRepo);
```

### Factory when impl chosen by config

```typescript
function createUserRepo(env: Config): UserRepo {
  return env.db === 'memory' ? new InMemoryRepo() : new PostgresRepo(pool);
}
```

### NestJS (framework DI)

```typescript
@Injectable()
class UserService {
  constructor(private repo: UserRepo) {}
}
// UserRepo bound in module providers array
```

### Express middleware as injectable chain

Each middleware receives `(req, res, next)` — deps wired when registering routes, not inside handler with globals.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tests hit prod DB | Real impl wired | Inject mock at test composition root |
| Circular dependency | A needs B needs A | Extract interface or third module |
| Container startup fails | Missing binding | Register all tokens in module |
| "Service not found" runtime | Service locator abuse | Constructor inject required deps |
| Too many constructor args | God object | Split bounded contexts |

## Gotchas

> [!WARNING]
> **Property injection frameworks** can construct partially initialized objects if circular deps misconfigured.

- **DI ≠ singleton** — container may return new instance per resolve unless scoped.
- **Over-injection** — 15-arg constructor signals missing facade or wrong boundary.
- **Dynamic `import()` for lazy DI** — track async init or first request fails.

## When NOT to use

- Pure functions with no external IO — pass args directly, no container.
- Script < 100 lines — manual wiring is clearer.

## Related

[[Design pattern/Bridge]] [[Design pattern/Command]] [[NodeJS/Express middleware]] [[Design pattern]]
