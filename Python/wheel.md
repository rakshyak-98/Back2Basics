- process of creating a wheel distribution package for a python project.
- is a binary package format (`.whl` extension).
### How to build a wheel
- require `setup.py` file with metadata and instructions for building the package.
```bash
pip install setuptools wheel;
# navigate to the working directory
python setup.py bdist_wheel
```