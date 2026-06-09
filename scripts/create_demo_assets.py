#!/usr/bin/env python3
"""Generate privacy-safe demo slide images, contact sheet, and GIF."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "examples" / "lab-safety-check"
IMAGE_DIR = DEMO_DIR / "images"
ASSET_DIR = ROOT / "assets"


NAVY = (14, 40, 65)
BLUE = (13, 67, 142)
PALE = (238, 246, 255)
GREEN = (79, 166, 77)
RED = (210, 65, 65)
GRAY = (95, 108, 125)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, radius=18, width=2):
    if hasattr(draw, "rounded_rectangle"):
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle(box, fill=fill, outline=outline, width=width)


def header(draw: ImageDraw.ImageDraw, section: str, title: str, page: str):
    draw.text((60, 35), section, font=font(58, True), fill=BLUE)
    draw.text((150, 45), "|", font=font(46), fill=NAVY)
    draw.text((205, 42), title, font=font(42, True), fill=NAVY)
    draw.text((1740, 42), page, font=font(42, True), fill=BLUE)
    draw.line((55, 125, 1865, 125), fill=BLUE, width=5)


def save_slide(name: str, title: str, subtitle: str, blocks: list[tuple[str, str, tuple[int, int, int]]], page: int):
    img = Image.new("RGB", (1920, 1080), "white")
    draw = ImageDraw.Draw(img)
    header(draw, f"{page:02d}", title, f"P{page}")

    rounded(draw, (70, 180, 1850, 960), fill=(250, 253, 255), outline=(194, 214, 235), radius=28)
    draw.text((120, 220), subtitle, font=font(34, True), fill=NAVY)
    draw.line((120, 275, 820, 275), fill=GREEN, width=6)

    x = 120
    y = 340
    w = 520
    h = 210
    for idx, (head, body, color) in enumerate(blocks):
        bx = x + (idx % 3) * 575
        by = y + (idx // 3) * 260
        rounded(draw, (bx, by, bx + w, by + h), fill=PALE, outline=(190, 210, 232), radius=20)
        draw.ellipse((bx + 30, by + 35, bx + 105, by + 110), fill=color)
        draw.text((bx + 135, by + 42), head, font=font(30, True), fill=NAVY)
        draw.text((bx + 35, by + 130), body, font=font(24), fill=GRAY)

    rounded(draw, (70, 985, 1850, 1040), fill=BLUE, radius=14)
    draw.text((110, 997), "Demo only: synthetic topic, synthetic text, no private course material.", font=font(22), fill="white")

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    img.save(IMAGE_DIR / name, quality=94)


def make_demo_slides():
    slides = [
        (
            "slide-01-cover.png",
            "Lab Safety Inspection",
            "From scattered notes to a sourced classroom deck",
            [
                ("Source-backed", "Extract facts before design", BLUE),
                ("Style-aware", "Follow a reference deck", GREEN),
                ("Script-ready", "Generate speaker notes", RED),
            ],
            1,
        ),
        (
            "slide-02-outline.png",
            "Workflow Overview",
            "A repeatable path for image-based PPT reports",
            [
                ("Collect", "Topic, sources, reference PPT", BLUE),
                ("Audit", "Colors, layout, visual rhythm", GREEN),
                ("Generate", "Prompts, images, contact sheet", RED),
                ("Revise", "Apply user feedback page by page", BLUE),
                ("Script", "Write a timed talk", GREEN),
                ("Deliver", "Folder + README-ready demo", RED),
            ],
            2,
        ),
        (
            "slide-03-source-audit.png",
            "Source Audit",
            "Separate evidence from interpretation",
            [
                ("Documents", "DOCX, PDF, pasted text", BLUE),
                ("Primary sources", "Official pages and dates", GREEN),
                ("Case notes", "Extra examples for the talk", RED),
            ],
            3,
        ),
        (
            "slide-04-image-prompts.png",
            "Image Prompts",
            "A unified visual system plus per-slide prompts",
            [
                ("Visual system", "Palette, typography, icons", BLUE),
                ("Required text", "Short labels, checked manually", GREEN),
                ("No fake logos", "Avoid seals and watermarks", RED),
            ],
            4,
        ),
        (
            "slide-05-qa.png",
            "Contact Sheet QA",
            "Review the whole deck before delivery",
            [
                ("Count", "Expected number of slides", BLUE),
                ("Consistency", "Headers, page numbers, style", GREEN),
                ("Text", "No wrong or forbidden words", RED),
            ],
            5,
        ),
        (
            "slide-06-closing.png",
            "Final Package",
            "Images, outline, and a timed presentation script",
            [
                ("Slides", "Numbered PNG files", BLUE),
                ("Script", "10-minute spoken flow", GREEN),
                ("Handoff", "Clear paths and next steps", RED),
            ],
            6,
        ),
    ]
    for args in slides:
        save_slide(*args)


def make_contact_sheet():
    import importlib.util

    script = ROOT / "scripts" / "make_contact_sheet.py"
    spec = importlib.util.spec_from_file_location("make_contact_sheet", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.build_contact_sheet(IMAGE_DIR, DEMO_DIR / "contact-sheet-demo.jpg", "slide-*.png", 3, 420, 30)


def make_gif():
    files = sorted(IMAGE_DIR.glob("slide-*.png"))
    frames = []
    for file in files:
        img = Image.open(file).convert("RGB")
        img.thumbnail((960, 540), Image.LANCZOS)
        canvas = Image.new("RGB", (960, 540), "white")
        canvas.paste(img, ((960 - img.width) // 2, (540 - img.height) // 2))
        frames.append(canvas)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        ASSET_DIR / "demo.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1100,
        loop=0,
        optimize=True,
    )
    Image.open(DEMO_DIR / "contact-sheet-demo.jpg").save(ASSET_DIR / "hero-contact-sheet.jpg", quality=92)


def main():
    make_demo_slides()
    make_contact_sheet()
    make_gif()
    print(DEMO_DIR)
    print(ASSET_DIR / "hero-contact-sheet.jpg")
    print(ASSET_DIR / "demo.gif")


if __name__ == "__main__":
    main()
