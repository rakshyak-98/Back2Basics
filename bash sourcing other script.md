```bash
# Safe sourcing
LIB_DIR="$(dirname "${BASH_SOURCE[0]}")/lib"

if [[ -f "$LIB_DIR/utils.sh" ]]; then
    source "$LIB_DIR/utils.sh"
else
    echo "Error: utils.sh not found" >&2
    exit 1
fi
```