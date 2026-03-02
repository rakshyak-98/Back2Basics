
Quick check if two directory have same content

```bash
diff -qr <dir1> <dir2> 
```
- `-q` → only report differences
- `-r` → recursive
- If no output → directories identical (names + content)

```bash
rsync -avnc --delete dir1/ dir2/
```
- `-n` -> dry run
- `-c` -> compare by checksum