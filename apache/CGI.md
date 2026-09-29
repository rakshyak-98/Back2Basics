The **Common Gateway Interface** is a standard that lets a web server run an external program to generate a dynamic HTTP response.

**Browser → Web Server → CGI Program → Web Server → Browser**

CGI therefore defines the **interface between the web server and the application program.** The program can receive request information through environment variables and standard input, and it sends its response through standard output.

Common Gateway Interface -> is a standard protocol that allows a web server to interact with external programs (called CGI scripts or programs) to generate dynamic content, rather than just serving static files.

Process per request -> Each CGI invocation spawns a new process, which is resource-intensive (slow for high traffic). This is why modern alternatives like FastCGI, mod_php, or application servers (Node.js) are preferred.


> [!INFO]
> CGI was foundational for early dynamic web sites in the 1990s but is rarely used for new projects due to performance overhead.