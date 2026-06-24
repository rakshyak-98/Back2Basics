# Python Package Setup

This guide explains how to turn the `python/` folder into an installable package for use in other projects.
The sample code under `python/src/` is currently a flat set of scripts. To reuse it as a library, follow the steps below.

---

## Target Layout

```

python/

├── pyproject.toml
├── README.md
├── package-setup-readme.md
├── examples/
│ └── app_sample.py
└── src/
└── doverunner_cpix/
├── __init__.py
├── cpix_client.py
├── content_packaging_data.py
├── drm_type.py
├── encryption_scheme.py
├── exceptions.py
└── track_type.py

```

Keep `app_sample.py` outside the package (e.g. in `examples/`) so sample code is not installed as library code.

---

## Step 1: Create `pyproject.toml`

Create `python/pyproject.toml` with the following content:

```toml

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "doverunner-cpix"
version = "0.1.0"
description = "DoveRunner CPIX API client for Python"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
	"requests",
]

[tool.setuptools.packages.find]
where = ["src"]

```

The PyPI/distribution name is `doverunner-cpix`; the Python import path is `doverunner_cpix`.

---

## Step 2: Create the Package Directory

```bash

mkdir -p python/src/doverunner_cpix

```

Move these files from `python/src/` into `python/src/doverunner_cpix/`:
- `cpix_client.py`
- `content_packaging_data.py`
- `drm_type.py`
- `encryption_scheme.py`
- `exceptions.py`
- `track_type.py`

Do **not** move `app_sample.py`, `*.json`, or other sample/output files.

---

## Step 3: Add `__init__.py`

Create `python/src/doverunner_cpix/__init__.py`:
```python

from .cpix_client import CpixClient
from .drm_type import DrmType
from .encryption_scheme import EncryptionScheme
from .track_type import TrackType
from .exceptions import CpixClientError
from .content_packaging_data import ContentPackagingInfo, MultiDrmInfo

__all__ = [
	"CpixClient",
	"DrmType",
	"EncryptionScheme",
	"TrackType",
	"CpixClientError",
	"ContentPackagingInfo",
	"MultiDrmInfo",
]

```

---

## Step 4: Fix Imports in `cpix_client.py`

Change the local imports at the top of `cpix_client.py` from:

```python

from drm_type import DrmType
from encryption_scheme import EncryptionScheme
from track_type import TrackType
from content_packaging_data import ContentPackagingInfo, MultiDrmInfo
from exceptions import CpixClientError

```

To:

```python

from .drm_type import DrmType
from .encryption_scheme import EncryptionScheme
from .track_type import TrackType
from .content_packaging_data import ContentPackagingInfo, MultiDrmInfo
from .exceptions import CpixClientError

```

No import changes are needed in `drm_type.py`, `encryption_scheme.py`, `track_type.py`, `content_packaging_data.py`, or `exceptions.py`.

---

## Step 5: Update the Sample Script

Move `app_sample.py` to `python/examples/app_sample.py` and update its imports:

```python

from doverunner_cpix import CpixClient, DrmType, EncryptionScheme, TrackType, CpixClientError

```

Run the sample **after** installing the package:

```bash

python python/examples/app_sample.py

```

---

## Step 6: Install Locally

From the `python/` directory:
```bash

cd python

# optional but recommended
python -m venv .venv
source .venv/bin/activate
pip install -e .

```

The `-e` flag installs in editable mode: changes under `src/doverunner_cpix/` are picked up without reinstalling.

Verify the install:
```bash

python -c "from doverunner_cpix import CpixClient; print(CpixClient)"

```

---

## Step 7: Use in Other Projects
### From a local path (same machine)

```bash

pip install -e /path/to/cpix-api-client/python

```

### From git (after pushing the packaging changes)

```bash

pip install "git+https://github.com/<org>/cpix-api-client.git#subdirectory=python"

```

### In your project code

```python

from doverunner_cpix import (
	CpixClient,
	DrmType,
	EncryptionScheme,
	TrackType,
	CpixClientError,
)
client = CpixClient("https://drm-kms.doverunner.com/v2/cpix/pallycon/getKey/{enc-token}")
pack_info = client.get_content_key_info_from_doverunner_kms(
	content_id="my-content",
	drm_type=DrmType.WIDEVINE | DrmType.PLAYREADY | DrmType.FAIRPLAY,
	encryption_scheme=EncryptionScheme.CENC,
	track_type=TrackType.ALL_TRACKS,
	period_index=0,
)

```

---

## Checklist

| Task                                                 | Done? |
| ---------------------------------------------------- | ----- |
| Create `pyproject.toml`                              |       |
| Create `src/doverunner_cpix/`                        |       |
| Move 6 library `.py` files                           |       |
| Add `__init__.py`                                    |       |
| Change imports in `cpix_client.py` to relative (`.`) |       |
| Update `app_sample.py` imports                       |       |
| `pip install -e .`                                   |       |
| Test import in another project                       |       |

---

## Requirements

- **Python 3.9+**
- **`requests`** (declared as a dependency in `pyproject.toml`)

---

## Notes
- Bump `version` in `pyproject.toml` for each release if you publish to PyPI.
- Consider adding `python/.venv/` and generated `*.json` output files to `.gitignore`.
- For a quick run without packaging, see the main [README.md](./README.md).