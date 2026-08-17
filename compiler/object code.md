[[compiler]] [[library file]] [[compile time]] [[clang]]

# Object code

> Compiler output for one translation unit — machine instructions and symbols in a relocatable file (`.o` / `.obj`), not yet a finished program.

```txt
        Object code ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check that you know compile vs link: unresolved symbols are ofte…

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

- Object code is a product of a compiler (or assembler)

## Mistakes to Avoid
- **Mistake:** Calling any compiler output “the binary”
- **Mistake:** Checking in object files instead of sources
- **Mistake:** Debugging link errors by only re-running the compiler without th…

## Pros/Cons or Trade-offs
- **Pro:** Separate compilation scales large codebases.
- **Con:** API changes in headers force many TUs to rebuild; opaque link errors if graphs are wrong.

## Comparison
- vs executable: objects still need linking and relocation.
- vs bytecode: object code usually means native relocatable machine code; bytecode targets a VM.


### Use cases
- Incremental builds: only recompile changed TUs to new `.o` files, then relink

- **Example:** `undefined reference to foo` after a clean compile
