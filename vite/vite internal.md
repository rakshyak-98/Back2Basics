[[vite]]

# vite internal

> vite internal — you cannot use process.env like in a Webpack setup; Vite exposes environment variables through import.meta.env instead.

---

## Mental model

**Say it in one breath:** During development and build, Vite injects `VITE_*` variables into `import.meta.env`; `process.env` is not populated the same way as in Webpack.

### Environment variable

```js
const apiUrl = import.meta.env.VITE_API_URL;
console.log(apiUrl);
```

- You cannot read `process.env` the same way as in Webpack. Use `import.meta.env` for values defined in `.env` files with the `VITE_` prefix.

### Conditional configuration

```js
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  if (command === 'serve') {
    return {
      // development-specific configuration
    }
  } else {
    // command === 'build'
    return {
      // production build configuration
    }
  }
})
```

### Development server proxy

```js
server: {
	proxy: {
		"/api": {
			target: "http://jsonplaceholder.typeicode.com"
		}
	}
}
```

- Redirects browser requests that start with `/api` to the target server.
- Used during development to avoid Cross-Origin Resource Sharing errors or to stand in for a backend that is not running locally.
- When the browser requests `/api/...` on the local development server, Vite intercepts the request and forwards it to the target URL.

---

## Related

[[vite]]
