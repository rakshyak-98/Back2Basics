

```text
project-root/
├── public/                # Static assets (e.g., index.html, favicon)
├── src/
│   ├── presentation/      # UI components and views
│   │   ├── components/    # Reusable UI elements (e.g., Button, Modal)
│   │   ├── pages/         # Page-level views (e.g., HomePage, LoginPage)
│   │   ├── layouts/       # Shared layouts (e.g., MainLayout with header/footer)
│   │   └── styles/        # Global styles, themes (e.g., CSS modules, Tailwind config)
│   ├── application/       # App orchestration
│   │   ├── state/         # State management (e.g., Redux store, Vuex, or Context API)
│   │   ├── routes/        # Routing configuration (e.g., React Router setup)
│   │   ├── hooks/         # Custom hooks for app logic (e.g., useAuth)
│   │   └── services/      # Application services (e.g., orchestrators calling domain logic)
│   ├── domain/            # Core business logic
│   │   ├── entities/      # Data models (e.g., User, Product interfaces)
│   │   ├── usecases/      # Business rules/actions (e.g., validateUser, calculateTotal)
│   │   └── repositories/  # Abstract interfaces for data access (e.g., IUserRepository)
│   ├── infrastructure/    # External integrations
│   │   ├── api/           # API clients (e.g., Axios wrappers for endpoints)
│   │   ├── storage/       # Local storage, cookies, or IndexedDB adapters
│   │   ├── repositories/  # Concrete implementations of domain repositories
│   │   └── external/      # Third-party integrations (e.g., analytics, auth providers)
│   ├── utils/             # Shared utilities (e.g., date formatters, validators) – cross-cutting
│   ├── config/            # Environment configs (e.g., API URLs, feature flags)
│   └── index.ts           # Entry point (e.g., bootstraps the app)
├── tests/                 # Unit/integration tests, organized by layer
├── .eslintrc.js           # Linting rules
├── tsconfig.json          # TypeScript config (if using TS)
├── vite.config.js         # Build tool config (or webpack.config.js)
└── package.json           # Dependencies
```

#### Detailed Layer Guidelines

##### 1. Presentation Layer

- **Responsibility**: Render UI, handle user events, and display data. This layer should be "dumb" – no business logic, just props/state passing.
- **Key Files/Examples**:
    - Components: Atomic (Button), molecular (Form), organisms (UserProfileCard).
    - Pages: Compose components (e.g., HomePage fetches data via application hooks).
    - Styles: Use CSS-in-JS (Styled Components), SCSS, or utility-first (Tailwind).
- **Guidelines**:
    - Keep components pure and reusable.
    - Use hooks or lifecycle methods to connect to application layer.
    - Avoid direct API calls or storage access.
    - Example: A Button component receives onClick from parent; doesn't know what it does.

##### 2. Application Layer

- **Responsibility**: Coordinate flows, manage global state, and wire up domain logic to presentation.
- **Key Files/Examples**:
    - State: Centralized store (e.g., Redux actions/reducers for user auth state).
    - Routes: Define paths and protected routes.
    - Hooks/Services: Custom logic like useFetchUsers that calls domain use cases.
- **Guidelines**:
    - Handle side effects (e.g., via Redux Thunk or Vuex actions).
    - Inject dependencies (e.g., pass repositories to services).
    - This layer adapts domain outputs for UI (e.g., transform data for display).
    - Example: A service like AuthService calls domain/usecases/loginUser and updates state.

##### 3. Domain Layer

- **Responsibility**: Encapsulate business rules, entities, and logic. This is the "heart" of the app – pure, no external dependencies.
- **Key Files/Examples**:
    - Entities: Plain objects/interfaces (e.g., class User { id: string; name: string; }).
    - Use Cases: Functions/classes for operations (e.g., loginUser(email, password) validates and returns a token entity).
    - Repositories: Interfaces only (e.g., interface IUserRepository { getUser(id): Promise<User>; }).
- **Guidelines**:
    - Keep it framework-agnostic (pure JS/TS).
    - Focus on "what" the app does, not "how" (e.g., validation rules here, not in UI).
    - Test heavily – this layer should have 100% coverage.
    - Example: A use case throws domain-specific errors (e.g., InvalidCredentialsError).

##### 4. Infrastructure Layer

- **Responsibility**: Implement external concerns like data fetching, persistence, and adapters.
- **Key Files/Examples**:
    - API: HTTP clients (e.g., api/users.ts with fetch/Axios calls).
    - Storage: Wrappers for localStorage or databases.
    - Repositories: Concrete classes implementing domain interfaces (e.g., ApiUserRepository implements IUserRepository).
    - External: Integrations like Firebase Auth or Google Analytics.
- **Guidelines**:
    - Depend on domain abstractions (e.g., repositories inject into application/domain).
    - Handle errors and mapping (e.g., API response to domain entity).
    - Mock for testing (e.g., in-memory repo for unit tests).
    - Example: ApiUserRepository.getUser(id) calls /users/${id} and maps to User entity.

#### Implementation Steps for Developers

1. **Setup Boilerplate**:
    - Create the folder structure as above.
    - Install core deps: npm init, add TypeScript, ESLint, a framework (e.g., npm i react react-dom).
    - Configure build: Use Vite for fast setup (npm create vite@latest).
2. **Developing a Feature**:
    - Start from domain: Define entities and use cases.
    - Implement infrastructure: Add repo implementations.
    - Build application: Create services/hooks to orchestrate.
    - Finish with presentation: Build UI to consume application layer.
    - Example Workflow for "User Login":
        - Domain: User entity, loginUser use case.
        - Infra: AuthApiRepository with POST to /login.
        - App: useLogin hook calling use case.
        - Presentation: LoginPage with form using the hook.
3. **Testing & Maintenance**:
    - Unit Tests: Per layer (e.g., Jest for domain use cases).
    - Integration Tests: Cross-layers (e.g., API to UI).
    - Code Reviews: Enforce layer boundaries (no skipping layers).
    - Scaling: For monorepos, use this per package; for micro-frontends, replicate across apps.
4. **Common Pitfalls to Avoid**:
    - Don't put business logic in components (e.g., no validation in UI).
    - Avoid circular dependencies.
    - Keep utils lightweight; if complex, move to domain.
    - Regularly refactor as the project grows.