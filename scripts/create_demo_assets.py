#!/usr/bin/env python3
"""Generate a privacy-safe simulated image2 PPT page set, contact sheet, and GIF."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "examples" / "lab-safety-check"
IMAGE_DIR = DEMO_DIR / "images"
ASSET_DIR = ROOT / "assets"

W, H = 1920, 1080

INK = (20, 31, 49)
MUTED = (91, 106, 124)
NAVY = (20, 55, 91)
TEAL = (0, 139, 149)
CYAN = (63, 180, 211)
MINT = (106, 190, 137)
AMBER = (243, 181, 71)
CORAL = (229, 91, 86)
PLUM = (117, 92, 168)
PAPER = (247, 250, 252)
PANEL = (255, 255, 255)
LINE = (210, 221, 232)


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


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, radius=22, width=2) -> None:
    if hasattr(draw, "rounded_rectangle"):
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle(box, fill=fill, outline=outline, width=width)


def text_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int,
    fill=INK,
    bold: bool = False,
    width: int = 42,
    line_gap: int = 10,
) -> int:
    x, y = xy
    fnt = font(size, bold)
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(wrap(paragraph, width=width) or [""])
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += size + line_gap
    return y


def new_slide(title: str, page: int, section: str = "DEMO") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 170, H), fill=NAVY)
    draw.rectangle((170, 0, W, 18), fill=TEAL)
    draw.rectangle((170, H - 18, W, H), fill=AMBER)
    draw.text((54, 58), f"{page:02d}", font=font(54, True), fill="white")
    draw.text((42, 128), section, font=font(18, True), fill=(192, 225, 230))
    draw.text((224, 54), title, font=font(42, True), fill=INK)
    draw.text((1680, 62), f"P{page}", font=font(30, True), fill=TEAL)
    draw.line((224, 126, 1760, 126), fill=LINE, width=2)
    draw.text(
        (224, 1018),
        "Synthetic demo only. Replace these placeholders with image2 outputs in real projects.",
        font=font(20),
        fill=MUTED,
    )
    return img, draw


def card(draw: ImageDraw.ImageDraw, box, title: str, body: str, color=TEAL) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, fill=PANEL, outline=LINE, radius=24, width=2)
    draw.rectangle((x1, y1, x1 + 10, y2), fill=color)
    draw.text((x1 + 34, y1 + 28), title, font=font(28, True), fill=INK)
    text_box(draw, (x1 + 34, y1 + 76), body, 21, fill=MUTED, width=34, line_gap=7)


def draw_flask(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: int = 1) -> None:
    s = scale
    draw.line((cx - 30 * s, cy - 90 * s, cx + 30 * s, cy - 90 * s), fill="white", width=8 * s)
    draw.line((cx - 16 * s, cy - 88 * s, cx - 16 * s, cy - 28 * s), fill="white", width=8 * s)
    draw.line((cx + 16 * s, cy - 88 * s, cx + 16 * s, cy - 28 * s), fill="white", width=8 * s)
    draw.polygon(
        [
            (cx - 18 * s, cy - 28 * s),
            (cx - 70 * s, cy + 80 * s),
            (cx + 70 * s, cy + 80 * s),
            (cx + 18 * s, cy - 28 * s),
        ],
        outline="white",
        fill=None,
    )
    draw.polygon(
        [(cx - 46 * s, cy + 44 * s), (cx + 46 * s, cy + 44 * s), (cx + 62 * s, cy + 76 * s), (cx - 62 * s, cy + 76 * s)],
        fill=(106, 216, 218),
    )


def save(img: Image.Image, name: str) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    img.save(IMAGE_DIR / name)


def slide_cover() -> None:
    img = Image.new("RGB", (W, H), (12, 39, 67))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 18), fill=AMBER)
    draw.rectangle((0, H - 18, W, H), fill=TEAL)
    for x, color in [(1180, TEAL), (1340, CYAN), (1500, MINT), (1660, AMBER)]:
        draw.polygon([(x, 0), (x + 190, 0), (x + 70, H), (x - 120, H)], fill=color)
    rounded(draw, (90, 76, 172, 158), fill=(255, 255, 255), radius=18)
    draw.text((112, 92), "01", font=font(32, True), fill=NAVY)
    draw.text((110, 252), "Campus Lab Safety", font=font(72, True), fill="white")
    draw.text((110, 340), "Risk Inspection Image Pages", font=font(64, True), fill=(206, 240, 244))
    draw.text((112, 454), "A privacy-safe simulated run for image2-first PPT workflows", font=font(30), fill=(210, 220, 230))
    rounded(draw, (112, 560, 620, 720), fill=(255, 255, 255), radius=26)
    draw.text((150, 596), "Source notes", font=font(27, True), fill=INK)
    draw.text((150, 642), "Prompts -> images -> PPTX", font=font(23), fill=MUTED)
    rounded(draw, (690, 560, 1050, 720), fill=(235, 250, 250), radius=26)
    draw.text((728, 596), "8 slides", font=font(32, True), fill=TEAL)
    draw.text((728, 646), "contact-sheet ready", font=font(23), fill=MUTED)
    rounded(draw, (1150, 240, 1560, 760), fill=(20, 55, 91), outline=(95, 186, 198), radius=36, width=4)
    draw_flask(draw, 1356, 494, 2)
    save(img, "slide-01-cover.png")


def slide_storyline() -> None:
    img, draw = new_slide("From Materials To A Deck", 2)
    steps = [
        ("Collect", "topic, sources,\nreference PPT", TEAL),
        ("Audit", "facts, tone,\nvisual rhythm", PLUM),
        ("Prompt", "image2-ready\nslide briefs", CYAN),
        ("Generate", "16:9 page\nimages", MINT),
        ("Wrap", "final images\ninside PPTX", AMBER),
    ]
    x = 250
    for i, (title, body, color) in enumerate(steps):
        cx = x + i * 300
        rounded(draw, (cx, 300, cx + 230, 530), fill=PANEL, outline=LINE, radius=28)
        draw.ellipse((cx + 72, 218, cx + 158, 304), fill=color)
        draw.text((cx + 98, 242), str(i + 1), font=font(28, True), fill="white")
        draw.text((cx + 34, 342), title, font=font(29, True), fill=INK)
        text_box(draw, (cx + 34, 398), body, 22, fill=MUTED, width=18)
        if i < len(steps) - 1:
            draw.line((cx + 232, 414, cx + 296, 414), fill=(158, 176, 196), width=5)
            draw.polygon([(cx + 296, 414), (cx + 278, 402), (cx + 278, 426)], fill=(158, 176, 196))
    rounded(draw, (250, 680, 1700, 830), fill=(235, 249, 249), outline=(188, 226, 229), radius=26)
    draw.text((300, 718), "Core promise", font=font(30, True), fill=TEAL)
    draw.text((300, 768), "The PPTX wrapper preserves the image2 page design instead of rebuilding pages from scratch.", font=font(29), fill=INK)
    save(img, "slide-02-storyline.png")


def slide_source_pack() -> None:
    img, draw = new_slide("Simulated Source Pack", 3)
    card(draw, (260, 215, 760, 405), "Course brief", "Audience, duration, grading context, required keywords.", TEAL)
    card(draw, (820, 215, 1320, 405), "Reference PPT", "Title system, color palette, chart grammar, page markers.", PLUM)
    card(draw, (1380, 215, 1760, 405), "Notes", "Synthetic inspection notes and risk examples.", CYAN)
    rounded(draw, (260, 520, 1760, 830), fill=PANEL, outline=LINE, radius=30)
    draw.text((310, 562), "Evidence rule", font=font(34, True), fill=INK)
    points = [
        ("Separate facts from interpretation", TEAL),
        ("Keep image text short and inspectable", MINT),
        ("Put extra cases in the talk script", AMBER),
        ("Never publish private course material", CORAL),
    ]
    for i, (label, color) in enumerate(points):
        y = 635 + i * 48
        draw.ellipse((318, y, 344, y + 26), fill=color)
        draw.text((370, y - 5), label, font=font(25), fill=MUTED)
    save(img, "slide-03-source-pack.png")


def slide_risk_map() -> None:
    img, draw = new_slide("Risk Map Before Design", 4)
    rounded(draw, (300, 220, 1330, 850), fill=PANEL, outline=LINE, radius=28)
    draw.line((430, 745, 1240, 745), fill=INK, width=4)
    draw.line((430, 745, 430, 320), fill=INK, width=4)
    draw.text((600, 785), "Likelihood", font=font(26, True), fill=MUTED)
    draw.text((330, 455), "Impact", font=font(26, True), fill=MUTED)
    zones = [
        (450, 520, 820, 725, (231, 247, 238), "routine"),
        (840, 520, 1220, 725, (255, 247, 225), "watch"),
        (450, 330, 820, 500, (231, 246, 249), "latent"),
        (840, 330, 1220, 500, (255, 234, 232), "priority"),
    ]
    for box in zones:
        x1, y1, x2, y2, color, label = box
        rounded(draw, (x1, y1, x2, y2), fill=color, outline=(235, 240, 246), radius=18)
        draw.text((x1 + 24, y1 + 24), label.upper(), font=font(23, True), fill=MUTED)
    for x, y, label, color in [
        (950, 410, "Chemical storage", CORAL),
        (1010, 600, "Training gap", AMBER),
        (650, 430, "Waste labels", CYAN),
        (620, 620, "Record delay", MINT),
    ]:
        draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=color)
        draw.text((x + 28, y - 16), label, font=font(22), fill=INK)
    card(draw, (1400, 260, 1730, 420), "Page decision", "Risk map becomes the image set's visual spine.", PLUM)
    card(draw, (1400, 470, 1730, 630), "Prompt decision", "Use color only to encode priority and action.", TEAL)
    save(img, "slide-04-risk-map.png")


def slide_route() -> None:
    img, draw = new_slide("Inspection Route", 5)
    stages = [
        ("Entrance", "identity + scope", TEAL),
        ("Storage", "chemicals + labels", CYAN),
        ("Bench", "operation + PPE", AMBER),
        ("Records", "training + logs", PLUM),
        ("Closeout", "risks + actions", MINT),
    ]
    y = 500
    for i, (name, note, color) in enumerate(stages):
        x = 270 + i * 300
        draw.line((x + 95, y, x + 300, y), fill=LINE, width=6)
        draw.ellipse((x, y - 70, x + 140, y + 70), fill=color)
        draw.text((x + 44, y - 24), f"{i + 1}", font=font(42, True), fill="white")
        draw.text((x - 10, y + 110), name, font=font(28, True), fill=INK)
        draw.text((x - 10, y + 155), note, font=font(21), fill=MUTED)
    rounded(draw, (290, 760, 1620, 890), fill=(255, 250, 236), outline=(235, 215, 171), radius=28)
    draw.text((340, 797), "Speaker note", font=font(30, True), fill=(167, 112, 27))
    draw.text((550, 802), "Use the route to explain how messy notes become clear image pages.", font=font(27), fill=INK)
    save(img, "slide-05-inspection-route.png")


def slide_prompt_board() -> None:
    img, draw = new_slide("Image2 Prompt Board", 6)
    rounded(draw, (260, 205, 1760, 860), fill=(22, 34, 52), outline=(66, 86, 114), radius=30)
    draw.text((315, 250), "Unified visual system", font=font(32, True), fill="white")
    draw.text((315, 306), "16:9 PPT, deep navy titles, clean academic layout, teal/mint/coral risk accents, no logos.", font=font(25), fill=(211, 224, 235))
    columns = [
        ("Slide role", ["Cover", "Risk map", "Route", "QA"]),
        ("Required text", ["short labels", "page number", "title", "no Q&A"]),
        ("Constraints", ["no fake seals", "readable text", "consistent palette", "real source notes"]),
    ]
    for i, (title, rows) in enumerate(columns):
        x = 320 + i * 470
        rounded(draw, (x, 420, x + 400, 750), fill=(255, 255, 255), radius=24)
        draw.text((x + 32, 455), title, font=font(27, True), fill=INK)
        for j, row in enumerate(rows):
            y = 520 + j * 52
            draw.ellipse((x + 36, y + 6, x + 58, y + 28), fill=[TEAL, AMBER, CORAL, MINT][j])
            draw.text((x + 78, y), row, font=font(23), fill=MUTED)
    save(img, "slide-06-prompt-board.png")


def slide_contact_qa() -> None:
    img, draw = new_slide("Contact Sheet QA", 7)
    x0, y0 = 270, 205
    for i in range(8):
        x = x0 + (i % 4) * 330
        y = y0 + (i // 4) * 225
        color = [TEAL, CYAN, MINT, AMBER, PLUM, CORAL, NAVY, (105, 137, 160)][i]
        rounded(draw, (x, y, x + 260, y + 146), fill=(255, 255, 255), outline=LINE, radius=18)
        draw.rectangle((x + 12, y + 12, x + 248, y + 82), fill=color)
        draw.text((x + 24, y + 102), f"slide-{i + 1:02d}.png", font=font(20, True), fill=INK)
    card(draw, (270, 710, 700, 885), "Count", "8 slides, no duplicate variants.", TEAL)
    card(draw, (760, 710, 1190, 885), "Style", "Headers, colors, and density align.", MINT)
    card(draw, (1250, 710, 1680, 885), "Text", "Short labels remain reviewable.", CORAL)
    save(img, "slide-07-contact-sheet-qa.png")


def slide_handoff() -> None:
    img, draw = new_slide("Final Handoff", 8)
    files = [
        ("image2-outline.md", "page-by-page prompt plan", TEAL),
        ("slide-XX.png", "final image2 slide pages", CYAN),
        ("contact-sheet.jpg", "deck-level visual QA", AMBER),
        ("demo-deck.pptx", "wrapper for final images", PLUM),
        ("10-minute-script.md", "speaker-ready narrative", MINT),
    ]
    for i, (name, desc, color) in enumerate(files):
        x = 310 + (i % 2) * 670
        y = 210 + (i // 2) * 190
        rounded(draw, (x, y, x + 570, y + 132), fill=PANEL, outline=LINE, radius=22)
        draw.rectangle((x, y, x + 12, y + 132), fill=color)
        draw.text((x + 42, y + 28), name, font=font(28, True), fill=INK)
        draw.text((x + 42, y + 76), desc, font=font(22), fill=MUTED)
    rounded(draw, (980, 780, 1600, 910), fill=(233, 248, 247), outline=(183, 226, 222), radius=26)
    draw.text((1025, 817), "Ready for rehearsal", font=font(34, True), fill=TEAL)
    draw.text((1025, 866), "The PPTX is image-led; the script carries the extra context.", font=font(24), fill=INK)
    save(img, "slide-08-final-handoff.png")


def make_demo_slides() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for file in IMAGE_DIR.glob("slide-*.png"):
        file.unlink()
    slide_cover()
    slide_storyline()
    slide_source_pack()
    slide_risk_map()
    slide_route()
    slide_prompt_board()
    slide_contact_qa()
    slide_handoff()


def make_contact_sheet() -> None:
    script = ROOT / "scripts" / "make_contact_sheet.py"
    prior_bytecode_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("make_contact_sheet", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior_bytecode_setting
    module.build_contact_sheet(IMAGE_DIR, DEMO_DIR / "contact-sheet-demo.jpg", "slide-*.png", 4, 390, 34)


def make_gif() -> None:
    files = sorted(IMAGE_DIR.glob("slide-*.png"))
    frames = []
    for file in files:
        img = Image.open(file).convert("RGB")
        img.thumbnail((960, 540), Image.LANCZOS)
        canvas = Image.new("RGB", (960, 540), PAPER)
        canvas.paste(img, ((960 - img.width) // 2, (540 - img.height) // 2))
        frames.append(canvas)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        ASSET_DIR / "demo.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1200,
        loop=0,
        optimize=True,
    )
    Image.open(DEMO_DIR / "contact-sheet-demo.jpg").save(ASSET_DIR / "hero-contact-sheet.jpg", quality=92)
    cover = Image.open(IMAGE_DIR / "slide-01-cover.png").convert("RGB")
    cover.thumbnail((1280, 720), Image.LANCZOS)
    preview = Image.new("RGB", (1280, 640), (12, 39, 67))
    preview.paste(cover, (0, -40))
    preview.save(ASSET_DIR / "social-preview.jpg", quality=92)


def main() -> None:
    make_demo_slides()
    make_contact_sheet()
    make_gif()
    print(DEMO_DIR)
    print(ASSET_DIR / "hero-contact-sheet.jpg")
    print(ASSET_DIR / "demo.gif")
    print(ASSET_DIR / "social-preview.jpg")


if __name__ == "__main__":
    main()
