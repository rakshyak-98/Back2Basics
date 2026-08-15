[[golang/go]] [[golang/go functions]] [[golang/go data structure]] [[golang/go error]]

# Go strings — bytes, UTF-8, and runes

> Go strings — bytes, UTF-8, and runes — a Go string is not a sequence of characters. It is an immutable, read-only view over a byte

## Interview Relevance

Strings/runes/bytes trips up candidates who assume “character index” — UTF-8, `range` over runes, and immutability are the interview traps.

## Sources

- [Go blog — Strings, bytes, runes and characters in Go](https://go.dev/blog/strings) — deep-dive
- [Go spec — String types](https://go.dev/ref/spec#String_types) — deep-dive

## Key Concepts

```txt
string "aé"
┌───┬───┬───┐
│ a │ é │   │   len(s) == 3  (bytes, not runes)
│1B │ 2B│   │   runes: 'a', 'é'  → 2 characters
└───┴───┴───┘
     s[0]     s[1]        s[2]
     'a'      1st byte    2nd byte of 'é'
              of 'é'
```

- `s[i]` returns a `byte` (`uint8`) at index `i` — **not** a character.
- `len(s)` returns the **byte length**, not the number of Unicode code points.
- Multi-byte characters (`é`, `Ω`, emojis) occupy 2–4 bytes in UTF-8. Indexing into the middle of one yields a single byte, not a valid character.

**Character-safe alternatives:**

| Need | Approach |
|------|----------|
| Iterate characters | `for i, r := range s` — `r` is a `rune` (`int32` code point) |
| Index by character position | `[]rune(s)` then `runes[i]` |
| Byte offsets for substrings | `unicode/utf8` — `RuneCountInString`, `DecodeRuneInString`, `ValidString` |

```go
s := "aé"

// Byte indexing — wrong mental model for "characters"
len(s)   // 3
s[0]     // 'a'
s[1]     // first byte of 'é' only — not 'é'

// Rune-safe indexing
runes := []rune(s)
runes[0] // 'a'
runes[1] // 'é' — whole character regardless of byte width
```

> [!NOTE]
> Converting to `[]rune` makes indexing **character-safe**:
> - `runes[0]` is `'a'`
> - `runes[1]` is `'é'` (the whole character, regardless of how many bytes it took to store it)

## Technical Details

### Iterate runes (preferred for most loops)

```go
for i, r := range s {
    // i = byte offset of r; r = rune (code point)
    _ = i
    _ = r
}
```

### Character count and indexing

```go
import "unicode/utf8"

n := utf8.RuneCountInString(s) // rune count, not len(s)
runes := []rune(s)
if len(runes) > 1 {
    _ = runes[1]
}
```

### Substring by byte range (valid UTF-8 boundary required)

```go
// s[start:end] slices bytes — cut only on rune boundaries or use utf8 helpers
sub := s[0:1] // safe for ASCII prefix only
```

### Compare and search

```go
import "strings"

strings.Contains(s, "é") // works — compares UTF-8 text, not raw byte halves
```

Prefer `strings`, `unicode/utf8`, and `range` over manual `s[i]` when handling user-facing text.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `len(s)` disagrees with visible character count | `utf8.RuneCountInString(s)` vs `len(s)` | Treat `len` as bytes; use rune count or `[]rune` for display limits |
| Garbled output or invalid UTF-8 after slice | `utf8.ValidString(sub)` on `s[i:j]` | Slice only at rune boundaries; build substrings with `range` or `utf8` decode |
| `s[i] == 'é'` or byte compare fails for accented text | Log `s[i]` as `%#v` — often a single UTF-8 byte | Compare runes (`rune(s[i])` is wrong for multi-byte); use `strings` or decode first |
| Truncation breaks last character (e.g. API max length) | Last byte is continuation byte `0x80–0xBF` | Truncate by runes: `string([]rune(s)[:n])` or walk with `utf8.DecodeRuneInString` |
| Emoji / combining marks counted wrong | `len([]rune(s))` vs grapheme clusters | For user-perceived length, use a locale/grapheme library; runes ≠ user-visible glyphs |

## Pros/Cons or Trade-offs

- **Trade-off:** Do not convert every string to `[]rune` by default — binary protocols, file paths, and wire formats are byte-oriented; `string`/`[]byte` is correct there.
- **Trade-off:** Do not use `s[i]` for parsing human text — use `range`, `strings`, or `unicode/utf8`.
- **Trade-off:** Do not assume one rune = one screen column — width, emoji sequences, and combining marks need domain-specific handling.

## Mistakes to Avoid

- **`s[i]` is a byte, not a character.** On `"aé"`, `s[1]` and `s[2]` are the two bytes of `é`. Using either alone in comparisons, hashing, or encryption corrupts the character.
- **`len(s)` is byte length.** A 140-character tweet limit implemented as `len(s) <= 140` will reject or accept the wrong strings once non-ASCII appears.
- **`[]rune(s)` allocates and copies.** Fine for small strings and correctness-critical paths; avoid in hot loops over large text — use `range` or `utf8` iterators instead.
- **Runes are Unicode code points, not grapheme clusters.** `"e\u0301"` (e + combining acute) is two runes but often displays as one glyph `é`.
