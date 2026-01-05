```bash
greet() {
    local name="$1"        # Assign first argument to a variable (good practice)
    local age="$2"

    if [ -z "$name" ]; then
        echo "Error: Please provide a name."
        return 1           # Return error code
    fi

    echo "Hello, $name!"
    [ -n "$age" ] && echo "You are $age years old."
}

# Usage
greet "Alice" 30
greet "Bob"
greet                   # Shows error
```
