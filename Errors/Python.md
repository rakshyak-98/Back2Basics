[[Descriptive/webdriver]] [[Python]] [[Errors]]

# Python errors (Selenium stale element)

> `StaleElementReferenceException` means the WebElement you hold no longer points at a DOM node — the page re-rendered and your reference died.

```txt
        Python errors (Sel ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Automation interviews: explain staleness, re-find elements after DOM updates,…

## Sources
- [Selenium — Stale element](https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/#staleelementreferenceexception) — deep-dive
- [Selenium — Waits](https://www.selenium.dev/documentation/webdriver/waits/) — overview

## Key Concepts
- **Element reference:** ID tied to a specific DOM node instance.
- **Stale:** DOM replaced/removed after navigation, React re-render, or AJAX refresh.
- **Fix:** locate again; wait for conditions; reduce long-held references.
- **Other common Python test errors:** timeouts, NoSuchElement — different root causes.

## Technical Details
```python
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_retry(driver, by, value, tries=3):
    for _ in range(tries):
        try:
            el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))
            el.click()
            return
        except StaleElementReferenceException:
            continue
    raise
```

| Error | Meaning |
|-------|---------|
| `StaleElementReferenceException` | Old reference after DOM change |
| `NoSuchElementException` | Not present (yet/wrong selector) |
| `TimeoutException` | Wait condition never true |

## Mistakes to Avoid
- **Mistake:** Storing elements in lists across page updates
- **Mistake:** Fixed `time.sleep` as the only synchronization strategy
- **Mistake:** Catching all exceptions and continuing silently

## Pros/Cons or Trade-offs
- **Pro:** Explicit waits make intent clear.
- **Con:** Over-retry can hide real product bugs — bound attempts.

## Comparison
- vs Playwright auto-waiting: similar problem space with different defaults.
- vs unit tests: UI tests are coupled to render timing by nature.


### Use cases
- UI test suites for SPAs: every click that triggers re-render may invalidate p…

- **Example:** Find rows, click “delete,” then assert on the same row variable
