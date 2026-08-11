[[Descriptive]] [[Java applets]]

# Java Basic

> Java basics — classes, `javac`/`java`, JVM bytecode, and the usual entrypoint `main`.

---

## Mental model

**Say it in one breath:** Source → bytecode (`.class`) → JVM executes; packages and classpath find your types.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| ClassNotFoundException | classpath | Fix `-cp` / build |
| UnsupportedClassVersion | newer bytecode than JVM | Upgrade JRE or retarget |
| No main | wrong class | Point to class with main |
| Package mismatch | folder vs package | Match directory layout |

---

## Gotchas

> [!WARNING]
> **File name = public class name** — `Hello.java` must hold `public class Hello`.

> [!WARNING]
> **Classpath hell** — duplicate classes; prefer a build tool (Maven/Gradle).

---

## When NOT to use

- **Tiny CLI glue** — scripting language may be faster to ship.
- **Browser applets** — dead; use modern web stacks.

## Related

[[Java applets]] [[Operating System/JVM]]
