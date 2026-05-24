### Source list file config

```txt
deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/debian jammy nginx
```

```text
`deb [arch=amd64 signed-by=/usr/share/keyrings/example.gpg] [https://repo.example.com/debian](https://repo.example.com/debian) stable main`
```

- `deb` 
	- this is a binary package source (as opposed to `deb-src` for source code).
	- Compiled binaries (`.deb` flies).
	- Points to pre-compiled binary packages.
- `deb-src` 
	- Original source code, patches, and build instructions.
	- Inspecting code modifying software, or compiling from scratch.
	- Points to the original source code and debianisation files.

### Options (Optional, in [] brackets)
these define specific constraints for the repository.
- `arch=` -> Restricts the repository to specific architectures (e.g., `amd64`, `arm64`).
- `[signed-by=...]` -> path to the gpg key used to verify the packages. This is the modern, secure way to handle keys instead of using `apt-key`.
- `http://` -> URL of the APT repository (from package org).
- `jammy` -> code name for Ubuntu 22.04 (APT uses Debian-style naming).
- `nginx` -> the distribution/component (like `main`, `contrib`)  here it is nginx specific package.

| Part        | Meaning                                                    | Example                                   |
| ----------- | ---------------------------------------------------------- | ----------------------------------------- |
| `deb`       | Binary packages (most common). `deb-src` = source packages | `deb`                                     |
| `[options]` | Extra settings (arch, signed-by, trusted=yes, etc.)        | `[arch=amd64 signed-by=...]`              |
| `URL`       | The repository base URL                                    | `https://dl.google.com/linux/chrome/deb/` |
| `suite`     | Release/codename (stable, noble, bookworm, etc.)           | `stable` or `noble`                       |
| `component` | Section (main, universe, multiverse, non-free, etc.)       | `main`                                    |

> [!INFO]
> `main` component -> sub folder under distribution `/dists/jammy/main/binary-amd64/`
> when you run `apt update` APT tries to download
```bash
https://my.repo.com/apt/dists/jammy/Release
https://my.repo.com/apt/dists/jammy/main/binary-amd64/Packages.gz
```
- `jammy` to select the `dists/<distribution>` folder
- `main` (component) to pick which subfolder(s) to load packages from

> [!NOTE]
> APT does not "determine" these — **you must specify both**, and the server must have a matching structure under `/dists`. 

