```shell
npm install <package>@<version>;
npm install <pacakge> --save-exact;
npm ci; # install dependincies from `package-local.json` (clean install).
```

```shell
npm update <pacakge>; # update package to the latest minor/patch version.
npm outdated; # list outdated packages.
npm upgrade; # updates all dependencies to the latest compatible versions.
npm dedupe; # remove duplicate dependencies.
```

```shell
npm show <package>; # show packages.
npm view <pacakge> version; # list available versions.
```

### Npm configuration
```shell
npm config list;
npm config set <ke> <value>;
npm config delete <key>;
npm cache clean --force;
```

### Npm package info
```shell
npm view <pacakge> dependencies;
npm info <pacakge>;
npm repo <pacakge>; # open repository in the browser.
npm search <pacakge>; # search for the package matching the keyword.
npm explain <package>; # explains why a package is installed.
```
