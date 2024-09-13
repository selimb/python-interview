# Interview Prep

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

## Test

The command below assumes you've activated the virtual environment:

```shell
$ python test.py
```

which should output something like:

```
ocean.mkv
400.0
(360, 640, 3)
ocean.mp4
400.0
(360, 640, 3)
```
