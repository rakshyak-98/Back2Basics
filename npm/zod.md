Making field options

```js
cosnt schema = z.object({
	descriptino: z.string().max(500).optionl(),
	images: z.array(z.string()).url().optionl();
	starRating: z.number().int().min(1).max(5).optionl(),
})
```

Default values

```js
const schema = z.object({
	role: z.enum(["admin", "user", "guest"]).default("guest"),
	theme: z.enum(["light", "dark"]).default("guest").optional().default("light"),
})
```

`superRefine` and `refine`

```js
const authSchema = z.object({
	email: z.string().email(),
	password: z.string().min(8).optional(),
	confirmPassword: z.string().optional(),
}).superRefine((data, ctx) => {
	if (data.password !== undefined){
		if(data.confirmPassword === undefined){
			ctx.addIssue({
				code: z.ZodIssueCode.invalid_type,
				expected: 'string',
				received: 'undefined',
				path: ['confirmPassword'],
				message: 'Confirm password is required when setting a password',
			});
		} else if (data.password !== data.confirmPassword){
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				path: ['confirmPassword'],
				message: 'Password do not match',
			})
		}
	}
})
```

```js
const contactSchema = z.object({
  email: z.string().email().optional(),
  phone: z.string().regex(/^\+?[1-9]\d{1,14}$/).optional(),
}).superRefine((data, ctx) => {
  if (!data.email && !data.phone) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'At least one of email or phone is required',
      path: [], // or ['email'] / ['phone'] depending on UX
    });
  }
});
```

`.transform()` Clean & powerful data shaping

```js
const userCreateSchema = z.object({
	fullName: z.string().min(2),
	birthYear: z.number().int().min(1900).max(new Date().getFullYear() - 13),
	role: z.enum(['user', 'admin', 'guest']).default('user'),
}).transform((data) => ({
	...data,
	slug: data.fullName
		.toLowerCase().replace(/\s+/g, '-')
}))
```

## Db query with validation

```js
const usernameCheck = z.string().min(3).superRefine(async (val, ctx) => {
  const exists = await db.user.findFirst({ where: { username: val } });
  if (exists) {
    ctx.addIssue({
      code: 'custom',
      message: 'Username already taken',
      path: ['username'],
    });
  }
});
```

## Error handling

```js
	
  if (err instanceof zod.ZodError) {
    response.error = "Validation error";
    response.message = zod.treeifyError(err); // zod provider error formator native support
  }
	
```