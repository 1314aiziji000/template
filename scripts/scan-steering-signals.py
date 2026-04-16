#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main():
    script_path = (
        Path(__file__).resolve().parent.parent
        / ".agents"
        / "skills"
        / "steering-runner"
        / "scripts"
        / "run-steering-scan.py"
    )
    sys.argv[0] = str(script_path)
    runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()
