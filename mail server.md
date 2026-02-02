- handles sending, receiving, routing, and storing of email messages across the internet.

|Protocol|Full Name|Main Job|Direction|Typical Ports (secure)|Keeps emails on server?|Best for|
|---|---|---|---|---|---|---|
|**SMTP**|Simple Mail Transfer Protocol|Sending emails (outgoing)|Client → Server → Server|465 (SSL), 587 (STARTTLS)|No (just transfers)|Sending emails from any client|
|**IMAP**|Internet Message Access Protocol|Retrieving & managing emails (incoming)|Server → Client|993 (SSL/TLS)|Yes (syncs across devices)|Using email on phone + laptop|
|**POP3**|Post Office Protocol v3|Retrieving emails (incoming)|Server → Client|995 (SSL/TLS)|Usually no (downloads & deletes)|Single-device use, saving space|

### Why It Matters

- If you're setting up email in an app → you need correct SMTP/IMAP/POP3 server addresses, ports, and login credentials.
- If you're sending bulk/marketing emails → using your own mail server (or a transactional service like SendGrid, Amazon SES) is often required to avoid spam filters.
- Security note: almost all real mail servers today require encryption (STARTTLS or SSL/TLS) and authentication.