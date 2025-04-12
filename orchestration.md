sequencing of multiple tasks, services, or components to achieve a defined workflow or system behavior.

Examples:
- Ensure service A starts before B, restart on failure, scale based on load.
- sequence APIs to fulfill business logic.

> [!INFO] Refactoring hint
> - avoid orchestration unless workflow complexity justifies it.
> - user orchestration when you need
> 	- central error handling
> 	- retries / timeouts
> 	- strict sequencing


