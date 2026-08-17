[[Descriptive]] [[Java applets]] [[Operating System/JVM]]

# Java Basic

> Java basics — classes, `javac`/`java`, JVM bytecode, and the usual entrypoint `main`.





## Interview Relevance
Interviewers may probe Java Basic as tooling or web platform literacy — expect a crisp definition, how it works, and when it is the wrong tool.

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
.java → javac → .class → java Main
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
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

## Pros/Cons or Trade-offs
- **Tiny CLI glue** — scripting language may be faster to ship.
- **Browser applets** — dead; use modern web stacks.

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
