```txt
Error: [Immer] The plugin for 'MapSet' has not been loaded into Immer. To enable the plugin, import and call `enableMapSet()` when initializing your application.
```
- Whey using `Map` or `Set` inside `immer` `createSlice`.[[Immer]] doesn't support structural mutation tracking for `Map` / `Set`.

```js
import { configureStore } from '@reduxjs/toolkit';
import { enableMapSet } from 'immer';

enableMapSet();

```