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

### Prevent unintended dragging
```css
img {
	pointer-events: none;
	user-drag: none;
	-webkit-user-drag: none;
}

```

```js
function blockContextMenu(e){
	e.preventDefault();	
}

document.addEventListener("contextmenu", blockContextMenu)

```

#### Detect focus loss and add watermark

```js
function addWatermarkWhenScreenShot(e){
	document.hidden ? addWaterMark() : removeWaterMark();
}

function addWatermark() {
    let wm = document.createElement("div");
    wm.innerText = "Protected Content";
    wm.id = "watermark";
    document.body.appendChild(wm);
}

function removeWatermark() {
    let wm = document.getElementById("watermark");
    if (wm) wm.remove();
}

document.addEventListener("visibilitychange", addWatermarkWhenScreenShot)
```

```css
#watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 3rem;
    color: rgba(255, 0, 0, 0.5);
    pointer-events: none;
    z-index: 9999;
}

```

```js
function addWaterMarkWhenPrintKeyboardShortut(e){
	if ((e.key === "PrintScreen" ) || (e.ctrlKey && e.key === "p")){
		addWatermark();
		setTimeout(removeWatermark, 3000);
	}
}
document.addEventListener("keydown", addWaterMarkWhenPrintKeyboardShortut)

```

### Select Warning: The `value` prop supplied to `<select>` must be a scalar value if `multiple` is false.
- you are using a `<select>` element with `multiple={false}` (or by default, since `multiple` is `false` by default).
- you passed an array or non-scaler value to the `value` prop.

> [!INFO]
> react will warn here because `value` is an array, only allowed when `multiple={true}`
```html
<select value={["apple"]}>
	<option value="apple">Apple</option>
	<option value="banana">Banana</option>
</select>
```