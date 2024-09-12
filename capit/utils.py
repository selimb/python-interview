from pathlib import Path
import shutil


def rm_rf(p: Path) -> None:
    """
    Like `rm -rf`.
    """
    if not p.exists():
        return

    if p.is_file():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)
