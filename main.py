"""Copy the finished news image to make.fun's requested output directory."""
import os
from pathlib import Path
import shutil


def main():
    # Resolve the source beside this script, even when the grader changes cwd.
    source = Path(__file__).resolve().parent / "entry.png"
    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination_dir / "entry.png")


if __name__ == "__main__":
    main()
