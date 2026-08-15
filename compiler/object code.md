[[compiler]] [[library file]] [[compile time]] [[clang]]

# Object code

> Compiler output for one translation unit — machine instructions and symbols in a relocatable file (`.o` / `.obj`), not yet a finished program.

## Interview Relevance

Interviewers check that you know compile vs link: unresolved symbols are often link-time, and object files still need relocation addresses filled in.

## Sources

- [Wikipedia — Object file](https://en.wikipedia.org/wiki/Object_file) — overview
- [man elf](https://man7.org/linux/man-pages/man5/elf.5.html) — deep-dive

## Key Concepts

- **Relocatable object:** addresses not final → linker patches references.
- **Symbols:** defined vs undefined → `nm` shows what this `.o` provides/needs.
- **Sections:** `.text`, `.data`, `.bss`, `.rodata` → code vs data layout.
- **One `.c` → one `.o`:** common TU mapping (unity builds are the exception).

## Technical Details

```bash
clang -c main.c -o main.o
nm main.o
objdump -d main.o
readelf -h main.o    # ELF header (Linux)
```

| Stage | Output |
|-------|--------|
| Compile (`-c`) | Object file |
| Link | Executable or shared lib |
| Archive | `.a` of objects — [[library file]] |

Object code is a product of a compiler (or assembler); it is not generally runnable alone.

## Real-World Applications

Incremental builds: only recompile changed TUs to new `.o` files, then relink — the core of `make`/`ninja` speed.

**Example:** `undefined reference to foo` after a clean compile — `foo.o` was never linked; fix the link line / build graph.

## Pros/Cons or Trade-offs

- **Pro:** Separate compilation scales large codebases.
- **Con:** API changes in headers force many TUs to rebuild; opaque link errors if graphs are wrong.

## Comparison

- vs executable: objects still need linking and relocation.
- vs bytecode: object code usually means native relocatable machine code; bytecode targets a VM.

## Mistakes to Avoid

- Calling any compiler output “the binary” — distinguish `.o`, `.so`, and the final executable.
- Checking in object files instead of sources.
- Debugging link errors by only re-running the compiler without the linker command.
