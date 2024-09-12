import logging
from pathlib import Path

import click

from . import core

logger = logging.getLogger(__name__)
_WORKDIR_DEFAULT = Path.cwd() / "wrk"


@click.command()
@click.option(
    "workdir",
    "-w",
    "--workdir",
    type=click.Path(path_type=Path),
    default=_WORKDIR_DEFAULT,
)
@click.option("--clean", is_flag=True, default=False)
def cli(workdir: Path, clean: bool) -> None:
    logging.basicConfig(level="DEBUG")

    logger.info(f"workdir={workdir.relative_to(Path.cwd())}")
    wrk = core.setup_workdir(workdir, clean=clean)

    core.run_forever(wrk)
