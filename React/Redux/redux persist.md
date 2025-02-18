### Configure Persist Reducer
```js
import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // Uses localStorage
import rootReducer from './reducers';

const persistConfig = {
  key: 'root', 
  storage, 
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
});

const persistor = persistStore(store);

export { store, persistor };

```

### What is `PersistGate` in Redux Persist?
`PersistGate` is a component from `redux-persist/integration/react` that delays rendering of the app until the persisted state is rehydrates (restored from storage).
- Ensures Redux state is fully loaded before rendering the app.
- Prevents issues where the UI might render with empty state before rehydration.
- Displays a loading fallback (spinner, text) while restoring the state.

```js
import { PersistGate } from 'redux-persist/integration/react';
import { Provider } from 'react-redux';
import { store, persistor } from './store';
import App from './App';

function Root() {
  return (
    <Provider store={store}>
      <PersistGate loading={<h1>Loading...</h1>} persistor={persistor}>
        <App />
      </PersistGate>
    </Provider>
  );
}

```