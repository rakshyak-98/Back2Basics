[[NextJS]]

# How to set global package which is been fetched at the client side

> How to set global package which is been fetched at the client side — productionBrowserSourceMaps: true, // enable client side source map

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

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

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
