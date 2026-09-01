Nginx handles the HTTPS/TLS connection from the client, decrypts the request, and then forwards the HTTP request to the backend server.

**Application-native TLS**
- the application opens as HTTPS/TLS listener directly.
- It loads the certificate/private key and performs the TLS handshake.
- Examples `net/http` Java Spring Boot/Tomcat, NodeJS HTTPS server.
- the application receives already-decrypted HTTP requests through i normal request-processing pipeline.
- **The application uses TLS library such as OpenSSL, BoringSSL or a language native TLS implementation.**