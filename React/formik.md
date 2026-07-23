[[RSC (React Server Component boundaries)]] [[react hooks]] [[React State management]] [[React Pattern/Controlled and Uncontrolled component Pattern]]

# Formik

> React form state library — values, touched, errors, submit lifecycle — **client-only** (needs DOM + hooks) — **Formik docs**.

---

## Mental model

Formik centralizes form state in one object:

```txt
values / errors / touched / isSubmitting
        ↓
<Field> or connect handlers → validation (sync or Yup) → onSubmit
```

Compared to raw `useState` per field: less boilerplate, consistent submit/validation flow. Compared to React Hook Form: Formik re-renders more (often whole form on keystroke) unless optimized.

| Piece | Role |
|-------|------|
| `initialValues` | Default shape |
| `validate` / `validationSchema` | Yup schema common |
| `onSubmit` | Async-safe; set `isSubmitting` |
| `<Field>` | Wires name → value/onChange |

**Cannot run in Server Components** — uses `useState`, `useEffect`, DOM events. Mark form tree `"use client"` ([[RSC (React Server Component boundaries)]]).

---

## Standard config / commands

```tsx
"use client";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const schema = Yup.object({
  email: Yup.string().email().required(),
  password: Yup.string().min(8).required(),
});

export function LoginForm() {
  return (
    <Formik
      initialValues={{ email: "", password: "" }}
      validationSchema={schema}
      onSubmit={async (values, { setSubmitting, setFieldError }) => {
        try {
          await api.post("/login", values);
        } catch (e: any) {
          setFieldError("email", e.message ?? "Login failed");
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <Form>
          <Field name="email" type="email" />
          <ErrorMessage name="email" component="div" />
          <Field name="password" type="password" />
          <button type="submit" disabled={isSubmitting}>Sign in</button>
        </Form>
      )}
    </Formik>
  );
}
```

### `enableReinitialize` for edit forms

```tsx
<Formik enableReinitialize initialValues={userFromApi ?? defaults} ... />
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Whole app re-renders typing | Large Formik tree | Split forms; React Hook Form; `FastField` |
| Validation never fires | `validateOnBlur` false | `validateOnChange` / submit |
| Values stale after props load | Missing reinitialize | `enableReinitialize` |
| RSC error "useState only client" | Form in Server Component | `"use client"` boundary |
| Double submit | No `isSubmitting` guard | Disable button; [[debouncing]] onSubmit |

---

## Gotchas

> [!WARNING]
> **Nested objects** — shallow updates need care; consider flat names or libraries like Immer inside custom handlers.

> [!WARNING]
> **File inputs** — special-case; not standard controlled value.

---

## When NOT to use

- **Server Actions + native `<form>`** — Next.js can post without Formik for simple flows.
- **Huge dynamic field arrays (100+)** — React Hook Form performance often wins.
- **Non-React surfaces** — web components without React bindings.

---

## Related

[[React Pattern/Controlled and Uncontrolled component Pattern]] · [[React State management]] · [[API handling]] · [[RSC (React Server Component boundaries)]]
