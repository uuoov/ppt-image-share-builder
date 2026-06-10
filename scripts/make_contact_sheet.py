#!/usr/bin/env python3
"""Create a labeled contact sheet from generated PPT page images."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def slide_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"slide[-_ ]?(\d+)", path.stem, re.IGNORECASE)
    if match:
        return (int(match.group(1)), path.name)
    return (10_000, path.name)


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def build_contact_sheet(
    image_dir: Path,
    output: Path,
    pattern: str,
    cols: int,
    thumb_width: int,
    label_height: int,
) -> None:
    if cols <= 0:
        raise SystemExit("--cols must be greater than 0")
    if thumb_width <= 0:
        raise SystemExit("--thumb-width must be greater than 0")
    if label_height < 0:
        raise SystemExit("--label-height must be 0 or greater")

    files = sorted(image_dir.glob(pattern), key=slide_sort_key)
    if not files:
        raise SystemExit(f"No images matched {pattern!r} in {image_dir}")

    with Image.open(files[0]) as first:
        aspect = first.height / first.width
    thumb_height = int(thumb_width * aspect)
    rows = math.ceil(len(files) / cols)

    sheet = Image.new("RGB", (cols * thumb_width, rows * (thumb_height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    font = load_font(18)

    for idx, file in enumerate(files):
        with Image.open(file) as source:
            img = source.convert("RGB")
        img.thumbnail((thumb_width, thumb_height), Image.LANCZOS)

        x0 = (idx % cols) * thumb_width
        y0 = (idx // cols) * (thumb_height + label_height)
        x = x0 + (thumb_width - img.width) // 2
        sheet.paste(img, (x, y0))
        draw.text((x0 + 8, y0 + thumb_height + 6), file.name, fill=(0, 0, 0), font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image_dir", type=Path, nargs="?", help="Directory containing PPT page images")
    parser.add_argument("--input-dir", type=Path, default=None, help="Directory containing PPT page images")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output contact sheet path")
    parser.add_argument("--pattern", default="slide-*.png", help="Glob pattern, default: slide-*.png")
    parser.add_argument("--cols", type=int, default=3, help="Number of columns")
    parser.add_argument("--thumb-width", type=int, default=420, help="Thumbnail width in pixels")
    parser.add_argument("--label-height", type=int, default=30, help="Label area height in pixels")
    args = parser.parse_args()

    image_dir = args.input_dir or args.image_dir
    if image_dir is None:
        parser.error("provide an image directory as a positional argument or with --input-dir")

    output = args.output or image_dir / "contact-sheet.jpg"
    build_contact_sheet(image_dir, output, args.pattern, args.cols, args.thumb_width, args.label_height)
    print(output)


if __name__ == "__main__":
    main()
