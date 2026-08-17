[[Jenkins]] [[npm/husk]] [[NodeJS/node command]] [[Github action]]

# Code Coverage

> Coverage tools instrument code, run tests, and report which lines and branches executed — they show what ran, not what was correctly asserted.





## Interview Relevance
Interviewers use coverage to see if you treat percentages as a signal, not a goal — and whether you know branch coverage, flaky inflation, and mutation testing beyond “we have 90%.”

## Sources
- [Wikipedia — Code coverage](https://en.wikipedia.org/wiki/Code_coverage) — overview
- [Istanbul / nyc](https://istanbul.js.org/) — overview
- [Jest — Coverage](https://jestjs.io/docs/configuration#collectcoverage-boolean) — deep-dive

## Core Definition
Code coverage measures which parts of a program were exercised during a test run (lines, branches, functions, statements). High coverage without strong assertions still ships bugs.

## Key Concepts
- **Line / statement coverage:** line entered at least once.
- **Branch coverage:** both outcomes of `if`/`switch` taken — stricter than line.
- **Function coverage:** function invoked at least once.
- **Instrumentation:** counters inserted before execution → report after suite.
- **Thresholds in CI:** ratchet gradually; diff coverage on PRs often beats global 95% on legacy code.
- **Mutation testing:** mutates code; tests should fail — finds weak assertions (e.g. Stryker).

## Technical Details
```
Source → instrument → run test suite → coverage report (% lines/branches/functions)
```

Jest:

```bash
npm test -- --coverage
```

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: ['src/**/*.{js,ts}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
};
```

nyc / Istanbul:

```bash
nyc --reporter=lcov --reporter=text npm test
```

Vitest:

```bash
vitest run --coverage
```

CI upload sketch:

```yaml
- run: npm test -- --coverage
- uses: codecov/codecov-action@v4
  with:
    files: ./coverage/lcov.info
```

Prefer narrowing `collectCoverageFrom` over blanket `/* istanbul ignore next */`.

| Symptom | Check | Fix |
|---------|-------|-----|
| Coverage dropped in PR | Diff coverage | Add tests for changed lines |
| 100% line, bugs ship | Weak assertions | Mutation testing; review tests |
| Flaky coverage % | Non-deterministic branches | Stabilize tests; seed RNG |
| Slow CI | Coverage on E2E only | Unit coverage in PR; E2E nightly |
| False 100% | Untested catch blocks | Exercise error paths |

## Real-World Applications
Pull requests fail if changed-line coverage drops; nightly jobs run mutation testing on critical payment modules.

**Example:** A PR hits 100% line coverage by calling functions without assertions — Stryker still survives mutants; fix the tests, not the percentage.

## Pros/Cons or Trade-offs
- **Pro:** Surfaces untested paths and guards regressions when thresholds are sensible.
- **Con:** Easy to game — execute code without asserting behavior.
- **Con:** Instrumentation and large suites slow CI if applied to every E2E run.

## Comparison
- vs mutation testing: coverage asks “did it run?”; mutation asks “would tests catch a bug?”
- vs lint-only gates: lint catches style; coverage catches unexercised paths — neither replaces production monitoring.
- vs [[Jenkins]] / [[Github action]] quality gates: coverage is one gate beside SAST and contract tests.

## Mistakes to Avoid
- Blocking merges on 95% global coverage for a legacy codebase — ratchet gradually.
- Measuring coverage on configuration-only or infrastructure repositories where the signal is meaningless.
- Ignoring generated protobuf/OpenAPI clients — exclude or separate thresholds.
- Treating line coverage as sufficient when branch coverage is what caught the null path.
