
```txt
# List all paste buffers with their contents
tmux list-buffers

# Show the content of the most recent buffer
tmux show-buffer

# Save the most recent buffer to a file
tmux save-buffer ~/copied-output.txt

# Save a specific buffer (by index) to a file
tmux save-buffer -b 0 ~/buffer0.txt

# Load a file into the paste buffer
tmux load-buffer ~/some-text.txt

# Delete all buffers
tmux delete-buffer -a
```