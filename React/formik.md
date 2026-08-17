[[react hooks]] [[React State management]] [[React Architecture]]

# Formik

> Form state library for React — values, validation, and touched/error tracking without hand-rolling every field.

```txt
        Formik ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers compare controlled forms, Formik, and React Hook Form

## Sources
- [Formik docs](https://formik.org/docs/overview) — deep-dive
- [React — <input>](https://react.dev/reference/react-dom/components/input) — overview

## Key Concepts
- **Initial values + schema:** often Yup/Zod validation.
- **Touched vs error:** show errors after blur/submit, not on first keystroke unless intended.
- **Submit:** async handlers with `setSubmitting` / error mapping.


- **Core:** Formik owns form values and meta (touched, errors, submit count) and wires in…

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

## Mistakes to Avoid
- **Mistake:** Validating only on the client and trusting it on the server
- **Mistake:** Remounting Formik on every parent render and wiping values

## Pros/Cons or Trade-offs
- **Pro:** Fast to ship medium forms with validation UX.
- **Con:** Large forms may prefer React Hook Form for fewer re-renders.

## Comparison
- vs controlled inputs alone: Formik adds validation/meta plumbing.


### Use cases
- Multi-step signup wizard with shared Formik state across steps and server-sid…
