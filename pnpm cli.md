`pnpm approve-builds` -> is a security feature. Its purpose is to explicitly allow packages to execute install/build scripts.

```bash
```
- there is supply-chain security risk.

Some npm packages execute scripts automatically during installation.
- `esbuild` needs to download a platform-specific binary during `postinstall`.
- instead of blindly executing it, `pnpm` may block it and ask for approval.

`pnpm approve-build` -> it opens interactive prompt to approve packages that are allowed to execute build/ install scripts. After approval, `pnpm` records the decision in your project configuration.