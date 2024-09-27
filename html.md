#### How to suppress the automatic requests for `favicon.ico` in web

```html
<head>
	<link rel='icon' href='data:,' />
<head>
```
- browser make a default request for `favicon.ico` on each page load.

### Browser specific methods to suppress automatic favicon requests
- firefox `about:config`
- search `browser.chrome.favicons`

```txt
Layout was forced before the page was fully loaded. If stylesheets are not yet loaded this may cause a flash of unstyled content. markup.js:250:53
```
- indicates that the browser is rendering elements before all CSS stylesheets have been fully loaded, leading to a [[Flash of Unstyled Content]] (FOUC).
