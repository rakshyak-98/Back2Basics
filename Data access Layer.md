> [!INFO]
> The Data Access Layer defines how the application access and persists data. It exposes data-access interfaces and hides the details of the underlying database or storage system.

```go
type PromotionRepository interface {
    Save(p *Promotion) error
    FindByID(id string) (*Promotion, error)
    Delete(id string) error
}
```

```go
type PostgresPromotionRepository struct {
    db *sql.DB
}

func (r *PostgresPromotionRepository) Save(p *Promotion) error {
    // INSERT/UPDATE SQL
}
```
- this interface says **what the application can do with promotion data.**

> [!NOTE]
> The Data Access Layer **does contain implementations,** but it should not expose those implementation details to the layers above it.

> [!NOTE]
> Data Access Layer controls the implementations of data access, while the interface controls the correct exposed to the application and domain layer.

> [!NOTE]
> Data Access Layer controls the way the application accesses stored data and hides the storage-specific representation. The application shouldn't need to know that the data comes from a PostgreSQL table or that a particular SQL query was used.

**Domain says whether a change is allowed. DAL says how that change gets persisted.**

## When Business Layer directly executed database operations

```go
func CreatePromotion(id string) {
    db.Query("SELECT * FROM restaurants WHERE id = ?", id)
}
```
- This execution in the Business logic couples the Database connector with the Domain/Business Layer with Data access layer, Now these two can't be separated. Block us to use any other database connector.
- the **business logic directly knows about the database connector and SQL** creates **tight coupling**.

> [!NOTE]
> Now it means the Business Layer cannot independently change or be reused without knowing about the database implementation. You have to modify the business Layer because it contains PostgreSQL/SQL-specific knowledge.

**To solve this we introduce an interface**

Data Access Layer exposes this interface:
```go
type RestaurantRepository interface {
    FindByID(id string) (*Restaurant, error)
}
```

Business Layer does this:
```go
func CreatePromotion( id string, restaurantRepo RestaurantRepository) {

    restaurant, err := restaurantRepo.FindByID(id)

    // Business logic...
}
```
- the Business Layer "I have a capability called `FindByID`". And now database can change.

> [!INFO]
> When the Business/Domain Layer executes database operations, it becomes tightly coupled to the Data Access/Infrastructure implementation. This prevent the Business Layer from being independent of the database technology and makes replacing the database implementation require changes to business logic.

The Solution: 
Business defines the data-access capabilities it needs through an abstraction, while the Data Access Layer provides the concrete implementation of that abstraction. 