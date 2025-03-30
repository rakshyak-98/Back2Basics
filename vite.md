### Environment variable
```js
const apiUrl = import.meta.env.VITE_API_URL;
console.log(apiUrl);

```
- you can not directly use `process.env` like in Webpack setup. Instead vite uses `import.meta.env` to access environment variables.
### Configuration
```javascript
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
- the `rewrite` function will remove the `/api` prefix from the path before forwarding the request to the target  