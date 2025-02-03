defined in RFC 5321
- describes how how emails are sent between mail servers.

> [!INFO] SMTP communication follows a command-response model:

| Command    | Purpose                   | Example Response          |
| ---------- | ------------------------- | ------------------------- |
| HELO/ EHLO | Initiates conversation    | 250 Hello mail.eample.com |
| MAIL FROM: | Specifies sender email    | 250 OK                    |
| RCPT TO:   | Specifies recipient email | 250 OK                    |
| DATA       | Sends email content       | 354 Start mail input      |
| QUIT       | Ends session              | 221 Bye                   |
- SMTP is a push protocol, meaning it pushes emails from one server to another.
- It operates over port 25 (default), port 587 (submission with STARTTLS), and port 465 (Secure SSL/TLS).
- Works in a client-server model with a sequence of commands and responses.

### SMTP workflow
1. The client establishes a connection with the SMTP server using `HELO` or `EHLO`
2. Then sender's email is specified using `MAIL FROM:`.
3. The recipient's email is specified using `RCPT TO:`.
4. The email content is send using `DATA`, followed by a period `.` to signal the end.
5. The connection is terminated with `QUIT`.

### Key components

| Components                  | Role                                |
| --------------------------- | ----------------------------------- |
| SMTP Client                 | Initiates email sending             |
| SMTP Server                 | Receives and relays emails          |
| Mail Transfer Agent (MTA)   | Routes emails across servers        |
| Mail submission Agent (MSA) | Handles email submission (port 587) |
| Mail Delivery agent (MDA)   | Stores and delivers emails          |
