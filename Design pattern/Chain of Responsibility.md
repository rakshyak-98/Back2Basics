[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Template Method]] [[NodeJS/Express middleware]]

# Chain of Responsibility

> Pass a request along a chain of handlers until one handles it (or all approve) — **Dive Into Design Patterns + launch validation chain**.

---

## Index

- [[#Mental model]]
- [[#Core idea]]
- [[#Variations / implementations]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#Trade-offs]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Ordered checks: authentication → goal → page → creative → budget. Each handler does one job; on success calls `next`, on failure short-circuits with an error. Open for extension: append a handler without editing others.

```
LaunchValidationChain
  AuthHandler → GoalHandler → PageHandler → CreativeHandler → BudgetHandler → OK
```

| Role | Responsibility |
|------|----------------|
| **Handler** | Can process or forward |
| **Concrete handler** | One check / concern |
| **Client** | Builds chain; sends request to first link |

## Core idea

…

## Variations / implementations

…

## Standard config / commands

```typescript
interface LaunchContext {
  userId: string;
  goalId: string;
  budget?: number;
}

type Handler = (ctx: LaunchContext, next: () => Promise<void>) => Promise<void>;

function compose(handlers: Handler[]): Handler {
  return async (ctx) => {
    let i = 0;
    const next = async (): Promise<void> => {
      if (i >= handlers.length) return;
      const h = handlers[i++];
      await h(ctx, next);
    };
    await next();
  };
}

const validateLaunch = compose([
  async (ctx, next) => {
    if (!ctx.userId) throw new Error('unauthorized');
    await next();
  },
  async (ctx, next) => {
    if (!ctx.goalId) throw new Error('goal required');
    await next();
  },
  async (ctx, next) => {
    if ((ctx.budget ?? 0) <= 0) throw new Error('budget');
    await next();
  },
]);
```

Express / Koa middleware is the same pattern — see [[NodeJS/Express middleware]].

### Extending

New launch check → new handler → append to chain registration. Do not grow a god `validateEverything()`.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Handler never runs | Forgotten in compose list | Single chain factory |
| Order bugs (budget before auth) | Array order | Document required order; tests |
| Handler does HTTP launch | Scope creep | Validation only; launch in Pipeline |
| Silent success on failure | Forgot to throw / didn't call next wrongly | Fail closed; don't call next on error |

## Gotchas

> [!WARNING]
> Calling `next()` after already failing, or swallowing errors, breaks the chain contract — one clear success path.

- Chain + Strategy: a handler may *delegate* to a strategy (goal-specific rules) without becoming a strategy itself.
- Pure functional `compose` avoids class boilerplate; classes help when handlers need injected deps.

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

## When NOT to use

- One check — a function is enough.
- All checks always run and combine errors — use a list of validators + aggregate, not short-circuit chain (unless you want fail-fast).

## Related

[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Command]] [[Design pattern/Template Method]] [[NodeJS/Express middleware]] [[MongoDB/mongoose middleware]]
