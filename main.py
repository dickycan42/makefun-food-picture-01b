"""Steaming Ramen, Chopsticks High -- make.fun food-picture-01 entry.

Copies the entry picture (entry.png, sitting beside this program) into
the grader's output directory and verifies the copy byte for byte.

Standard library only. Deterministic: no network, no timestamps,
no randomness.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 fingerprint of the file at ``path``."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / PICTURE_NAME

    source_size = source.stat().st_size
    if source_size == 0 or source_size >= 1024 * 1024:
        print(
            f"error: source picture failed the size check "
            f"({PICTURE_NAME} is {source_size} bytes; "
            f"must be non-empty and smaller than 1 megabyte)",
            file=sys.stderr,
        )
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / PICTURE_NAME

    shutil.copyfile(source, destination)

    source_hash = sha256_of(source)
    copy_hash = sha256_of(destination)
    if source_hash != copy_hash:
        print(
            f"error: copied picture differs from source "
            f"(source {source_hash}, copy {copy_hash})",
            file=sys.stderr,
        )
        return 1

    print(
        f"wrote {destination} ({destination.stat().st_size} bytes, "
        f"sha256 {copy_hash})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
