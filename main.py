#!/usr/bin/env python3
"""news-image-01 entry: write the picture of Friday 13 November 2026's world news.

The image ships in this repository as entry.png (the bytes are a JPEG; the
competition keeps the name entry.png either way). This program checks the file
against the competition limits and copies it, byte for byte, to the output
directory: /output by default, or $MAKEFUN_OUTPUT_DIR when that is set.

Standard library only, no network, no clock, no randomness: every run writes
the same bytes.
"""

import os
import struct
import sys

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
MAX_BYTES = 1_048_576  # 1 MiB
MAX_SIDE = 1024  # pixels, each way

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


class EntryError(Exception):
    """The shipped image breaks one of the competition limits."""


def detect_format(data: bytes) -> str:
    """Tell PNG from JPEG by the first bytes, as the gate does."""
    if data.startswith(PNG_MAGIC):
        return "png"
    if data.startswith(JPEG_MAGIC):
        return "jpeg"
    raise EntryError("entry.png is neither a PNG nor a JPEG")


def png_size(data: bytes) -> tuple[int, int]:
    """Width and height from the IHDR chunk, which must come first."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise EntryError("PNG has no IHDR chunk at its start")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


# Start-of-frame markers carry the picture size. 0xC4 (Huffman tables),
# 0xC8 (reserved) and 0xCC (arithmetic conditioning) share the range but are not frames.
JPEG_FRAME_MARKERS = frozenset(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}
# Markers that stand alone, with no length field after them.
JPEG_BARE_MARKERS = frozenset(range(0xD0, 0xD8)) | {0x01}


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Width and height from the first start-of-frame segment."""
    position = 2  # past the SOI marker
    end = len(data)
    while position + 4 <= end:
        if data[position] != 0xFF:
            raise EntryError(f"JPEG segment at byte {position} does not start with 0xFF")
        marker = data[position + 1]
        if marker == 0xFF:  # fill byte before a marker
            position += 1
            continue
        if marker in JPEG_BARE_MARKERS:
            position += 2
            continue
        (length,) = struct.unpack(">H", data[position + 2:position + 4])
        if length < 2:
            raise EntryError(f"JPEG segment at byte {position} has a bad length")
        if marker in JPEG_FRAME_MARKERS:
            if position + 9 > end:
                break
            height, width = struct.unpack(">HH", data[position + 5:position + 9])
            return width, height
        if marker == 0xDA:  # start of scan: no frame header came before it
            break
        position += 2 + length
    raise EntryError("JPEG has no start-of-frame segment")


def validate(data: bytes) -> tuple[str, int, int]:
    """Return (format, width, height), or raise EntryError."""
    if not data:
        raise EntryError("entry.png is empty")
    if len(data) > MAX_BYTES:
        raise EntryError(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit")
    kind = detect_format(data)
    width, height = png_size(data) if kind == "png" else jpeg_size(data)
    if width < 1 or height < 1:
        raise EntryError(f"image size {width}x{height} is not a picture")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise EntryError(f"image is {width}x{height}, over {MAX_SIDE}x{MAX_SIDE}")
    return kind, width, height


def output_dir() -> str:
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    with open(source, "rb") as handle:
        data = handle.read()

    try:
        kind, width, height = validate(data)
    except EntryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    with open(target, "wb") as handle:
        handle.write(data)

    # Read the file back: the run only counts if the bytes on disk are the ones shipped.
    with open(target, "rb") as handle:
        if handle.read() != data:
            print(f"error: {target} differs from the shipped image", file=sys.stderr)
            return 1

    print(f"wrote {target}: {kind}, {width}x{height}, {len(data)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
