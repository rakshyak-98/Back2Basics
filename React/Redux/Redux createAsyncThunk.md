```js
// features/user/userThunks.ts
import { createAsyncThunk } from '@reduxjs/toolkit'

export const fetchUserById = createAsyncThunk(
  'user/fetchById',
  async (userId: string, thunkAPI) => {
    const res = await fetch(`/api/users/${userId}`)
    if (!res.ok) return thunkAPI.rejectWithValue('Fetch failed')
    return res.json()
  }
)

```

```js
// features/user/userSlice.ts
import { createSlice } from '@reduxjs/toolkit'
import { fetchUserById } from './userThunks'

const initialState = {
  data: null,
  status: 'idle', // 'loading' | 'succeeded' | 'failed'
  error: null,
}

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserById.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(fetchUserById.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.data = action.payload
      })
      .addCase(fetchUserById.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.payload
      })
  },
})

export const userReducer = userSlice.reducer

```

## Use in component
```js
// in a React component
const dispatch = useAppDispatch()
const user = useAppSelector((state) => state.user)

useEffect(() => {
  dispatch(fetchUserById('123'))
}, [])

```
