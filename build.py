from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Sequence


def run(command: Sequence[str]) -> None:
    executable = shutil.which(command[0])

    if executable is None:
        raise SystemExit(f"Required executable not found: {command[0]}")

    subprocess.run([executable, *command[1:]], check=True)


def main() -> None:
    run(["npm", "run", "test"])
    run([sys.executable, "-m", "pytest"])


if __name__ == "__main__":
    main()
