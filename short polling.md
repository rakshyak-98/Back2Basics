**Short polling** communication technique client send requests to a server at regular intervals to check whether new data or an update is available.
- The server responds to each request immediately with a current result, event if nothing has changed.

- Server repeatedly performs work to answer requests, even when nothing has changed. As number of client increases, these unnecessary requests consume server resources that could otherwise be used for actual business operations.

**When is short polling a good decision?**
short polling is a reasonable choice when:
- updates are not requried instantly
- the number of concurrent users is relatively small.
- The API response is lightweight.
- Database queries are inexpensive and properly indexed.
- Simplicity is more valuable than real-time responsiveness.