
> [!NOTE] Please stop using builder patterns for JavaScript SDK

## Modular architecture
- Components and plugins are separate modules that need to be explicitly registered before they can be used.
- the modular architecture allows for better tree-shaking (dead code elimination ) by bundlers like Web-pack.
- By only importing and registering the components you need, you can reduce the final bundle size.

### Reduce Bundles size

#### modular architecture ref 
- [valibot](https://www.builder.io/blog/valibot-bundle-size)
- [Jared Palmer bachelor's thesis](https://valibot.dev/thesis.pdf)
- [Dropbox article](https://dropbox.tech/frontend/how-we-reduced-the-size-of-our-javascript-bundles-by-33-percent)
- [Strategies of crafting High-performance web apps](https://dev.to/codebeast/strategies-for-crafting-high-performance-web-apps-with-smaller-bundle-sizes-2mmj)