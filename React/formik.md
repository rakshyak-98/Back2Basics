[[react hooks]] [[React State management]] [[React Architecture]]

# Formik

> Form state library for React — values, validation, and touched/error tracking without hand-rolling every field.

## Interview Relevance

Interviewers compare controlled forms, Formik, and React Hook Form — performance on large forms and validation strategy.

## Sources

- [Formik docs](https://formik.org/docs/overview) — deep-dive
- [React — <input>](https://react.dev/reference/react-dom/components/input) — overview

## Core Definition

Formik owns form values and meta (touched, errors, submit count) and wires inputs through `Field` or `useFormik`.

## Key Concepts

- **Initial values + schema:** often Yup/Zod validation.
- **Touched vs error:** show errors after blur/submit, not on first keystroke unless intended.
- **Submit:** async handlers with `setSubmitting` / error mapping.

## Technical Details

```tsx
<Formik initialValues={{ email: '' }} onSubmit={async (v) => api.subscribe(v.email)}>
  {({ errors, touched }) => (
    <Form>
      <Field name="email" type="email" />
      {touched.email && errors.email}
      <button type="submit">Join</button>
    </Form>
  )}
</Formik>
```

## Real-World Applications

Multi-step signup wizard with shared Formik state across steps and server-side field errors mapped back into `setErrors`.

## Pros/Cons or Trade-offs

- **Pro:** Fast to ship medium forms with validation UX.
- **Con:** Large forms may prefer React Hook Form for fewer re-renders.

## Comparison

- vs controlled inputs alone: Formik adds validation/meta plumbing.

## Mistakes to Avoid

- Validating only on the client and trusting it on the server.
- Remounting Formik on every parent render and wiping values.
