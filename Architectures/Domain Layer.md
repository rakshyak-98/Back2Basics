> [!INFO]
> Instead of allowing different parts of the application to directly update business data, the domain layer provides controlled operations that enforce the business rules required for the update. This keeps the rules governing related data changes in one place.

if rule of the Domain is violated, it lead to rule duplication on different ranges of the service layer and can leak into different layers. With the domain layer the data object controls **how its state is allowed to change**.

```go
func (p *Promotion) Publish() error {
    if p.Status != Ready {
        return errors.New("promotion cannot be published")
    }

    p.Status = Published
    return nil
}
```
- and reset of the application uses `promotion.Publish()`. Avoid other layer to directly update the data. Other layers call the action to "Perform the business action called Publish".

> [!INFO]
> The domain object then decides **whether that action is valid and what data must change as a result**.

> [!WARNING]
> Without a centralized domain operation, different code paths may update only part of the required state. Which leads to inconsistency in business data.

```txt
API A:
    Status = PUBLISHED

Admin API:
    Status = PUBLISHED
    PublishedAt = now

Background Job:
    VideoURL = ...
    Status = PUBLISHED
```

> [!INFO]
> The Domain layer doesn't exist merely to "update data". It owns the business meaning of a state change. Instead of exposing raw update, it exposes business actions, and those actions enforce the rules and perform the related state change together.