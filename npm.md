### peer dependency conflict during the `npm install` process
`npm warn ERESOLVE overriding peer dependency`
- it means the dependency resolution mechanism detected a mismatch between the expected versions of dependencies specified by a package and the actual versions being installed.

##### how to resolve
```shell
npm info <package> peerDependencies; # view peer dependencies
npm install <package>; # install compatible peer dependencies
npm install --legacy-peer-deps; # force install peer dependencies

```
