## PS1
```bash
PS1='\[\e[38;5;109m\]\u\[\e[38;5;250m\]@\[\e[38;5;110m\]\h \[\e[38;5;144m\]\w\[\e[0m\]\n\$ '
```

```bash
 PS1='\[\e[38;5;141m\]\W\[\e[38;5;175m\]$(__git_ps1 " (%s)")\[\e[0m\]\[\e[38;5;108m\] ➜ \[\e[0m\]'
```

```bash
PS1='\[\e[38;5;110m\]➜ \[\e[38;5;144m\]\W\[\e[38;5;109m\]$(__git_ps1 " (%s)")\[\e[0m\] '
```
## Habamax dark
```bash
#!/bin/bash

# Get the current profile ID (first in list)
PROFILE_ID=$(gsettings get org.gnome.Terminal.ProfilesList list | grep -o "'[^']*'" | tr -d "'" | head -n 1)

# Base path for gsettings
BASE_PATH="org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/"

# Disable theme colors/background
gsettings set "$BASE_PATH" use-theme-colors false
gsettings set "$BASE_PATH" use-theme-background false

# Set Habamax theme colors
gsettings set "$BASE_PATH" background-color '#1c1c1c'     # Background
gsettings set "$BASE_PATH" foreground-color '#d0d0d0'     # Foreground
gsettings set "$BASE_PATH" bold-color '#ffffaf'           # Bold color (Yellowish)
gsettings set "$BASE_PATH" bold-color-same-as-fg false

# Set Habamax 16-color palette
gsettings set "$BASE_PATH" palette "[
  '#1c1c1c',  # black
  '#af5f5f',  # red
  '#5f875f',  # green
  '#87875f',  # yellow
  '#5f87af',  # blue
  '#875f87',  # magenta
  '#5f8787',  # cyan
  '#d0d0d0',  # white

  '#585858',  # bright black
  '#ff8700',  # bright red (orange-like)
  '#87af87',  # bright green
  '#ffffaf',  # bright yellow
  '#87afd7',  # bright blue
  '#d787af',  # bright magenta
  '#87d7d7',  # bright cyan
  '#ffffff'   # bright white
]"

```

### Use rose pine moon theme
```bash
# Get the current profile ID
PROFILE_ID=$(gsettings get org.gnome.Terminal.ProfilesList list | grep -o "'[^']*'" | tr -d "'")

# Set theme colors
BASE_PATH="org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/"

gsettings set "$BASE_PATH" use-theme-colors false
gsettings set "$BASE_PATH" use-theme-background false

# Background, foreground, bold
gsettings set "$BASE_PATH" background-color '#232136'     # base
gsettings set "$BASE_PATH" foreground-color '#e0def4'     # text
gsettings set "$BASE_PATH" bold-color '#c4a7e7'           # love
gsettings set "$BASE_PATH" bold-color-same-as-fg false

# Rosé Pine Moon palette (16 colors)
gsettings set "$BASE_PATH" palette "[
  '#393552',  # black     (surface)
  '#eb6f92',  # red       (love)
  '#9ccfd8',  # green     (foam)
  '#f6c177',  # yellow    (gold)
  '#3e8fb0',  # blue      (pine)
  '#c4a7e7',  # magenta   (iris)
  '#ea9a97',  # cyan      (rose)
  '#e0def4',  # white     (text)

  '#6e6a86',  # bright black  (highlight low)
  '#eb6f92',  # bright red    (love)
  '#9ccfd8',  # bright green  (foam)
  '#f6c177',  # bright yellow (gold)
  '#3e8fb0',  # bright blue   (pine)
  '#c4a7e7',  # bright magenta(iris)
  '#ea9a97',  # bright cyan   (rose)
  '#e0def4'   # bright white  (text)
]"

```

### Use rose pine moon theme (light)
```bash

# Get the current profile ID (first in the list)
PROFILE_ID=$(gsettings get org.gnome.Terminal.ProfilesList list | grep -o "'[^']*'" | tr -d "'" | head -n 1)

# Set base path
BASE_PATH="org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/"

# Disable default theme colors
gsettings set "$BASE_PATH" use-theme-colors false
gsettings set "$BASE_PATH" use-theme-background false

# Set background, foreground, bold colors
gsettings set "$BASE_PATH" background-color '#ffffff'     # pure white background
gsettings set "$BASE_PATH" foreground-color '#000000'     # black text
gsettings set "$BASE_PATH" bold-color '#ae7cf7'           # purple (bold accent)
gsettings set "$BASE_PATH" bold-color-same-as-fg false

# Set palette (converted rgb to hex)
gsettings set "$BASE_PATH" palette "[
  '#000000',  # rgb(0,0,0)
  '#ff5555',  # rgb(255,85,85)
  '#5070fa',  # rgb(80,112,250)
  '#f1fa8c',  # rgb(241,250,140)
  '#ae7cf7',  # rgb(174,124,247)
  '#ff79c6',  # rgb(255,121,198)
  '#81d3e5',  # rgb(129,211,229)
  '#bfbfbf',  # rgb(191,191,191)

  '#4d4d4d',  # rgb(77,77,77)
  '#ff6e67',  # rgb(255,110,103)
  '#5a8ff7',  # rgb(90,143,247)
  '#f4f99d',  # rgb(244,249,157)
  '#9e76da',  # rgb(158,118,218)
  '#ff92d0',  # rgb(255,146,208)
  '#96cfdb',  # rgb(150,207,219)
  '#e6e6e6'   # rgb(230,230,230)
]"
```


## Catppuccin Mocha palette

```bash
#!/bin/bash

# Catppuccin Mocha palette
declare -A colors=(
  [black]="#1e1e2e"
  [red]="#f38ba8"
  [green]="#a6e3a1"
  [yellow]="#f9e2af"
  [blue]="#89b4fa"
  [magenta]="#f5c2e7"
  [cyan]="#94e2d5"
  [white]="#cdd6f4"
  [brightBlack]="#585b70"
  [brightRed]="#f38ba8"
  [brightGreen]="#a6e3a1"
  [brightYellow]="#f9e2af"
  [brightBlue]="#89b4fa"
  [brightMagenta]="#f5c2e7"
  [brightCyan]="#94e2d5"
  [brightWhite]="#ffffff"
  [bg]="#1e1e2e"
  [fg]="#cdd6f4"
  [cursor]="#f5c2e7"
)

# Create a new GNOME terminal profile with Catppuccin colors
PROFILE_NAME="Catppuccin Mocha"
PROFILE_SLUG="catppuccin-mocha"
DCONF_DIR=/org/gnome/terminal/legacy/profiles:
PROFILE_ID=$(uuidgen)

# Append profile
dconf write $DCONF_DIR/list "[$(dconf read $DCONF_DIR/list | sed "s/]$/, '$PROFILE_ID']/")]"
dconf write $DCONF_DIR/:$PROFILE_ID/visible-name "'$PROFILE_NAME'"
dconf write $DCONF_DIR/:$PROFILE_ID/palette "['${colors[black]}', '${colors[red]}', '${colors[green]}', '${colors[yellow]}', '${colors[blue]}', '${colors[magenta]}', '${colors[cyan]}', '${colors[white]}', '${colors[brightBlack]}', '${colors[brightRed]}', '${colors[brightGreen]}', '${colors[brightYellow]}', '${colors[brightBlue]}', '${colors[brightMagenta]}', '${colors[brightCyan]}', '${colors[brightWhite]}']"
dconf write $DCONF_DIR/:$PROFILE_ID/background-color "'${colors[bg]}'"
dconf write $DCONF_DIR/:$PROFILE_ID/foreground-color "'${colors[fg]}'"
dconf write $DCONF_DIR/:$PROFILE_ID/bold-color "'${colors[fg]}'"
dconf write $DCONF_DIR/:$PROFILE_ID/use-theme-colors "false"
dconf write $DCONF_DIR/:$PROFILE_ID/use-theme-background "false"
dconf write $DCONF_DIR/:$PROFILE_ID/cursor-colors-set "true"
dconf write $DCONF_DIR/:$PROFILE_ID/cursor-background-color "'${colors[cursor]}'"
dconf write $DCONF_DIR/:$PROFILE_ID/cursor-foreground-color "'${colors[bg]}'"

# Optional: Set as default profile
dconf write $DCONF_DIR/default "'$PROFILE_ID'"

echo "🎨 Catppuccin Mocha theme applied to GNOME Terminal."

```