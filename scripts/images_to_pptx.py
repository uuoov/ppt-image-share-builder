#!/usr/bin/env python3
"""Assemble generated slide images into a PowerPoint deck.

Requires python-pptx:
    python -m pip install python-pptx
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slide_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"slide[-_ ]?(\d+)", path.stem, re.IGNORECASE)
    if match:
        return (int(match.group(1)), path.name)
    return (10_000, path.name)


def import_pptx():
    try:
        from pptx import Presentation
        from pptx.util import Inches
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: python-pptx. Install it with:\n"
            "  python -m pip install python-pptx"
        ) from exc
    return Presentation, Inches


def build_pptx(image_dir: Path, output: Path, pattern: str) -> None:
    Presentation, Inches = import_pptx()
    files = sorted(image_dir.glob(pattern), key=slide_sort_key)
    if not files:
        raise SystemExit(f"No images matched {pattern!r} in {image_dir}")

    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for file in files:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(str(file), 0, 0, width=prs.slide_width, height=prs.slide_height)

    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image_dir", type=Path, nargs="?", help="Directory containing slide images")
    parser.add_argument("--input-dir", type=Path, default=None, help="Directory containing slide images")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output .pptx path")
    parser.add_argument("--pattern", default="slide-*.png", help="Glob pattern, default: slide-*.png")
    args = parser.parse_args()

    image_dir = args.input_dir or args.image_dir
    if image_dir is None:
        parser.error("provide an image directory as a positional argument or with --input-dir")

    build_pptx(image_dir, args.output, args.pattern)
    print(args.output)


if __name__ == "__main__":
    main()
