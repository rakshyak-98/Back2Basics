
| **Command**                                 | **Description**                            |
| ------------------------------------------- | ------------------------------------------ |
| `jq '.' file.json`                          | Pretty-print JSON                          |
| `jq '.key' file.json`                       | Extract a key's value                      |
| `jq '.key1.key2' file.json`<br>             | Access nested keys                         |
| `jq '.[0]' file.json`                       | Access first array element                 |
| `jq '.[]' file.json`                        | Iterate over an array                      |
| `jq '.[].key' file.json`                    | Extract key from all objects in an array   |
| `jq 'map(.key)' file.json`                  | Extract key from all objects (alternative) |
| `jq 'select(.key=="value")' file.json`      | Filter objects by key value                |
| `jq 'map(select(.key=="value"))' file.json` | Filter objects in an array                 |
| `jq 'length' file.json`                     | Get array length                           |
| `jq 'keys' file.json`                       | Get object keys                            |
| `jq 'has("key")' file.json`                 | Check if key exists                        |
| `jq 'del(.key)' file.json`                  | Remove a key                               |
| `jq 'sort' file.json`                       | Sort an array                              |
| `jq 'unique' file.json`                     | Get unique values from an array            |
| `jq 'group_by(.key)' file.json`             | Group objects by key                       |
| `jq 'add' file.json`                        | Sum array of numbers                       |
| `jq 'map_values(. * 2)' file.json`          | Multiply all values by 2                   |
| `jq 'to_entries' file.json`                 | Convert object to array of key-value pairs |
| `jq 'from_entries' file.json`               | Convert array of key-value pairs to object |
| `jq -r '.key' file.json`                    | Output raw string (no quotes)              |
| `jq -c '.' file.json`                       | Compact output (no pretty-print)           |
- `jq` is a lightweight and powerful command-line JSON processor.
- it allows you to parse, filter, transform, and manipulate JSON data efficiently in a Unix-like environment.

#### Transforming with `jq`
```shell
jq 'map(.key)' #Extract a key from all objects in an array
jq 'map_values(.*2)' #Multiply all numeric values by 2
jq 'to_entries' #Convert an object into an array of key-value pairs
jq 'from_entries' #Convert an array of key-value pairs back to an object
jq 'with_entries(.key|=ascii_upcase)' #Convert object keys to uppercase
jq 'map(if .key>10 then .key=10 else . end)' #Modify values conditionally
jq 'map({newKey:.oldKey})' #Rename keys in an array of objects
jq 'del(.key)' #Remove a specific key from an object
jq 'map(del(.unwantedKey))' #Remove a key from all objects in an array
jq 'group_by(.category)' #Group objects by a specific key
jq 'map({(.id):.name})|add' #Convert an array of objects to a key-value object
jq 'join(",")' #Convert an array of strings into a single CSV string
jq 'sort_by(.key)' #Sort an array of objects by a key
jq 'reverse' #Reverse an array
jq 'flatten' #Flatten nested arrays into a single-level array
jq 'split(" ")' #Split a string into an array by spaces
jq 'map_values(tostring)' #Convert all values in an object to strings
jq 'map(.key|=tonumber)' #Convert string numbers to actual numbers

```