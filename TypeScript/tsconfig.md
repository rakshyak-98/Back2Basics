[[TypeScript]]

# tsconfig

> `tsconfig.json` — TypeScript compiler options, libs, paths, and project roots.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

#### change the lib compiler
### ts config not able to detect `types` modules
> if already have the `@types` package installed in your `node_modules`, but TypeScript is still unable to find them, you might need to add a `typeRoot` or `types` field in you `tsconfig.node.json` to explicitly specify where TypeScript should look for type definitions.
`tsBuildInfoFile`: option in the `tsconfig.json` file
- specifies the location where TypeScript should store incremental compilation information.
- these files helps typescript speed up subsequent compilations by storing information about the previous compilations.
- the `tsBuildInfoFile` option allows you to specify the path where this incremental compilation information should be stored.
> [!INFO] by compilation information is stored in a file named `.tsbuildinfo` in the same directory as the `tsconfig.json` file.

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
