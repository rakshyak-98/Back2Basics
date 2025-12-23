
## Installation

[doc](https://pkl-lang.org/main/current/pkl-cli/index.html)


```bash
pkl eval app.pkl;
pkl eval --format json app.pkl;
pkl eval --format yaml app.pkl;
```

- multiple environment 

```bash
pkl eval -p env=production app.pkl;
```


```pkl
// Most common style today
amends "package://pkg.pkl-lang.org/pkl-config/config@1.0.0#/Config.pkl"

local env = read("env:APP_ENV") ?? "development"

environment {
  name = env
  isProduction = env == "production"
  isDevelopment = env == "development"
}

// Then use it like:
logLevel = if (environment.isProduction) "info" else "debug"
```

## Separate files + import

```pkl
// Alternative popular style: separate files + import
// dev.pkl
amends "../base.pkl"

environment = "development"
database { host = "localhost" }
logLevel = "debug"

// prod.pkl
amends "../base.pkl"

environment = "production"
database { host = "db-prod.company.internal" }
logLevel = "warn"
```