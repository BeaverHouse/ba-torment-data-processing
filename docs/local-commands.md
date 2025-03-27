# Commands for local development

## Prerequisites

- [Python](https://www.python.org/) 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## uv Commands

### Create a virtual environment

```bash
cd src && uv sync
```

### Enter the virtual environment

Assume that you are in the `src` directory.

On Windows:

```cmd
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### Add the package (after entering the virtual environment)

```bash
uv add <package_name>
```

### Remove the package (after entering the virtual environment)

```bash
uv remove <package_name>
```

If you need other commands, please refer to the [uv documentation](https://docs.astral.sh/uv/getting-started/features/).

## pytest Commands

### Run the test (after entering the virtual environment)

To run all tests:

```bash
python -m pytest tests/
```

To run a specific test, for example:

```bash
python -m pytest tests/test_arona_ai.py::test_arona_ai -v
```

If you need to view more detailed logs, you can use the following command:

```bash
python -m pytest -s tests/test_arona_ai.py::test_arona_ai -vv
```
