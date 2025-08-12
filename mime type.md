## set the recommended (default) application for a mime type on your system
```bash
xdg-mime query default mime/type;
xdg-mime default vim.desktop text/plain;
```

### mime type
- `/etc/mime.types` 
- `/usr/share/mime` -> system wide
- 

```bash
xdg-mime query default inode/directory; # get the information of file manager
gio mime <mime-type>;
```


#### Make the mount permanent
- automatically mounted at boot, you can add an entry to `/etc/fstab` file.
```txt
tmpfs <path> tmpfs size=100M 0 0
```

```bash
df -h; #verify the mount
```

`application/octet-stream` -> generic MIME type for arbitrary binary data. Used when the actual file type is **unknown** or **not declared**.

application -> indicates non-text data (application-level content).
octet-stream -> sequence of 8-bit bytes (no specific format/encoding).

> [!INFO]
> use to force download in browsers. Many servers send this type with a `Content-Disposition: attachment` header to trigger file save dialog.