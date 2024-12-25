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
[[XSRF (cross-site request forgery)]]

## Browser cookie
[cookies, document.cookie](https://javascript.info/cookie)
If you run it, you will likely see multiple cookies. That’s because the `document.cookie=` operation does not overwrite all cookies. It only sets the mentioned cookie `user`.
- The `name=value` pair, after `encodeURIComponent`, should not exceed 4KB. So we can’t store anything huge in a cookie.
```js
document.cookie = "user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT"
```

> [!NOTE] Please note, by default, a cookie is not shared with a subdomain, such as `forum.site.com`.

Session cookies: By default, if a cookie doesn’t have one of these attributes, it disappears when the browser/tab is closed. Such cookies are called “session cookies”

When a user follows a legitimate link to `bank.com`, like from their notes, they’ll be surprised that `bank.com` does not recognize them. Indeed, `samesite=strict` cookies are not sent in that case
- We could work around that by using two cookies: one for “general recognition”, only to say: “Hello, John”, and the other one for data-changing operations with `samesite=strict`.
```js
samesite=lax // (same as `samesite` without value)
```

A `samesite=lax` cookie is sent if both of these conditions are true:

1. The HTTP method is “safe” (e.g. GET, but not POST).
   The full list of safe HTTP methods is in the [RFC7231 specification](https://tools.ietf.org/html/rfc7231#section-4.2.1). These are the methods that should be used for reading, but not writing the data. They must not perform any data-changing operations. Following a link is always GET, the safe method.
   
2. The operation performs a top-level navigation (changes URL in the browser address bar).
   This is usually true, but if the navigation is performed in an `<iframe>`, then it is not top-level. Additionally, JavaScript methods for network requests do not perform any navigation.