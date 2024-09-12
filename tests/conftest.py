from pathlib import Path

import pytest


@pytest.fixture
def tmp_path(tmp_path: Path) -> Path:
    """
    Like the built-in `tmp_path`, but always prints the directory for easier debugging.
    """
    print("tmp_path", tmp_path)
    return tmp_path
