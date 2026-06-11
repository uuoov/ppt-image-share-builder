#!/usr/bin/env python3
"""Build a content-rich medical-device flight-check image demo.

The demo keeps the image2-first delivery model: final slides are still full-page
images. For source-critical Chinese text, this script composes exact content on
top of image2-generated visual assets so the public demo is both attractive and
substantive.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "examples" / "medical-device-flight-check"
IMAGE_DIR = DEMO_DIR / "images"
VISUAL_DIR = DEMO_DIR / "visual-assets"

W, H = 1920, 1080

NAVY = (9, 49, 102)
BLUE = (17, 97, 176)
CYAN = (38, 164, 205)
GREEN = (55, 157, 89)
MINT = (226, 246, 241)
AMBER = (235, 160, 42)
RED = (203, 55, 63)
INK = (19, 32, 52)
MUTED = (83, 101, 124)
LINE = (191, 211, 232)
PAPER = (247, 251, 255)
WHITE = (255, 255, 255)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf" if bold else "C:/Windows/Fonts/simsun.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def crop_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = img.size
    ratio = max(target_w / src_w, target_h / src_h)
    resized = img.resize((int(src_w * ratio), int(src_h * ratio)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def bg(name: str, wash: int = 218) -> Image.Image:
    path = VISUAL_DIR / name
    if path.exists():
        img = crop_cover(Image.open(path).convert("RGB"), (W, H))
    else:
        img = Image.new("RGB", (W, H), PAPER)
    overlay = Image.new("RGBA", (W, H), (255, 255, 255, wash))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    return img.convert("RGB")


def rect(draw: ImageDraw.ImageDraw, box, fill, outline=None, radius=22, width=2) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for ch in paragraph:
            candidate = current + ch
            if text_size(draw, candidate, fnt)[0] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = ch
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int,
    fill=INK,
    bold: bool = False,
    max_width: int = 500,
    line_gap: int = 8,
) -> int:
    x, y = xy
    fnt = font(size, bold)
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += size + line_gap
    return y


def header(draw: ImageDraw.ImageDraw, title: str, page: int, section: str) -> None:
    draw.text((74, 46), f"{page:02d}", font=font(54, True), fill=NAVY)
    draw.text((178, 54), "|", font=font(48, True), fill=BLUE)
    draw.text((214, 52), title, font=font(44, True), fill=INK)
    draw.text((1600, 62), f"P{page}", font=font(30, True), fill=NAVY)
    draw.line((72, 122, 1848, 122), fill=NAVY, width=5)
    rect(draw, (72, 944, 1848, 1018), fill=NAVY, radius=16)
    draw.text((112, 964), section, font=font(26, True), fill=WHITE)


def footer(draw: ImageDraw.ImageDraw, source: str) -> None:
    draw.text((78, 1032), source, font=font(18), fill=(103, 120, 140))


def card(draw: ImageDraw.ImageDraw, box, title: str, body: str, color=BLUE, body_size: int = 26) -> None:
    x1, y1, x2, y2 = box
    rect(draw, box, fill=WHITE, outline=LINE, radius=20)
    draw.rectangle((x1, y1, x1 + 12, y2), fill=color)
    draw.text((x1 + 34, y1 + 26), title, font=font(30, True), fill=INK)
    draw_wrapped(draw, (x1 + 34, y1 + 76), body, body_size, fill=MUTED, max_width=x2 - x1 - 70, line_gap=8)


def bullet_list(draw: ImageDraw.ImageDraw, x: int, y: int, items: list[tuple[str, str]], color=BLUE, size=27, gap=58) -> None:
    for i, (head, body) in enumerate(items):
        cy = y + i * gap
        draw.ellipse((x, cy + 7, x + 24, cy + 31), fill=color)
        draw.text((x + 38, cy), head, font=font(size, True), fill=INK)
        draw.text((x + 220, cy + 2), body, font=font(size - 2), fill=MUTED)


def table(draw: ImageDraw.ImageDraw, box, headers: list[str], rows: list[list[str]], widths: list[int], row_h: int = 78) -> None:
    x1, y1, x2, _ = box
    rect(draw, box, fill=WHITE, outline=LINE, radius=18)
    draw.rectangle((x1, y1, x2, y1 + row_h), fill=NAVY)
    x = x1
    for i, head in enumerate(headers):
        draw.text((x + 18, y1 + 23), head, font=font(24, True), fill=WHITE)
        x += widths[i]
        if i < len(widths) - 1:
            draw.line((x, y1, x, box[3]), fill=LINE, width=2)
    for r, row in enumerate(rows):
        y = y1 + row_h + r * row_h
        fill = (247, 251, 255) if r % 2 == 0 else WHITE
        draw.rectangle((x1, y, x2, y + row_h), fill=fill)
        draw.line((x1, y, x2, y), fill=LINE, width=2)
        x = x1
        for i, cell in enumerate(row):
            draw_wrapped(draw, (x + 18, y + 16), cell, 22, fill=INK if i == 0 else MUTED, bold=(i == 0), max_width=widths[i] - 34, line_gap=3)
            x += widths[i]


def save(img: Image.Image, name: str) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    img.save(IMAGE_DIR / name)


def slide_01() -> None:
    img = bg("image2-bg-inspection-lab.png", wash=92)
    draw = ImageDraw.Draw(img)
    rect(draw, (72, 80, 1000, 720), fill=(255, 255, 255), outline=(214, 229, 244), radius=34)
    draw.text((120, 150), "从“提前准备”到", font=font(66, True), fill=NAVY)
    draw.text((120, 238), "“随时接受检查”", font=font(76, True), fill=NAVY)
    draw.line((122, 348, 920, 348), fill=BLUE, width=6)
    draw.text((120, 388), "医疗器械飞行检查制度的监管逻辑", font=font(38, True), fill=INK)
    draw.text((120, 466), "《药品医疗器械飞行检查办法》主题分享", font=font(30, True), fill=BLUE)
    draw.text((124, 544), "汇报人：梁志聪    日期：2026年", font=font(28), fill=MUTED)
    labels = [("风险防控", GREEN), ("现场真实", BLUE), ("证据固定", CYAN), ("快速处置", AMBER)]
    for i, (label, color) in enumerate(labels):
        x = 120 + i * 210
        draw.ellipse((x, 622, x + 58, 680), fill=color)
        draw.text((x + 74, 633), label, font=font(25, True), fill=INK)
    rect(draw, (72, 906, 1848, 1018), fill=NAVY, radius=22)
    draw.text((118, 940), "核心观点：飞检不是“突然袭击”，而是把文件合规拉回真实现场与风险闭环。", font=font(34, True), fill=WHITE)
    save(img, "slide-01-cover.png")


def slide_02() -> None:
    img = bg("image2-bg-lifecycle-shield.png", wash=225)
    draw = ImageDraw.Draw(img)
    header(draw, "目录：用 4 个问题串起这份报告", 2, "本报告的逻辑不是逐条背法条，而是解释飞检为什么能改变企业日常运行。")
    items = [
        ("01", "为什么需要飞检", "从监管信息差、质量风险和患者安全看制度价值"),
        ("02", "《办法》怎么运作", "启动、入场、取证、报告、风险控制和后续处理"),
        ("03", "公开案例说明什么", "委托生产接口、现场记录、无菌与放行的典型缺陷"),
        ("04", "医工学生学什么", "把法规要求转化为岗位能力、记录能力和整改能力"),
    ]
    for i, (num, title, body) in enumerate(items):
        y = 190 + i * 160
        draw.ellipse((130, y, 214, y + 84), fill=BLUE if i < 2 else GREEN)
        draw.text((151, y + 20), num, font=font(28, True), fill=WHITE)
        card(draw, (250, y - 8, 1700, y + 102), title, body, color=BLUE if i < 2 else GREEN, body_size=26)
    footer(draw, "来源：总局令第14号；国家药监局/核查中心公开通告；NMPA 2024统计年度数据。")
    save(img, "slide-02-contents.png")


def slide_03() -> None:
    img = bg("image2-bg-cleanroom-records.png", wash=205)
    draw = ImageDraw.Draw(img)
    header(draw, "为什么常规检查还不够", 3, "飞检的价值：把监管从“看文件有没有”推进到“看体系是否真实运行”。")
    card(draw, (90, 190, 575, 420), "监管端：信息差", "投诉举报、不良事件、抽检异常、资料疑问往往不是定期检查当天出现。飞检让监管能顺着风险线索直接到现场。", BLUE, 24)
    card(draw, (620, 190, 1105, 420), "企业端：临时准备", "如果所有检查都提前通知，现场可能被整理成“迎检状态”，不能代表日常质量体系。", AMBER, 24)
    card(draw, (1150, 190, 1635, 420), "患者端：风险外溢", "医疗器械从设计、生产、灭菌、放行到使用，任何环节失守都可能转化为安全有效性问题。", RED, 24)
    rect(draw, (160, 520, 1760, 790), fill=WHITE, outline=LINE, radius=26)
    draw.text((220, 565), "课本关键词", font=font(34, True), fill=NAVY)
    for i, (kw, note, color) in enumerate([
        ("突击性", "不预先告知，压缩临时修饰空间", RED),
        ("独立性", "检查组依法独立、客观公正", BLUE),
        ("高效性", "发现风险后快速衔接控制措施", GREEN),
    ]):
        x = 520 + i * 390
        draw.ellipse((x, 555, x + 92, 647), fill=color)
        draw.text((x + 120, 560), kw, font=font(32, True), fill=INK)
        draw_wrapped(draw, (x + 120, 610), note, 24, fill=MUTED, max_width=260)
    footer(draw, "依据：《药品医疗器械飞行检查办法》及其说明。")
    save(img, "slide-03-why-flight-check.png")


def slide_04() -> None:
    img = bg("image2-bg-inspection-lab.png", wash=230)
    draw = ImageDraw.Draw(img)
    header(draw, "飞行检查是什么：不是只看“打招呼”", 4, "定义 + 范围 + 原则 + 核心要求，是理解后面流程和案例的入口。")
    card(draw, (90, 190, 680, 440), "定义", "针对药品和医疗器械研制、生产、经营、使用等环节开展的不预先告知的监督检查。", BLUE, 27)
    card(draw, (725, 190, 1315, 440), "范围", "医疗器械全链条：研制、注册、生产、经营、使用、上市后监测、召回与整改。", CYAN, 27)
    card(draw, (1360, 190, 1830, 440), "框架", "总则、启动、检查、处理、附则；共 5 章 35 条，自 2015 年 9 月 1 日施行。", GREEN, 26)
    rect(draw, (130, 545, 1790, 790), fill=(238, 247, 255), outline=(174, 207, 236), radius=26)
    draw.text((190, 585), "一句话记忆：", font=font(34, True), fill=NAVY)
    for i, word in enumerate(["启得快", "办得实", "查得严", "处得准"]):
        x = 500 + i * 300
        rect(draw, (x, 570, x + 230, 675), fill=WHITE, outline=LINE, radius=20)
        draw.text((x + 44, 602), word, font=font(34, True), fill=[BLUE, CYAN, RED, GREEN][i])
    draw.text((190, 710), "快：风险线索出现后迅速启动；实：进入真实现场；严：固定证据；准：衔接整改、暂停、召回、处罚或移送。", font=font(26), fill=INK)
    footer(draw, "依据：总局令第14号；关于《药品医疗器械飞行检查办法》的说明。")
    save(img, "slide-04-definition.png")


def slide_05() -> None:
    img = bg("image2-bg-lifecycle-shield.png", wash=226)
    draw = ImageDraw.Draw(img)
    header(draw, "启动情形：飞检不是随机吓人", 5, "启动依据通常来自风险线索，重点是把“可能有问题”转化为现场核查。")
    items = [
        ("投诉举报", "产品质量、安全有效性或资料真实性被质疑"),
        ("抽检/监测异常", "抽检不合格、不良事件聚集、舆情或风险信号"),
        ("注册/许可疑问", "申报资料、生产条件、委托关系存在异常"),
        ("监管计划", "重点企业、高风险产品、带量采购中选产品等"),
        ("其他线索", "上级交办、跨区域协查、前次整改复查"),
    ]
    bullet_list(draw, 155, 220, items, color=BLUE, size=29, gap=92)
    rect(draw, (1120, 220, 1740, 738), fill=WHITE, outline=LINE, radius=28)
    draw.text((1170, 265), "启动后要解决的 3 个问题", font=font(32, True), fill=NAVY)
    for i, (head, body, color) in enumerate([
        ("查什么", "锁定产品、批次、场地、记录和人员", BLUE),
        ("谁来查", "检查组独立实施，必要时跨区域协同", GREEN),
        ("怎么处置", "发现风险后同步准备控制措施", RED),
    ]):
        y = 350 + i * 112
        draw.ellipse((1175, y, 1235, y + 60), fill=color)
        draw.text((1255, y + 4), head, font=font(28, True), fill=INK)
        draw.text((1255, y + 42), body, font=font(23), fill=MUTED)
    footer(draw, "依据：《办法》启动章节；NMPA/CFDI公开飞检通告常见启动背景。")
    save(img, "slide-05-timeline.png")


def slide_06() -> None:
    img = bg("image2-bg-cleanroom-records.png", wash=222)
    draw = ImageDraw.Draw(img)
    header(draw, "核心流程：从启动到公开处理", 6, "飞检不是“进去看看”，而是一套证据链和风险处置链。")
    steps = [
        ("启动", "风险线索/计划任务"),
        ("方案", "范围、重点、人员"),
        ("入场", "不预先告知，亮明身份"),
        ("检查取证", "现场、记录、抽样、电子数据"),
        ("报告", "形成事实与缺陷判断"),
        ("处理公开", "整改、暂停、召回、处罚、移送"),
    ]
    y = 315
    for i, (name, note) in enumerate(steps):
        x = 95 + i * 300
        draw.ellipse((x, y, x + 94, y + 94), fill=BLUE if i < 4 else GREEN)
        draw.text((x + 31, y + 24), f"{i+1}", font=font(30, True), fill=WHITE)
        draw.line((x + 94, y + 47, x + 285, y + 47), fill=LINE, width=5)
        draw.text((x - 8, y + 128), name, font=font(30, True), fill=INK)
        draw_wrapped(draw, (x - 8, y + 176), note, 23, fill=MUTED, max_width=250)
    rect(draw, (130, 700, 1790, 855), fill=WHITE, outline=LINE, radius=24)
    draw.text((180, 738), "现场实施要点", font=font(32, True), fill=NAVY)
    draw.text((460, 742), "亮明身份  |  明确义务  |  调取文件  |  复制拍照  |  抽样检验  |  结果通报", font=font(30, True), fill=INK)
    footer(draw, "依据：《办法》检查与处理章节；公开通告中的整改、暂停生产、召回要求。")
    save(img, "slide-06-process.png")


def slide_07() -> None:
    img = bg("image2-bg-inspection-lab.png", wash=228)
    draw = ImageDraw.Draw(img)
    header(draw, "关键制度力量：两不两原 + 配合义务", 7, "飞检有力量，不只因为突然，而是因为现场、证据和处置能直接衔接。")
    four = [
        ("不预先告知", "不提前透露行程和检查内容，减少迎检式准备。", RED),
        ("不透露线索", "不得泄露检查进展和违法线索，避免被检查对象提前规避。", RED),
        ("第一时间入场", "到达后直接进入可能存在问题的现场，不绕弯。", BLUE),
        ("原始状态核查", "尽量查看原始记录、原始场景、原始数据。", GREEN),
    ]
    for i, (title, body, color) in enumerate(four):
        x = 100 + (i % 2) * 875
        y = 190 + (i // 2) * 220
        card(draw, (x, y, x + 800, y + 165), title, body, color, 25)
    rows = [
        ["材料提供", "文件、记录、票据、凭证、电子数据应真实、完整、有效"],
        ["现场配合", "不得拖延进入、停产逃避、拒绝拍照复印或抽样"],
        ["风险后果", "拒绝、逃避、阻碍检查可能进入从重处理逻辑"],
    ]
    table(draw, (180, 690, 1740, 924), ["配合事项", "具体含义"], rows, [310, 1250], row_h=58)
    footer(draw, "依据：《办法》第五条及检查实施要求；课堂关键词“两不两原”。")
    save(img, "slide-07-key-mechanisms.png")


def slide_08() -> None:
    img = bg("image2-bg-lifecycle-shield.png", wash=222)
    draw = ImageDraw.Draw(img)
    header(draw, "案例 1：2026 年委托生产接口失守", 8, "注册人可以委托生产，但质量责任不能外包。")
    rect(draw, (100, 190, 820, 820), fill=WHITE, outline=LINE, radius=26)
    draw.text((150, 235), "2026 年第 18 号通告", font=font(34, True), fill=NAVY)
    draw_wrapped(draw, (150, 300), "国家药监局对山西银药师医药有限公司及两家受托生产企业开展飞行检查，发现质量管理体系存在严重缺陷。", 28, fill=INK, max_width=600, line_gap=10)
    draw.text((150, 462), "监管措施", font=font(30, True), fill=RED)
    bullet_list(draw, 158, 514, [
        ("暂停生产", "依法采取风险控制措施"),
        ("风险评估", "评估产品安全风险"),
        ("整改复查", "整改合格后方可恢复"),
    ], color=RED, size=25, gap=72)
    rows = [
        ["质量协议", "未定期评审适宜性、充分性、有效性"],
        ["现场审核", "注册人未定期对受托方体系开展现场审核"],
        ["过程控制", "关键风险点监控、设计转换、放行衔接不到位"],
        ["课堂启示", "委托生产不是责任转移，而是接口管理能力测试"],
    ]
    table(draw, (890, 215, 1780, 655), ["问题点", "为什么重要"], rows, [230, 660], row_h=88)
    footer(draw, "依据：国家药监局 2026年第18号医疗器械飞行检查情况通告。")
    save(img, "slide-08-2026-delegated-manufacturing.png")


def slide_09() -> None:
    img = bg("image2-bg-cleanroom-records.png", wash=214)
    draw = ImageDraw.Draw(img)
    header(draw, "案例 2：现场、设施与记录能否对上", 9, "公开案例共同说明：飞检不是只查制度文件，而是看文件、现场、记录能否相互印证。")
    card(draw, (100, 190, 850, 650), "2025 年：江苏百易得 7 项一般不符合", "产品：不可吸收带线锚钉。缺陷集中在仓储状态标识、设备维护、空调压差与过滤器风险、纯化水职责、文件控制、生产清洗参数和现场操作偏差。", BLUE, 27)
    card(draw, (930, 190, 1780, 650), "2024 年：威海华特严重缺陷", "问题涉及无菌检验室环境控制、设备验证、灭菌剂残留量验证、成品放行检验、管理评审等；监管要求暂停生产并评估产品安全风险。", RED, 27)
    rect(draw, (200, 740, 1720, 890), fill=(238, 247, 255), outline=(174, 207, 236), radius=24)
    draw.text((250, 780), "共同模式：", font=font(34, True), fill=NAVY)
    draw.text((470, 785), "现场状态、记录数据、职责分工、放行依据、风险评估之间不能断链。", font=font(32, True), fill=INK)
    footer(draw, "依据：CFDI 2025年第1号通告及附件；国家药监局 2024年第28号通告。")
    save(img, "slide-09-site-records.png")


def slide_10() -> None:
    img = bg("image2-bg-inspection-lab.png", wash=230)
    draw = ImageDraw.Draw(img)
    header(draw, "中外对比：相似的是风险导向，不同的是制度工具", 10, "不能把中国飞检、FDA 检查、欧盟公告机构不预告审核简单画等号。")
    headers = ["维度", "中国飞检", "美国 FDA", "欧盟 MDR"]
    rows = [
        ["监管主体", "药品监管部门组织实施", "FDA 风险基础检查", "公告机构监督审核"],
        ["典型触发", "投诉举报、抽检/监测异常、资料疑问、重点监管", "常规/风险/投诉/上市前后检查", "证书周期内监督；不预告审核"],
        ["证据工具", "现场记录、复制拍照、抽样、电子数据", "Form 483、Warning Letter 等", "审核报告、抽样测试、证书管理"],
        ["后果衔接", "整改、暂停、召回、处罚、公开、移送", "整改、警告信、进口/执法措施", "整改、暂停/撤销证书、监督升级"],
    ]
    table(draw, (90, 190, 1830, 650), headers, rows, [260, 500, 500, 480], row_h=92)
    rect(draw, (170, 860, 1750, 930), fill=(236, 248, 241), outline=(177, 220, 190), radius=18)
    draw.text((220, 878), "共同点：都不是只看“有没有文件”，而是通过现场证据判断质量体系是否真实有效。", font=font(28, True), fill=GREEN)
    footer(draw, "依据：FDA Form 483/Warning Letter 公开说明；EU MDR Annex IX 3.4；中国《办法》。")
    save(img, "slide-10-international-comparison.png")


def slide_11() -> None:
    img = bg("image2-bg-lifecycle-shield.png", wash=216)
    draw = ImageDraw.Draw(img)
    header(draw, "趋势与职业：从纸面合规到真实运行", 11, "飞检把法规、质量体系、生产现场、数据记录和整改闭环连在一起。")
    rows = [
        ["注册法规专员", "注册申报、法规检索、变更与合规判断", "8k-15k/月"],
        ["质量体系工程师", "QMS 文件、内审、管理评审、CAPA", "9k-18k/月"],
        ["生产/供应商质量工程师", "过程控制、供应商审核、技术转移", "10k-20k/月"],
        ["临床评价/上市后监测", "临床评价、PMS、不良事件与风险管理", "10k-22k/月"],
    ]
    table(draw, (770, 210, 1810, 600), ["岗位方向", "核心能力", "薪资参考"], rows, [310, 500, 230], row_h=78)
    rect(draw, (100, 210, 670, 680), fill=WHITE, outline=LINE, radius=26)
    draw.text((150, 250), "全生命周期监管环", font=font(32, True), fill=NAVY)
    center = (390, 450)
    r = 170
    labels = ["注册", "生产", "经营", "使用", "监测", "整改"]
    for i, label in enumerate(labels):
        angle = -math.pi / 2 + i * math.pi * 2 / len(labels)
        x = center[0] + int(math.cos(angle) * r)
        y = center[1] + int(math.sin(angle) * r)
        draw.ellipse((x - 42, y - 42, x + 42, y + 42), fill=BLUE if i < 3 else GREEN)
        draw.text((x - 28, y - 16), label, font=font(24, True), fill=WHITE)
    draw.ellipse((center[0] - 80, center[1] - 80, center[0] + 80, center[1] + 80), fill=(232, 243, 255), outline=BLUE, width=5)
    draw.text((center[0] - 56, center[1] - 18), "飞检", font=font(34, True), fill=NAVY)
    rect(draw, (105, 742, 1810, 850), fill=NAVY, radius=22)
    draw.text((150, 772), "2024年：医疗器械生产企业飞行检查 3024 家次，其中停产整改 333 家次。", font=font(35, True), fill=WHITE)
    draw.text((150, 870), "注：薪资为公开招聘样本的课堂参考区间，受城市、企业规模、经验和学历影响较大。", font=font(22), fill=MUTED)
    footer(draw, "依据：NMPA 2024药品监督管理统计年度数据；岗位薪资为脱敏招聘样本区间。")
    save(img, "slide-11-trends-careers.png")


def slide_12() -> None:
    img = bg("image2-bg-cleanroom-records.png", wash=222)
    draw = ImageDraw.Draw(img)
    header(draw, "总结：飞检带来的真正提醒", 12, "对企业是日常体系能力测试；对学生是法规、质量和现场执行能力的交叉训练。")
    for i, (title, body, color) in enumerate([
        ("真实", "看现场、看实物、看运行状态，而不是只看迎检材料。", BLUE),
        ("追溯", "采购、生产、检验、放行、投诉、召回都要有证据链。", CYAN),
        ("风险控制", "发现问题后能暂停、整改、召回、处罚或移送。", GREEN),
    ]):
        x = 120 + i * 590
        card(draw, (x, 220, x + 500, 560), title, body, color, 29)
    rect(draw, (200, 660, 1720, 840), fill=(238, 247, 255), outline=(174, 207, 236), radius=24)
    draw.text((250, 702), "对医工学生：", font=font(34, True), fill=NAVY)
    draw.text((520, 707), "把法规要求、质量体系、现场执行和数据记录真正对齐。", font=font(34, True), fill=INK)
    draw.text((250, 772), "未来无论做 RA、QA、工艺、验证、PMS，都要能回答：证据在哪里？风险有没有闭环？", font=font(27), fill=MUTED)
    footer(draw, "依据：本报告对《办法》、公开飞检案例和课程关键词的归纳。")
    save(img, "slide-12-summary.png")


def slide_13() -> None:
    img = bg("image2-bg-inspection-lab.png", wash=105)
    draw = ImageDraw.Draw(img)
    rect(draw, (92, 96, 980, 720), fill=(255, 255, 255), outline=(214, 229, 244), radius=34)
    draw.text((145, 170), "感谢垂听", font=font(78, True), fill=NAVY)
    draw.text((145, 292), "《药品医疗器械飞行检查办法》主题分享", font=font(36, True), fill=INK)
    draw.line((145, 358, 820, 358), fill=BLUE, width=6)
    draw.text((145, 420), "从“提前准备”到“随时接受检查”", font=font(35, True), fill=BLUE)
    draw_wrapped(draw, (145, 492), "核心收束：飞检不是临时事件，而是质量体系是否日常真实运行的一次现场验证。", 30, fill=MUTED, max_width=740)
    draw.text((145, 642), "欢迎批评指正", font=font(30, True), fill=GREEN)
    rect(draw, (92, 906, 1848, 1018), fill=NAVY, radius=22)
    draw.text((138, 940), "关键词：突击性｜独立性｜高效性｜真实｜追溯｜风险控制", font=font(34, True), fill=WHITE)
    save(img, "slide-13-closing.png")


def main() -> None:
    slides = [
        slide_01,
        slide_02,
        slide_03,
        slide_04,
        slide_05,
        slide_06,
        slide_07,
        slide_08,
        slide_09,
        slide_10,
        slide_11,
        slide_12,
        slide_13,
    ]
    for build in slides:
        build()
    print(IMAGE_DIR)


if __name__ == "__main__":
    main()
