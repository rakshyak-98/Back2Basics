[install](https://www.npmjs.com/package/class-transformer)

```ts
import { plainToInstance, Exclude, Expose } from "class-transformer";

class UserDTO {
    @Expose() id: string;
    @Expose() name: string;
    @Expose() email: string;
    @Exclude() password: string; // Exclude password from response

    constructor(partial: Partial<UserDTO>) {
        Object.assign(this, partial);
    }
}

// Express Route using class-transformer
app.get("/users/:id", async (req, res) => {
    const user = await UserModel.findById(req.params.id);
    if (!user) return res.status(404).json({ error: "User not found" });

    const serializedUser = plainToInstance(UserDTO, user.toObject());
    res.json(serializedUser);
});

```