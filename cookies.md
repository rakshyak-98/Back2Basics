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
[[cross-site scripting]]
[[cross-site request forgery]]

## Browser cookie
[cookies, document.cookie](https://javascript.info/cookie)
If you run it, you will likely see multiple cookies. That’s because the `document.cookie=` operation does not overwrite all cookies. It only sets the mentioned cookie `user`.
- The `name=value` pair, after `encodeURIComponent`, should not exceed 4KB. So we can’t store anything huge in a cookie.
```js
document.cookie = "user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT"
```

> [!NOTE] Please note, by default, a cookie is not shared with a subdomain, such as `forum.site.com`.