# Commands for local development

## Prerequisites

- [Python](https://www.python.org/) 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## uv Commands

### Initialize the virtual environment

On Windows:

```cmd
.\scripts\init-venv.bat
```

On macOS/Linux:

```bash
./scripts/init-venv.sh
```

Then, you can configure the virtual environment in Cursor (VS Code) to run the code directly in the IDE.

### Enter the virtual environment

On Windows:

```cmd
.\src\.venv\Scripts\activate
```

On macOS/Linux:

```bash
source src/.venv/bin/activate
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

<br />
<br />

## pytest Commands

### Run all tests without entering the virtual environment

On Windows:

```cmd
.\scripts\pytest.bat
```

On macOS/Linux:

```bash
./scripts/pytest.sh
```

### Run the test (after entering the virtual environment)

Assume that you are in the `src` directory.

To run all tests:

```bash
pytest
```

To run a specific test, for example:

```bash
pytest tests/test_arona_ai.py::test_arona_ai_party_data -v
```

If you need to view more detailed logs, you can use the following command:

```bash
pytest -s tests/test_arona_ai.py::test_arona_ai_party_data -vv
```
