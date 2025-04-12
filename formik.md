### Formik depends on **client-only React APIs**:
- `useState`, `useEffect`
- DOM events like `onChange`, `onSubmit`
- Direct manipulation of form elements
These **cannot run inside a Server Component** (RSC), which is rendered on the server and **never hydrated**.