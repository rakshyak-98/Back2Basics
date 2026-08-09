[[vite]]

# vite internal

> vite internal — you can not directly use process.env like in Webpack setup. Instead vite uses import.meta.env to access environment variables.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** vite internal — plain job, how I run it, how I know it’s broken.


### Environment variable
```js
const apiUrl = import.meta.env.VITE_API_URL;
console.log(apiUrl);
```
- you can not directly use `process.env` like in Webpack setup. Instead vite uses `import.meta.env` to access environment variables.
### Conditional config
```js
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  if (command === 'serve') {
    return {
      // dev specific config
    }
  } else {
    // command === 'build'
    return {
      // build specific config
    }
  }
})
```
### Configuration
```js
server: {
	proxy: {
		"/api": {
			target: "http://jsonplaceholder.typeicode.com"
		}
	}
}
```
- the purpose of this code is to redirect these API requests to a different server, in this case `http://jsonplaceholder.typeicode.com`.
- often used during development to avoid issues with Cross-Origin Resource Sharing or to simulate a back-end server that isn't running locally.
- when a request is made to a URL starting with `/api` on local development server, vite will intercept this request and forward it to the specified target URL.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **vite internal** | Core idea of this note | “I can explain vite internal without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[vite]]
