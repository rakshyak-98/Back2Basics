[[cross-site scripting]]

# cookies configuration

> cookies configuration — set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT

## Mental model

**Say it in one breath:** cookies configuration — set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT

[cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cookie)
```shell
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: theme=light
Set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT
httpOnly
```

## Related

[[cross-site scripting]]
