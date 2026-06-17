> [!NOTE]
> In a well architected application, the **Presentation Layer** should never communicate directly with the [[Data access Layer]]. Doing so creates tight coupling, making your code fragile and difficult to test.

- The Presentation Layer should interact exclusively with [[Service Layer]]


**The Recommended Flow of Communication**
- To achieve a clean, maintainable architecture, data flow should follow a strict hierarchy:

**Presentation Layer** -> Receives the user request (HTTP POST, UI button Click).
**Service Layer** -> Executes the business logic (validation, calculation, orchestrating multiple data sources).
Data Access Layer -> Performs the raw CRUD operations on the database.

### Why the Presentation Layer talks only to the Service Layer

- **Encapsulation of Complexity:** Your UI shouldn't know how the database is structured. If your database schema changes, you only update the Data Access Layer and potentially the Service Layer, leaving the Presentation Layer untouched.
    
- **Security & Validation:** Business rules (like "a user cannot withdraw more than their balance") belong in the Service Layer. If the UI talked to the Data Access Layer, someone could potentially bypass those rules by hitting the database directly.
    
- **Transactional Integrity:** A single user action might involve updating three different database tables. The Service Layer ensures these happen as one atomic transaction, preventing partial updates that would break your application.