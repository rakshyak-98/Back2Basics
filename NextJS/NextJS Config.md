# How to set global package which is been fetched at the client side
```js

```

```js
const nextConfig = {
  images: {
    domains: ["example.com"]
  } }
```

```js
const nextConfig = {
	images: {
    remotePatterns: [
      { hostname: "example.com" },
    ],
  },
}
```

### Enable client side source map
```js
const nextConfig = {
  productionBrowserSourceMaps: true, // enable client side source map
}
```

```js
const nextConfig = {
	async redirects() {
		return [
			{
				source: '/old-path',
				destination: '/new-path',
				parament: true,
			}
		]
	}
}
```