
### Interface

```go
type Animal interface {
	Speak() string
}

type Dog struct {}

func(Dog) Speak() string { return "Woof" }

func main(){
 var animal Animal = Dog{}
 animal.Speak()
}
```
- In GO, an **interface can only declare methods**. It cannot contain properties/fields