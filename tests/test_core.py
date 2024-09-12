import contextlib
from pathlib import Path
import shutil
import threading
import time
from typing import Iterator

import pytest  # noqa: F401

from capit import core

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
VIDEO_BAD = DATA_DIR / "bad.mp4"
VIDEO_EARTH = DATA_DIR / "earth.mp4"
VIDEO_OCEAN = DATA_DIR / "ocean.mp4"
# ATTENTION: This file is not tracked in Git.
VIDEO_PECULIAR = DATA_DIR / "peculiar.mkv"


class AppRunner:
    def __init__(self, tmp_path: Path) -> None:
        self.wrk = core.setup_workdir(tmp_path)
        self.stop_evt = threading.Event()
        self.report = core.Report()
        self.app = core.App(wrk=self.wrk, stop_evt=self.stop_evt, report=self.report)

    def add_input(self, p: Path) -> None:
        shutil.copy(p, self.wrk.in_dir / p.name)

    @contextlib.contextmanager
    def run_background(self) -> Iterator[None]:
        t = threading.Thread(target=self.app.run, name="app.run")
        t.start()

        try:
            yield
        finally:
            self.stop_evt.set()
            t.join()

    def wait_reports(self, n: int) -> list[core.ReportItem]:
        timeout = 5
        start = time.time()
        while True:
            if self.report.count >= n:
                return self.report.get()

            elapsed = time.time() - start
            if elapsed > timeout:
                raise AssertionError(f"Expected at least {n} report items.")

            # CHALLENGE-4: Can we get rid of time.sleep here?
            time.sleep(0.1)


# @pytest.mark.only
def test_processes_existing_file(tmp_path: Path) -> None:
    """
    Tests that a file that already exists in the input directory is processed.
    """
    runner = AppRunner(tmp_path)
    runner.add_input(VIDEO_EARTH)
    with runner.run_background():
        reports = runner.wait_reports(1)

    assert reports == [
        core.ReportItem(
            filename=VIDEO_EARTH.name, frame_count=901, width=480, height=270
        )
    ]


def test_outputs_image_using_input_filename(tmp_path: Path) -> None:
    """
    Tests that the output file has the same base name as the input file.
    """
    runner = AppRunner(tmp_path)
    runner.add_input(VIDEO_EARTH)
    with runner.run_background():
        _ = runner.wait_reports(1)

    filenames = [p.name for p in runner.wrk.out_dir.iterdir()]
    assert filenames == ["earth.jpeg"]


def test_watches_for_new_files(tmp_path: Path) -> None:
    """
    Tests that the app continuously watches for new files.
    """
    runner = AppRunner(tmp_path)
    runner.add_input(VIDEO_EARTH)
    with runner.run_background():
        # Give enough time for all background threads to start
        time.sleep(1)

        runner.add_input(VIDEO_OCEAN)
        reports = runner.wait_reports(2)

    assert [item.filename for item in reports] == [VIDEO_EARTH.name, VIDEO_OCEAN.name]


def test_ignores_invalid_videos(tmp_path: Path) -> None:
    """
    Tests that invalid videos are ignored.
    """
    runner = AppRunner(tmp_path)
    runner.add_input(VIDEO_BAD)
    with runner.run_background():
        # Give enough time for all background threads to start
        time.sleep(1)

        runner.add_input(VIDEO_EARTH)
        reports = runner.wait_reports(1)

    assert [item.filename for item in reports] == [VIDEO_EARTH.name]
    out_files = list(runner.wrk.out_dir.iterdir())
    assert len(out_files) == 1


def test_peculiar_video(tmp_path: Path) -> None:
    """
    Surprise!
    """
    runner = AppRunner(tmp_path)
    runner.add_input(VIDEO_PECULIAR)
    with runner.run_background():
        reports = runner.wait_reports(1)

    assert reports == [
        core.ReportItem(
            filename=VIDEO_PECULIAR.name, frame_count=20, width=1280, height=720
        )
    ]
