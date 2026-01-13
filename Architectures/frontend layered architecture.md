

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