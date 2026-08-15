[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[html]] [[Debugger configuratoin]]

# webdriver

> WebDriver is the W3C API for driving browsers — Selenium talks WebDriver to click, type, and assert UI.

## Interview Relevance

WebDriver interviews cover browser automation — flaky selectors, waits, and CI reliability.

## Sources

- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts

```txt
test → WebDriver → chromedriver → Chrome
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Driver** | Browser binary bridge | “Version must match browser.” |
| **Locator** | How to find elements | “CSS/xpath; avoid brittle paths.” |
| **Explicit wait** | Wait for condition | “Not blind sleep.” |
| **Grid** | Remote browsers | “Parallel CI.” |

## Technical Details

```js
const driver = await new Builder().forBrowser('chrome').build()
await driver.get('https://example.com')
await driver.findElement(By.css('h1'))
await driver.quit()
```

| Knob | Why it matters |
|------|----------------|
| Browser/driver version | Protocol mismatches |
| Headless | CI without display |
| Implicit wait | Can hide races — prefer explicit |

## Pros/Cons or Trade-offs

- **Unit logic tests** — no browser needed.
- **API contracts** — HTTP tests are cheaper.

## Mistakes to Avoid

> [!WARNING]
> **Sleep(1000) everywhere** — slow and still flaky; wait for conditions.

> [!WARNING]
> **XPath tied to layout** — one CSS change breaks the suite.

| Symptom | Check | Fix |
|---------|-------|-----|
| Session not created | driver/browser mismatch | Align versions / Selenium Manager |
| Flaky element | timing | Explicit wait / better selector |
| Stale element | DOM re-render | Re-find element |
| CI only fails | headless / res | Set viewport; await network |

