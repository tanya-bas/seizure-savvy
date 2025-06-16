# Quick overview of the test suite

The following tests are contained in their corresponding folders.

- `test_schema.py` - Tests for schema validation: correct attribute names, data types, constraints, relationships (including many-to-many and cascade delete, e.g. deleting a user should delete all their logs).
- `test_auth.py` - Tests for authentication endpoints
- `test_user.py` - Tests for user endpoints
- `test_medication.py` - Tests for logging endpoints
- `test_log.py` - Tests for logging endpoints
- `test_model.py` - Tests for model endpoints

# Run tests

Quick command to run all tests

```bash
cd api
pytest -W ignore::DeprecationWarning
```

The tags `-W ignore::DeprecationWarning` are used to ignore the deprecation warnings **only** for the tests. Not recommended to use in production code.

## Run tests with verbose output

```bash
cd api
pytest -v
```

## Run tests with coverage

```bash
cd api
pytest --cov=. --cov-config=.coveragerc -W ignore::DeprecationWarning
```

# Write tests

## When to write tests

Whenever there are new features added or existing features are modified inside the API, write tests for them.

- Schema
- Endpoints (auth, user, medication, log)
- Models

## How to write tests

### Basic guide

Reference: [pytest documentation](https://docs.pytest.org/en/stable/)

- Tests are written using `pytest` inside this `tests` directory
- Create a new folder/directory for each module test. Each folder should contain
  - `__init__.py` file (required) so that pytest can discover the tests
  - `conftest.py` file, if needed, to write fixtures, which can be used across multiple test files inside the directory + any lower-level directories. See [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) for more information.
  - `test_*.py` file
- The functions inside the `test_*.py` file should start with `test_` prefix
- Each test should be independent of other tests

### Build on existing tests

1. See the highest-level `conftest.py` for fixtures that can be used across all tests
2. Look at the existing tests to understand how they are written. The `user` tests are a good starting point, since it links to other modules.

# Future improvements

- [x] Add Github Actions to run tests on every push
