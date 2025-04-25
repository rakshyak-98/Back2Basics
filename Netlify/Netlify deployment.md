## Build `netlify.toml` file configuration

```toml
[build]
  command = "yarn run build"
  publish = ".next"

[[plugins]]
    package = "@netlify/plugin-nextjs"
```
