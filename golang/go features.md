> [!NOTE]
> - Go intentionally makes iteration order unpredictable. To prevent developers from accidentally relying on map iteration order.
> - Go doesn't have class inheritance.

### Struct embedding (closest to `extends`)

```go
type Animal struct {}

func (a *Animal) Eat() {
	fmt.Println("Eating")
}

type Cat struct {
	Animal
}

// Override methods. This is method shadowing
func (c *Cat) Eat() {
	fmt.Println("Cat eating")
}

func main(){
	cat := Cat{}
	cat.Eat()
}

```
- Although `Cat` doesn't define `Eat()`, the method is promoted from the embedded  `Animal`