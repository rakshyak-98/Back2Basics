- enable web server to store **stateful** information.
	- such as item added in shopping cart.
	- which page visited in the past.
	- track user's browsing activity (recording which page were visited in the past).
```shell
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: theme=light
Set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT
```
#### Authentication cookies
- authenticate user logged in, and with which account they are logged in.
	- without this user have to log in on each page.
- session cookies are intended to be deleted by the browser when the browser closes.
#### relates to
[[cross-site scripting]]
[[cross-site request forgery]]