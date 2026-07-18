The `~/Templates` directory in Linux is part of the XDG user directories standard.
- It allow you to create custom file templates that appear in your file manager's right click context menu

## How it works

- Any file you place in `~/Templates` becomes a template option.
- When you right-click in a folder and select **New Document**, your templates will show up in the submenu.
- Selecting a template creates a copy of it in the current folder types, like boilerplate documents, scripts, or code snippets.

> [!INFO]
> You can also check/edit the configuration in `~/.config/user-dirs.dirs` to point to

- run `xdg-user-dirs-update` to apply changes
```text
XDG_TEMPLATES_DIR="$HOME/Templates"
```

- Open file manager
- Navigate to any folder
- Right-click in empty space -> **New Document**
- Select the template from the list
- A copy will be created in the current folder.