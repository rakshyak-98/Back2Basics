[[Descriptive]] [[Java applets]] [[Operating System/JVM]]

# Java Basic

> Java basics — classes, `javac`/`java`, JVM bytecode, and the usual entrypoint `main`.

```txt
        Java Basic ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers may probe Java Basic as tooling or web platform literacy

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
.java → javac → .class → java Main
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **JVM** | Runtime | “Write once, run on JVM.” |
| **Bytecode** | Portable instructions | “Not machine code yet.” |
| **classpath** | Where classes live | “Missing jar = ClassNotFound.” |
| **static main** | Entry | `public static void main(String[] args)` |

## Technical Details
```bash
javac Hello.java
java Hello
java -cp target/classes:lib/* com.example.App
```

```java
public class Hello {
  public static void main(String[] args) {
    System.out.println("hi");
  }
}
```

| Knob | Why it matters |
|------|----------------|
| `--source/--target` | Compatibility |
| Module path | JPMS apps |
| Heap `-Xmx` | Memory cap |

## Mistakes to Avoid
> [!WARNING]
> **File name = public class name** — `Hello.java` must hold `public class Hello`.

> [!WARNING]
> **Classpath hell** — duplicate classes; prefer a build tool (Maven/Gradle).

| Symptom | Check | Fix |
|---------|-------|-----|
| ClassNotFoundException | classpath | Fix `-cp` / build |
| UnsupportedClassVersion | newer bytecode than JVM | Upgrade JRE or retarget |
| No main | wrong class | Point to class with main |
| Package mismatch | folder vs package | Match directory layout |

## Pros/Cons or Trade-offs
- **Tiny CLI glue** — scripting language may be faster to ship.
- **Browser applets** — dead; use modern web stacks.
