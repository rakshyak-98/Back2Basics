[[event listener]] [[Event Loop]] [[debouncing]] [[throttle]] [[content security policy]] [[dataTransfer]]

# User-triggered events

> Browser events caused directly by user input — the gate for privileged APIs, popup blockers, and "did the user mean this?" security checks.





## Interview Relevance
Interviewers probe **User-triggered events** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Wikipedia — user triggered event](https://en.wikipedia.org/wiki/user_triggered_event) — overview

## Core Definition
Not all DOM events are user-triggered. **User activation** (also called *transient activation*) is a browser-internal flag set when the user clicks, taps, presses a key, etc. It expires after a short window (~few seconds) and gates sensitive operations.

## Key Concepts
- Not all DOM events are user-triggered. **User activation** (also called *transient activation*) is a browser-internal flag set when the user clicks, taps, presses a key, etc. It…
- Categories: - **Direct user events** — `click`, `keydown`, `pointerdown`, `submit`, drag/drop initiated by user. - **Synthetic but trusted** — programmatic click on a focused bu…
- Common handlers: `onclick`, `onchange`, `onselect`, `ondrag`, `ondrop`, `onsubmit`.

## Technical Details
Not all DOM events are user-triggered. **User activation** (also called *transient activation*) is a browser-internal flag set when the user clicks, taps, presses a key, etc. It expires after a short window (~few seconds) and gates sensitive operations.

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

Categories:
- **Direct user events** — `click`, `keydown`, `pointerdown`, `submit`, drag/drop initiated by user.
- **Synthetic but trusted** — programmatic click on a focused button *may* count; untrusted `dispatchEvent` from script generally does **not**.
- **Passive / document events** — `scroll`, `mousemove` — not user activation for privileged APIs.

Common handlers: `onclick`, `onchange`, `onselect`, `ondrag`, `ondrop`, `onsubmit`.

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

## Real-World Applications
In production APIs and tooling, **user triggered event** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Activation does not survive `await`** — any microtask/macrotask gap can consume transient activation. Open popups / start media **before** the first `await`; **`dispatchEvent` is not a user gesture** — tests and programmatic events won't unlock autoplay or popups; design UX for real clicks.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Browser events caused directly by user input — the gate for privileged APIs, pop…).
- **Con / when not:** **Background automation** — don't hack `click()` from `setInterval` to bypass policies; use proper permissions API or server-side flow.
- **Con / when not:** **Scroll handlers for "user intent"** — scrolling doesn't grant activation for popups/clipboard.
- **Con / when not:** **Global document listeners for everything** — attach to interactive elements; reduces noise and eases passive/listener tuning.

## Comparison
vs [[event listener]]: know when each applies — do not treat them as interchangeable. vs [[Event Loop]]: know when each applies — do not treat them as interchangeable. vs [[debouncing]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Activation does not survive `await`** — any microtask/macrotask gap can consume transient activation. Open popups / start media **before** the first `await`.
- **`dispatchEvent` is not a user gesture** — tests and programmatic events won't unlock autoplay or popups; design UX for real clicks.
- **Delegated listeners still count** — activation propagates from real user target; use event delegation on `document` without losing gesture if handler runs synchronously.
- **Third-party iframes** — cross-origin frames have separate activation; embedding payment or OAuth flows must happen in direct user navigation or sanctioned iframe APIs.
- **`play()` rejected / autoplay blocked:** check Was `play()` called outside click/tap handler?; fix: Call `play()` synchronously inside user event; mute for autoplay fallback
- **`window.open` returns `null`:** check Popup blocker; lost activation after `await`; fix: Open window sync in handler; use `<a target="_blank">`
- **Clipboard write fails:** check No permission + no user gesture; fix: Trigger from `click`; use `navigator.permissions.query`
- **Fullscreen API rejects:** check Not user-initiated; fix: Bind to button `click`
- **File upload dialog doesn't open:** check `input.click()` from setTimeout; fix: Call `click()` synchronously in user handler
- **Double submit / duplicate API calls:** check No debounce on rapid clicks; fix: Disable button during request; [[debouncing]]
