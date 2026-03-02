```text
Error: 400 {"type":"error","error":{"type":"invalid_request_error","message":"messages.4: `tool_use` ids were found without `tool_result` blocks immediately after: toolu_018XLoNZDysSCZitFpMk8qf3. Each `tool_use` block must have a corresponding `tool_result` block in the next message."},"request_id":"req_011CYYJdG5Hrm8eASvwh19fo"}
```

- it means claude returned a `tool_use` block but your code didn't send back a `tool_result` for it.

---

```text
Error: 429 {"type":"error","error":{"type":"rate_limit_error","message":"This request would exceed your organization's rate limit of 10,000 input tokens per minute (org: 8bdf8921-d1f0-461a-aa8c-83ebf25f39ae, model: claude-opus-4-5-20251101). For details, refer to: https://docs.claude.com/en/api/rate-limits. You can see the response headers for current usage. Please reduce the prompt length or the maximum tokens requested, or try again later. You may also contact sales at https://www.anthropic.com/contact-sales to discuss your options for a rate limit increase."},"request_id":"req_011CYYRzSbTRCSGijrV661t9"}

```