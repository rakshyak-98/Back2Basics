## Orchestration of the service

```go
type PromotionApplicationService struct {
    restaurantService   RestaurantService
    subscriptionService SubscriptionService
    promotionRepo       PromotionRepository
    videoService        VideoService
}

func (s *PromotionApplicationService) CreatePromotion(
    ctx context.Context,
    input CreatePromotionInput,
) (*Promotion, error) {

    // 1. Resolve the restaurant
    restaurant, err := s.restaurantService.Get(ctx, input.RestaurantID)
    if err != nil {
        return nil, err
    }

    // 2. Check whether the restaurant is allowed
    if err := s.subscriptionService.Validate(restaurant.ID); err != nil {
        return nil, err
    }

    // 3. Create the promotion
    promotion := NewPromotion(restaurant.ID, input)

    // 4. Persist it
    if err := s.promotionRepo.Save(ctx, promotion); err != nil {
        return nil, err
    }

    // 5. Trigger the next operation
    if err := s.videoService.Generate(ctx, promotion.ID); err != nil {
        return nil, err
    }

    return promotion, nil
}
```
- Application layer decides what happens and in what order
- The individual service/components decide how their own responsibility is performed. [[Service Layer]]

> [!INFO]
> The application layer should generally contain the workflow of the use case, while the services it calls contain the specialized logic for their respective responsibilities.