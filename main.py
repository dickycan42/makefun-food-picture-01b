"""Molten Cheddar Smash Burger -- make.fun food-picture-01 entry.

Copies the entry picture (entry.png, sitting beside this program) into
the grader's output directory and verifies the copy byte for byte.

The picture shows a smash burger being lifted apart, molten cheddar
stretching in long glossy strands between the charred patty and the
toasted brioche bun, against a dark background in warm light.

Standard library only. Deterministic: no network, no timestamps,
no randomness, no image processing -- the file is copied as-is.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 fingerprint of the file at ``path``."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def looks_like_picture(header: bytes) -> bool:
    """True when the leading bytes name a PNG or a JPEG image."""
    return header.startswith(PNG_MAGIC) or header.startswith(JPEG_MAGIC)


def picture_size(data: bytes) -> tuple[int, int]:
    """Return the (width, height) of a PNG or JPEG from its first bytes.

    PNG: width and height sit at the start of the IHDR chunk.
    JPEG: scan the markers for a start-of-frame segment, which carries
    the height then the width as big-endian 16-bit values.
    """
    if data.startswith(PNG_MAGIC):
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            raise ValueError("bad JPEG marker")
        marker = data[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        if marker == 0xD8 or marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        pos += 2 + length
    raise ValueError("no JPEG start-of-frame segment found")


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / PICTURE_NAME

    if not source.is_file():
        print(f"error: {PICTURE_NAME} is missing beside main.py", file=sys.stderr)
        return 1

    source_size = source.stat().st_size
    if source_size == 0 or source_size >= MAX_BYTES:
        print(
            f"error: {PICTURE_NAME} is {source_size} bytes; "
            f"must be non-empty and smaller than {MAX_BYTES} bytes",
            file=sys.stderr,
        )
        return 1

    with source.open("rb") as handle:
        header = handle.read(4096)
    if not looks_like_picture(header):
        print(
            f"error: {PICTURE_NAME} is neither a PNG nor a JPEG "
            f"(leading bytes {header[:8]!r})",
            file=sys.stderr,
        )
        return 1

    try:
        width, height = picture_size(header)
    except (ValueError, struct.error) as exc:
        print(f"error: cannot read {PICTURE_NAME} dimensions: {exc}", file=sys.stderr)
        return 1
    if width > MAX_SIDE or height > MAX_SIDE:
        print(
            f"error: {PICTURE_NAME} is {width}x{height}; "
            f"each side must be at most {MAX_SIDE} pixels",
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
