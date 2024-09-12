import dataclasses
import logging
from pathlib import Path
import threading
from typing import NamedTuple

import cv2
import numpy as np

from .utils import rm_rf

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Workdir:
    in_dir: Path
    out_dir: Path


def setup_workdir(workdir: Path, *, clean: bool = False) -> Workdir:
    workdir.mkdir(parents=True, exist_ok=True)
    in_dir = workdir / "in"
    out_dir = workdir / "out"
    if clean:
        rm_rf(in_dir)
        rm_rf(out_dir)
    in_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    return Workdir(in_dir=in_dir, out_dir=out_dir)


class ReportItem(NamedTuple):
    filename: str
    frame_count: int
    width: int
    height: int


class Report:
    def __init__(self) -> None:
        self._items: list[ReportItem] = []

    def add(self, item: ReportItem) -> None:
        self._items.append(item)

    @property
    def count(self) -> int:
        return len(self._items)

    def get(self) -> list[ReportItem]:
        return self._items.copy()


class App:
    def __init__(
        self, wrk: Workdir, *, stop_evt: threading.Event, report: Report
    ) -> None:
        self.wrk = wrk
        self.stop_evt = stop_evt
        self.report = report

        # CHALLENGE-1: What do you think of using a list here?
        self._processed: list[Path] = []
        # CHALLENGE-2: What about here?
        self._to_process: list[Path] = []

    def run(self) -> None:
        watcher = threading.Thread(target=self._run_watcher, name="watcher")
        watcher.start()
        processor = threading.Thread(target=self._run_processor, name="processor")
        processor.start()

        self.stop_evt.wait()

        # Cleanup
        watcher.join()
        processor.join()

    def _run_watcher(self) -> None:
        in_dir = self.wrk.in_dir
        # CHALLENGE-3: How would you reduce the delay between adding new files and
        #   processing them? In other words, how could this be more "real-time"?
        while not self.stop_evt.is_set():
            logger.debug("Scanning...")
            for p in sorted(in_dir.iterdir()):
                if p in self._processed:
                    break
                else:
                    self._to_process.append(p)
                    self._processed.append(p)
            self.stop_evt.wait(2)

    def _run_processor(self) -> None:
        while not self.stop_evt.is_set():
            if len(self._to_process) > 0:
                p = self._to_process.pop(0)
                # CHALLENGE-5: How would you parallelize this?
                self._do_process(p)
            self.stop_evt.wait(2)

    def _do_process(self, p: Path) -> None:
        cap = cv2.VideoCapture(str(p))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.report.add(
            ReportItem(
                filename=p.name, frame_count=frame_count, width=width, height=height
            )
        )
        logger.info(f"Processing {p.name}: {frame_count=} {height=} {width=}")

        images: list[np.ndarray] = []
        for _i in range(frame_count):
            _, img = cap.read()
            images.append(img)

        images_arr = np.array(images)
        image_avg = np.average(images_arr, axis=0)
        out_path = self.wrk.out_dir / "average.jpeg"
        cv2.imwrite(str(out_path), image_avg)


def run_forever(wrk: Workdir) -> None:
    report = Report()
    stop_evt = threading.Event()
    app = App(wrk, stop_evt=stop_evt, report=report)
    try:
        app.run()
    except KeyboardInterrupt:
        stop_evt.set()
