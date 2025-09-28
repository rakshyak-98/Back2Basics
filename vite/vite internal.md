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
- the `changeOrigin: true`  setting tells the proxy to change the origin of the request to match the target server, which can help prevent certain CORS issues.
- the `rewrite` function will remove the `/api` prefix from the path before forwarding the request to the target.

#### Set base path for deployment
if deploying a sub-directory
```ts
import { defaultConifg } from 'vite';
import react from "@vitejs/plugin-react";

export default defineConfig({
	plugins: [react()],
	base: '/my-app/', // change this based on your deployment URL
})

```

```ts
export default defineConfig({
	build: {
		target: 'esnext',
		minify: 'terser',
		sourcemap: false, // disable source maps (set to `true` if debugging )
	}
})
```

### `Source map error: No sources are declared in this source map. Resource URL: [http://localhost:8080/node_modules/.vite/deps/chunk-WOOG5QLI.js?v=16298d72](http://localhost:8080/node_modules/.vite/deps/chunk-WOOG5QLI.js?v=16298d72 "http://localhost:8080/node_modules/.vite/deps/chunk-WOOG5QLI.js?v=16298d72") Source Map URL: chunk-WOOG5QLI.js.map`

> [!INFO] the browser is trying to access a source amp, but vite isn't properly serving it.

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    port: 8080, // Ensure the correct port is used
  },
  build: {
    sourcemap: mode === 'development', // Enable source maps in development
  },
  optimizeDeps: {
		// fixs missing source maps for dependiencies like `node_modules/.vite/deps/*`
    esbuildOptions: {
      sourcemap: mode === 'development', // Ensure dependencies also get source maps.
    },
  },
}));

```

## PostCSS
- anytime your `import "./style.css"` in your code, vite runs the file through PostCSS pipeline.

> [!INFO]
> vite looks for PostCSS config in your project root: `postcss.config.js` `postcss.config.cjs` `postcss.config.mjs` `postcss.config.json` or inline config inside `vite.config.js` under `css.postcss`