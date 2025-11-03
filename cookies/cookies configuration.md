[cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cookie)
```shell
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: theme=light
Set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT
httpOnly
```

> [!INFO] `httpOnly` attribute forbids any JavaScript access to the cookie. We can't see such a cookie or manipulate it using `document.cookie`

> [!NOTE] Cookies have several attribute, many of which are important and should be set.
```js
document.cookie = "user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT"
```

> [!WARNING] By default, if a cookie doesn't have one of these attributes, it disappears when the browser/tab is closed.
> Such cookies are called **session cookies** (max-age, expires)

#### Authentication cookies
- the cookie should be transferred only over HTTPS (`secure` key). By default, if we set a cookie at `http://site.com`, then it also appears at `https://site.com` and vice versa.
- authenticate user logged in, and with which account they are logged in.
	- without this user have to log in on each page.
- session cookies are intended to be deleted by the browser when the browser closes.

[[cross-site scripting]]
[[XSRF (cross-site request forgery)]]

> [!NOTE] You can set/update a single cookie at a time using `document.cookie`

## Browser cookie

[cookies, document.cookie](https://javascript.info/cookie)
If you run it, you will likely see multiple cookies. That’s because the `document.cookie=` operation does not overwrite all cookies. It only sets the mentioned cookie `user`.

> [!NOTE] The `name=value` pair, after `encodeURIComponent`, should not exceed 4KB. So we can’t store anything huge in a cookie.

> [!NOTE] The total number of cookies per domain is limited to around 20+ the exact limit depends on the browser.

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

### Cookies attributes

> [!NOTE] There's no way to let a cookie be accessible from another 2nd-level domain (it is safety restriction)
- We have to explicitly set the `domain` attribute to the root domain `domain=site.com`. Then all sub-domain will see such a cookie.

> [!INFO] usually we should set `path` to the root: `path=/` to make the cookie accessible from all website pages.

> [!WARNING]- cookies with `samesite=strict` is never sent if the user comes from outside the same site.
> - weather a user follow a same link from their email, submits a form outside the same site.
> - user does any operation that originates from another domain, the cookie is not sent.

### Fix localhost cookies error (not being sent in request API from client browser)

- in production, frontend and backend are likely on the same origin or subdomain, so cookies are automatically sent. In development they are on different origins (ports), so you must set `credentials: 'include'`.
- subdomain based setup -> when frontend and backend are on different origin, set `sameSite: 'none'` and `secure: true` (when using HTTPS) in cookies. Have backend set with `Access-Control-Allow-Credentials: true`.

> [!INFO]
> Browser blocks cookies by default in cross-origin unless
> - `fetch(..., { credentials: true })` is used.
> - Backend CORS has `credentials: true`.
> - Cookie is set with correct `sameSite` and `secure` flags.


```js
axios.defaults.withCredentials = true;
```