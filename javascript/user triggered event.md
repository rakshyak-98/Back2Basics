[[event listener]] [[Event Loop]] [[debouncing]] [[throttle]] [[content security policy]] [[dataTransfer]]

# User-triggered events

> Browser events caused directly by user input — the gate for privileged APIs, popup blockers, and "did the user mean this?" security checks.

```txt
        User-triggered eve ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **User-triggered events** to see if you understand what it…

## Sources
- [Wikipedia — user triggered event](https://en.wikipedia.org/wiki/user_triggered_event) — overview

## Key Concepts
- **Not all:** Not all DOM events are user-triggered
- **Categories: -:** Categories: - **Direct user events**
- **Common handlers:** Common handlers: `onclick`, `onchange`, `onselect`, `ondrag`, `ondrop`, `onsu…


- **Core:** Not all DOM events are user-triggered

## Technical Details
- Not all DOM events are user-triggered.
- **User activation:** (also called *transient activation*) is a browser-interna…
- It expires after a short window (~few seconds) and gates sensitive operations.

```
User click/tap/key
       │
       ▼
[ transient user activation ] ──► allowed: play(), open popup, fullscreen, clipboard write
       │
       │  setTimeout 5s later / await fetch first
       ▼
[ activation consumed or expired ] ──► blocked or requires permission prompt
```

- Categories:

- **Direct user events:** — `click`, `keydown`, `pointerdown`, `submit`, drag/drop initiated by user.
- **Synthetic but trusted:** — programmatic click on a focused button *may* count
- **Passive / document events:** — `scroll`, `mousemove` — not user activation for privileged APIs.

- Common handlers: `onclick`, `onchange`, `onselect`, `ondrag`, `ondrop`, `onsu…

### Register handlers (prefer explicit over inline HTML)

```js
button.addEventListener('click', (e) => {
  e.preventDefault(); // if needed — e.g. form submit
  handleUserAction();
}, { once: false, passive: false });
```

### Privileged APIs that require user gesture

```js
// Audio/video — autoplay policy
document.querySelector('video').play(); // throws or rejects without prior user gesture

// Popup
window.open('/help'); // blocked if not in click handler chain

// Fullscreen
await document.documentElement.requestFullscreen();

// Clipboard (write)
await navigator.clipboard.writeText('copied');

// File picker
input.click(); // works if triggered synchronously from user handler
```

### Preserve activation through async work

```js
button.addEventListener('click', async () => {
  // BAD: activation often lost after first await
  await fetch('/api/prepare');
  window.open('/result'); // likely blocked

  // GOOD: open synchronously in handler, navigate later
  const popup = window.open('about:blank');
  const res = await fetch('/api/prepare');
  popup.location = res.url;
});
```

### Passive listeners (scroll performance)

```js
// scroll/touch — mark passive so browser needn't wait for preventDefault check
window.addEventListener('touchstart', onTouch, { passive: true });
```

### React / framework pattern

```jsx
<button onClick={handleClick}>Save</button>
// Avoid: useEffect(() => window.open(...), []) — no user activation
```

## Mistakes to Avoid
- **Mistake:** **Activation does not survive `await`**
- **Mistake:** **`dispatchEvent` is not a user gesture**
- **Mistake:** **Delegated listeners still count**
- **Mistake:** **Third-party iframes**
- **Mistake:** **`play()` rejected / autoplay blocked:** check Was `play()` cal…
- **Mistake:** **`window.open` returns `null`:** check Popup blocker
- **Mistake:** **Clipboard write fails:** check No permission + no user gesture
- **Mistake:** **Fullscreen API rejects:** check Not user-initiated
- **Mistake:** **File upload dialog doesn't open:** check `input.click()` from …
- **Mistake:** **Double submit / duplicate API calls:** check No debounce on ra…

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Browser events caused directly by user input — the gate for privileged APIs, pop…).
- **Con / when not:** **Background automation**
- **Con / when not:** **Scroll handlers for "user intent"**
- **Con / when not:** **Global document listeners for everything**

## Comparison
- vs [[event listener]]: know when each applies


### Use cases
- In production APIs and tooling, **user triggered event** shows up whenever te…
