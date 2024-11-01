## Allow multiple rendering strategies
- Being able to use multiple rendering strategies is probably the main reason why we want to use NextJS
### NextJS
- it allows us to define the behavior of page rendering at the page level 
- means we can define how we want to render each page individually 
- support multiple rendering strategies
### `src` folder structure
- components: all shared components that are used across the entire application
- config: application configuration files
- features: different feature-based things. should contain specific code for a given feature.
	- api: API request declarations and API hooks related to a specific feature. Makes our API layer and UI layer separate and reusable
	- components: contains all components that are scoped to a specific feature.
	- types: type definitions to a specific feature.
	- `index.ts` entry point of every feature. It should only export things that should be public for other parts of the application.
- layouts: different layout of pages
- lib: configuration for different libraries
- pages: application pages
- providers: all application providers
- stores: contains all global state stores that are used in the application
- testing: test related mocks, helpers, utilities, and configurations.
- types: base typescript type definitions that are used across the application
- utils: contains all shared utility functions

> [!NOTE] we can combine all the application providers in `providers` and export a single application provider with we can wrap `App.tsx`
