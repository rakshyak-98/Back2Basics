[[DevOps/Jenkins]] [[npm/husk]] [[NodeJS/node command]] [[Design pattern/Dependency Injection]]

# Code Coverage

> Percentage of source lines/branches executed by tests — guide, not quality proof — **Istanbul/nyc + CI gates**.

## Mental model

Coverage tools **instrument** code (counters at branches/lines), run tests, report what executed.

```
Source → instrument → run test suite → coverage report (% lines/branches/functions)
```

High coverage ≠ correct behavior — it shows **what ran**, not **what was asserted**.

| Metric | Meaning |
|--------|---------|
| **Line** | Line entered at least once |
| **Branch** | Both outcomes of if/switch taken |
| **Function** | Function invoked |
| **Statement** | Similar to line in JS |

## Standard config / commands

### Jest (built-in coverage)

```bash
npm test -- --coverage
# jest.config.js
module.exports = {
  collectCoverageFrom: ['src/**/*.{js,ts}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
};
```

### nyc / Istanbul (Node)

```bash
nyc --reporter=lcov --reporter=text npm test
# Output: coverage/lcov.info for Codecov/Sonar
```

### Vitest

```bash
vitest run --coverage
```

### CI upload (Codecov example)

```yaml
- run: npm test -- --coverage
- uses: codecov/codecov-action@v4
  with:
    files: ./coverage/lcov.info
```

### Exclude generated/dead code

```javascript
/* istanbul ignore next */
if (process.env.UNREACHABLE) { … }
```

Prefer narrowing `collectCoverageFrom` over blanket ignores.

### Mutation testing (beyond coverage)

```bash
npx stryker run   # mutates code; tests should fail — finds weak assertions
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Coverage dropped in PR | Diff coverage | Add tests for changed lines |
| 100% line, bugs ship | Assertions weak | Mutation testing; review test quality |
| Flaky coverage % | Non-deterministic branches | Stabilize tests; seed RNG |
| Slow CI | Coverage on E2E only | Unit coverage in PR; E2E nightly |
| False 100% | Untested catch blocks | Test error paths explicitly |
| Instrumentation breaks build | ESM/CJS mismatch | Use provider supported by test runner |

## Gotchas

> [!WARNING]
> **Gaming coverage** — tests that execute code without assertions inflate numbers.

- **Generated code** (protobuf, OpenAPI client) — exclude or separate threshold.
- **Branch coverage** harder than line — `if (x) return` needs two tests.
- **Integration tests** may double-count same lines — acceptable if intentional.

## When NOT to use

- Don't block merge on 95% global threshold for legacy codebase — ratchet gradually.
- Don't measure coverage on config-only or infra repos — meaningless signal.

## Related

[[DevOps/Jenkins]] [[npm/husk]] [[NodeJS/node command]] [[Design pattern/Dependency Injection]]
