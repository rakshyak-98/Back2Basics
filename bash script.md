
- Start every script with a shebang

```bash
#!/bin/bash
```

- Save the file (e.g., `myscript.sh`)
- Make it executable

```bash
chmod +x myscript.sh;
```

- Run it

```bash
./myscript.sh
```

## Variables

```bash
name="World"
count=42
```

use with `$`

```bash
echo "Hello, $name!";
echo "Count, ${count}"; # Curly braces for clearity
```

## Output echo

```bash
echo "Hello, World!":
echo -n "No newline"; # -n suppresses newline
echo -e "Line\nLine2"; # -e enables backslash escape
```

## User input: read

```bash
echo "Enter your name:"
read name
echo "Hi, ${name}";
```

```bash
read -p "Enter age: " age
```

## Command-line arguments

```bash
echo "First arg: $1"
echo "All arg: $@"
echo "Number of args: $#"
```

## Conditionals (if-else)

```bash
if [ "$age" -gt 18 ]; then
	echo "Adult"
elif [ "$age" -lt 18 ] then
	echo "Minor"
else
	echo "Exactly 18"
if
```

- common tests
	- `-eq` `-ne` `-lt` `-gt` `-le` `-ge` (numbers)
	- `=`, `!=` (strings)
	- `-f file` (file exists), `-d dir` (directory exists)


## Loop

```bash
for i in 1 2 3 4 5 6; do
	echo "Number: ${i}"
done
```

```bash
for i in {1..5}; do
	echo $i
done
```

```bash
count=1
while [ $count -le 5 ]; do
	echo $count
	((count++))
done
```

### String Manipulation

- Remove suffix

```bash
folder="beachside-hotel"
new="${folder%-hotel}";
```

- Remove prefix

```bash
new="${folder#hotel-}"
```

- Replace

```bash
new="${folder/-hotel/}"
```

## Function

```bash
greet() {
	echo "Hello, ${1}!"
}
```

## Arithmetic

```bash
((sum = 5 + 3))
echo $sum  # 8
((count++))  # Increment
```