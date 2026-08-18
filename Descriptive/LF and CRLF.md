[[Descriptive]] [[Markdown]]

# LF and CRLF

> LF (`\n`) and CRLF (`\r\n`) are line endings — Unix vs classic Windows; mismatches break scripts and diffs.

## Mental model

**Say it in one breath:** Text lines must end somehow; Git `core.autocrlf` / `.gitattributes` keep the repository consistent across OS.

```txt
LF = \n          CRLF = \r\n
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **LF** | Unix/macOS default | “Shell scripts need LF.” |
| --- | --- | --- |
| **CRLF** | Windows default | “Notepad legacy.” |
| **`.gitattributes`** | Force eol per path | `* text=auto eol=lf` |
| **shebang break** | `#!/bin/bash\r` | “bad interpreter” |

## Standard config / commands

```bash
file file.sh           # shows CRLF if present
dos2unix file.sh       # to LF
unix2dos file.sh       # to CRLF
printf '\r\n' | od -c
```

```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
```

| Knob | Why it matters |

| autocrlf | Local checkout conversion |
| --- | --- |
| Editor “EOL” | Save with correct ending |
| Docker build scripts | Must be LF |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| bad interpreter | CRLF shebang | dos2unix |
| Noisy git diffs | eol churn | .gitattributes |
| Make fails weirdly | `\r` in Makefile | Convert to LF |
| CI only | checkout eol | Align attributes |

## Gotchas

> [!WARNING]
> **Mixing eol in one file** — some tools only look at first line.

> [!WARNING]
> **Binary marked as text** — autocrlf can corrupt; set binary in attributes.

## When NOT to use

- **Binary formats** — don’t “normalize” images.
- **Protocols that define their own framing** — HTTP already specifies CRLF in headers.

## Related

[[Markdown]] [[Linux/commands/SSH]]
