# Squash the Bugs

## Pre-requisites

- Python 3.11 (3.11.9 is fine)

## Setup

Make sure you use the right `python` executable depending on your OS and setup.

```shell
$ python --version
Python 3.11.9
```

Next, setup a virtual environment and install the dependencies.
Feel free to diverge if you're used to a certain flow.

```shell
$ python -m venv venv
# Linux
$ venv/bin/pip install -r requirements.txt
# Windows
$ venv\Scripts\pip install -r requirements.txt
```

## Run the Application

Start by populating the work directory:

```shell
$ mkdir -p wrk/in
$ cp data/earth.mp4 wrk/in/
```

Now run the application.
The command below assumes you've activated the virtual environment:

```shell
$ python -m capit
```

## Lint

This project uses `ruff` and `mypy`.

```shell
$ ruff check
$ mypy .
```

If you're not familiar with those tools, it doesn't matter.

## Run the Tests

```shell
$ pytest
```

You should see 4 failed and 1 passed.

### Selecting Tests

If you've ran `pytest` tests from your IDE in the past, then feel free to do so.
If not, or if you just prefer the CLI, you can target specific tests using fully-qualified test IDs:

```shell
$ pytest tests/test_core.py::test_processes_existing_file
```

or using "keyword expressions"

```shell
$ pytest -k "existing"
```

Alternatively, you can add the `@pytest.mark.only` decorator on a test.

## Your Mission

### 1. Fix the Tests

Make all the tests pass.
Tackle them in the order that they are defined.

### 2. Discuss the Challenges

Grep for `CHALLENGE-` comments in the code and discuss, or even implement!
