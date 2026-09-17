Hibernate is Java ORM that maps Java object to relational database tables and manages the SQL/database interaction needed to persist and retrieve those objects.

```txt
Java Application
       ↓
   Java Objects
       ↓
    Hibernate
       ↓
      SQL
       ↓
   Database
```

```java
@Entity
public class User {

    @Id
    private Long id;

    private String name;
}
```

Join fetch  tells Hibernate: "When you load this entity, load the related entities in the same database query."
It is primarily used to **avoid the N+1 query problem**

## Batch insert
Batch insert `GenerationType.IDENTITY` this is an important limitation.

```java
@Entity
class User {
	@ID
	@GenerateValue(strategy = GenerateType.IDENTIRY)
	private Long id;
	private String name;
}
```
Because of this, **Hibernate cannot generally batch `Identity` inserts in the same efficient way it can with sequence-base identifiers.** 

```java
@Id
@GenerateValue(stragegy = GenerateType.SEQUENCE)
private Long id;
```
- Hibernate can obtain IDs ahead of time

The exact SQL batching behavior depends on the database/JDBC driver/Hibernate-version, but the architectural advantage is that **Hibernate knows the identifiers before executing the inserts.**

> Hibernate's batching mechanism works best when it doesn't need to execute each insert immediately just to discover the generated primary key.

