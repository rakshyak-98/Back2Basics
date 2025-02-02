```js
```
- Memoization of function:
	- preventing its recreation on every render unless its dependency array changes.
	- avoids expensive computations when passing functions as props to child components.


```ts
const setRef = useCallback((divRef: HTMLDivElement | null) => {
	if(divRef){
		// called with the element when it is mounted
	}else { 
		// called with null when the element is unmounted
	}
}, [])

// Pass callback function to ref prop
return <div ref={setRef} />
```
- Defining a `RefCallback` [what-react-refs-can-do-for-you](https://www.youtube.com/watch?v=TgpTG5XYoz4)
- Wrap with `useCallback` pre-render
- Called with the element on mount
- Called again with null when the element is unmounted
- Runs synchronously before paint
- Only runs once in StrictMode (v18)

### Context provider
- there is an issue if you wrap multiple component with Context provider component and assume all the state will be sync.
[Context provider]()
