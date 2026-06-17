A **Service Layer** is a design pattern used in software architecture to act as an intermediary between the [[presentation layer]] (UI/API controllers) and the [[Data access Layer]] (repositories/databases).

- Encapsulate business logic, ensuring that your application follow the **Separation of Concerns** principle. Instead of controllers dealing with complex calculations, data validation, and transaction management, they simply delegate those tasks to the Service layer.

**Core Responsibilities**
- Business Logic Encapsulation -> Contains the core rules of your application (e.g., "Calculate interest", "check inventory before purchase", "generate invoice").
- Transaction Management -> Manages database transactions (begin, commit, rollback) to ensure data consistency across multiple operations.
- Decoupling -> Prevents the UI layer from knowing about database schema or specific persistence frameworks. This makes it easier to swap out a database or even change your front-end technology.
- Orchestration -> Coordinates calls to multiple repositories or external services. For Example a `UserRegistrationServiceq` might call a `UserRepository` to save the user, a `MailService` to send a welcome email, and a `LoggerService` to track the event.