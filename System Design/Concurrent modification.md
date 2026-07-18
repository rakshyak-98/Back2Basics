Any resource where multiple actors (users, services, or automated jobs) can read-modify-write the same record independently, with a gap between read and write.

Workflow/Status state machines
- Order/Subscription status transitions `pending -> active -> cancelled` a webhook from the payment provider and a customer support agent action both trying to transition the same order concurrently

> [!NOTE]
> If the API pattern is -> client does `GET` (reads full state) -> user/system computes a change -> client does `PUT/PATCH` (writes back full or partial state), and more than one client can plausibly do this against the same resource within a short window, it needs ETag/If-Match or an equivalent (version column, `updated_at` compare-and-swap).
> - If the pattern is `POST` to create a new resource where retries are the risk (not concurrent editors), it needs idempotency keys instead, different problem, different mechanism.
