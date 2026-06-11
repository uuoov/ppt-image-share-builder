# PPT Image Share Builder

[English](README.md) | 简体中文

[![Release](https://img.shields.io/github/v/release/uuoov/ppt-image-share-builder?style=flat-square)](https://github.com/uuoov/ppt-image-share-builder/releases)
[![License](https://img.shields.io/github/license/uuoov/ppt-image-share-builder?style=flat-square)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-2563eb?style=flat-square)](SKILL.md)
[![PowerPoint](https://img.shields.io/badge/output-PPTX_wrapper-b7472a?style=flat-square)](scripts/images_to_pptx.py)

![演示总览图](assets/hero-contact-sheet.jpg)

把一个课程汇报主题、资料文件和参考 PPT 风格，转换成一套以 image2 生成为核心的“PPT 页面图片”工作流：

- 有来源依据的逐页大纲
- 每一页的 image2 页面图片提示词
- 由 image2 或同类图片模型生成的高质量 PPT 页面图片
- 用于检查整体风格的缩略图总览
- 将最终页面图片插入得到的 PPTX 承载文件
- 可直接练习的限时汇报稿
- 根据用户反馈进行局部重生成和修改

这是一个 Codex skill，适合学生、教师、研究者，以及任何需要从零散材料中做出课堂汇报、课程展示、讲座型 PPT 或报告型 PPT 的人。

核心链路是：

```text
资料文件 + 参考 PPT 风格
  -> image2 可直接使用的逐页提示词
  -> 生成 16:9 PPT 页面图片
  -> 制作 contact sheet 总览检查
  -> 按反馈重生成需要修改的页面图片
  -> 把最终图片全屏插入 PPTX 承载文件
  -> 生成限时汇报稿
```

辅助脚本不替代 image2。它们只负责图片生成之后的事情：做图片总览、检查整套页面、把最终 PNG/JPG 页面图片插入 `.pptx` 承载文件。

## 为什么需要这个 Skill

很多 AI 做 PPT 的流程停得太早：

1. 只帮你总结资料。
2. 只生成几张“看起来不错”的图。
3. 留下结构、风格一致性、资料来源、讲稿衔接这些问题给用户自己补。

`ppt-image-share-builder` 封装的是一个更完整的流程：

```mermaid
flowchart LR
  A["主题 + 资料文件"] --> B["抽取并核验资料"]
  B --> C["分析参考 PPT 风格"]
  C --> D["搭建汇报逻辑"]
  D --> E["写逐页图片提示词"]
  E --> F["生成页面图片"]
  F --> G["制作缩略图总览"]
  G --> H["按反馈重生成部分页面图片"]
  H --> I["把最终图片插入 PPTX"]
  I --> J["写限时汇报稿"]
```

它特别适合这些场景：

- 你有一个课程汇报主题；
- 你有教材原文、`.docx`、`.pdf`、网页资料或复制来的文字；
- 你有一个已有 PPT，希望新内容沿用它的蓝白风、学术风、医学风、商务风等；
- 你需要做 8-10 分钟左右的课堂汇报；
- 你希望最后不只是有图片，还要有可讲的稿子。

## 能生成什么

典型输出如下：

```text
<主题>_image2逐页大纲.md
<主题>_10分钟汇报稿.md
<主题>.pptx
outputs/<topic-slug>-images/
  slide-01-cover.png
  slide-02-contents.png
  ...
  slide-13-closing.png
  contact-sheet-13-slides.jpg
```

实际文件名可以根据你的主题和语言调整。

## Demo

仓库现在包含一个真正跑通的示例：**Medical Device Flight Check**。它围绕医疗器械飞行检查课堂汇报，使用公开监管案例和脱敏后的课程资料摘录，由 image2 生成医疗监管视觉资产，再把有来源依据的中文报告内容排成完整 16:9 页面图片，最后生成 contact sheet、PPTX 承载文件和 10 分钟讲稿。

- [输入资料示例](examples/medical-device-flight-check/input-notes.md)
- [逐页内容稿](examples/medical-device-flight-check/report-content.md)
- [image2 逐页大纲示例](examples/medical-device-flight-check/image2-outline.md)
- [生成图片总览](examples/medical-device-flight-check/contact-sheet-demo.jpg)
- [最终讲稿示例](examples/medical-device-flight-check/10-minute-script.md)

原来的 **Campus Lab Safety Risk Inspection** 仍保留为完全脱敏的合成备用示例，但不再作为主预览。

![演示 GIF](assets/demo.gif)

## 安装方式

### Skill Installer

如果你的 Codex 环境带有内置 skill installer，推荐使用：

Windows PowerShell：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo uuoov/ppt-image-share-builder --path . --name ppt-image-share-builder
```

macOS / Linux：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo uuoov/ppt-image-share-builder --path . --name ppt-image-share-builder
```

然后重启 Codex，让它重新加载 skill 元数据。

### 手动 clone

也可以直接把这个仓库克隆到你的 Codex skills 目录：

Windows PowerShell：

```powershell
git clone https://github.com/uuoov/ppt-image-share-builder.git "$env:USERPROFILE\.codex\skills\ppt-image-share-builder"
```

macOS / Linux：

```bash
git clone https://github.com/uuoov/ppt-image-share-builder.git ~/.codex/skills/ppt-image-share-builder
```

### Release 下载

也可以从 [GitHub Releases](https://github.com/uuoov/ppt-image-share-builder/releases) 下载最新 ZIP，解压后放入 Codex skills 目录。

## 快速开始

显式调用这个 skill：

```text
Use $ppt-image-share-builder to turn my course topic, source files, and reference PPT style into image2 page prompts, generated PPT page images, a PPTX wrapper, and a 10-minute presentation script.
```

如果你用中文提需求，可以这样写：

```text
使用 $ppt-image-share-builder。

我需要做一个 10 分钟课堂汇报。
主题是：<你的主题>
受众是：<课程/老师/同学>
参考 PPT 在：<文件路径>
资料包括：<docx/pdf/txt/网页链接>
必须覆盖的关键词：<关键词>

请帮我：
1. 抽取并整理资料；
2. 分析参考 PPT 的整体风格；
3. 写一份 12-14 页的 image2 逐页大纲；
4. 先生成前 3 页图片让我确认风格；
5. 确认后继续生成剩余页面；
6. 做一张总览图检查；
7. 按反馈重生成需要修改的页面图片；
8. 把最终图片插入 PPTX；
9. 最后写一份 10 分钟汇报稿。
```

## 辅助脚本

下面的命令都兼容 Windows PowerShell。PowerShell 5.x 不支持 `&&`，多步命令请分成多行或分开执行。

先安装脚本依赖：

```powershell
python -m pip install -r requirements.txt
```

image2 生成好编号页面图片之后，自动制作 contact sheet：

```powershell
python scripts/make_contact_sheet.py --input-dir examples/medical-device-flight-check/images -o examples/medical-device-flight-check/contact-sheet-demo.jpg
```

重新生成完全脱敏的合成备用 demo，并刷新 README 顶部效果图和 GIF。如果医疗器械真实 demo 存在，顶层预览资产会优先使用这个主 demo，而不是回退到合成占位图：

```powershell
python scripts/create_demo_assets.py
```

使用仓库内置 image2 视觉资产，重新生成有内容的医疗器械飞检 demo：

```powershell
python scripts/create_medical_device_demo.py
```

把 image2 生成好的最终页面图片自动插入 PPTX 承载文件：

```powershell
python scripts/images_to_pptx.py --input-dir examples/medical-device-flight-check/images -o examples/medical-device-flight-check/demo-deck.pptx
```

## 工作流说明

### 1. 收集输入

确认主题、受众、时长、页数、参考 PPT、资料文件和必须出现的关键词。

### 2. 抽取并规范资料

对 `.docx`、`.txt`、`.csv`、`.md` 等材料进行文本抽取。对于中文 Word 文件、政府文件或教材材料，优先规范成 UTF-8，避免乱码和路径编码问题。

### 3. 分析参考 PPT 风格

检查参考 PPT 的：

- 封面和结尾风格
- 目录页结构
- 标题和页码位置
- 配色
- 字体
- 表格/流程图/时间轴样式
- 图片和图标风格
- 信息密度

### 4. 搭建汇报逻辑

先确定汇报主线，再拆成每页的角色。常见结构包括：

- 封面
- 目录
- 为什么重要
- 概念定义
- 制度演进
- 流程框架
- 关键制度
- 案例
- 中外对比
- 趋势和岗位关系
- 总结
- 结尾

### 5. 写逐页图片提示词

每一页通常包含：

- 页面标题
- 画面结构
- 必须出现的文字
- image2 提示词

对于中文较多的页面，skill 会倾向于减少小字，优先保证标题、关键词和图表结构清楚。

### 6. 用 image2 生成 PPT 页面图片并保存

一般先生成前 3 页确认风格，再继续生成后续页面。图片会按页码保存，作为最后展示效果的视觉源文件。

### 7. 做总览图并检查

生成缩略图总览，重点检查：

- 页数是否正确
- 风格是否统一
- 中文是否明显错误
- 页码是否正确
- 是否有重复文件
- 是否出现用户要求删除的内容，例如不该出现的 `Q&A`

### 8. 把最终图片插入 PPTX

把最终确认的页面图片全屏插入 PPTX。这里的 PPTX 是承载文件，核心视觉仍然来自 image2 生成的页面图片。

### 9. 写限时汇报稿

汇报稿不是简单念 PPT，而是补充：

- 页面之间的过渡
- PPT 上没有展开的案例
- 资料来源背后的逻辑
- 面向课堂的口语表达

## 仓库结构

```text
ppt-image-share-builder/
  SKILL.md
  README.md
  README.zh-CN.md
  agents/
    openai.yaml
  assets/
    hero-contact-sheet.jpg
    demo.gif
    social-preview.jpg
  examples/
    medical-device-flight-check/
      input-notes.md
      report-content.md
      image2-outline.md
      contact-sheet-demo.jpg
      demo-deck.pptx
      10-minute-script.md
      images/
      visual-assets/
    lab-safety-check/
      input-notes.md
      image2-outline.md
      contact-sheet-demo.jpg
      10-minute-script.md
  references/
    workflow-checklist.md
    prompt-patterns.md
    qa-checklist.md
  scripts/
    create_demo_assets.py
    create_medical_device_demo.py
    make_contact_sheet.py
    images_to_pptx.py
  requirements.txt
```

## 设计原则

- **资料先行**：法律、日期、数据、案例要有来源依据。
- **风格跟随**：新生成的页面要尽量贴近用户给的参考 PPT。
- **小步确认**：先生成少量页面确认风格，再批量继续。
- **中文友好**：中文图片生成容易出错，尽量控制小字数量。
- **隐私安全**：不要把用户的教材原文、私人姓名、课程文件或未公开材料上传到公开仓库。

## 适用范围

这是一个聚焦型 skill，主要服务于 image2-first 的课堂汇报和报告型 PPT 工作流，适合：

- 把资料整理成 image2 可直接使用的逐页提示词；
- 生成 16:9 的高质量 PPT 页面图片；
- 用 contact sheet 检查整套图片页面；
- 把最终图片插入 PPTX 承载文件；
- 生成对应时长的汇报稿。

## 当前功能

- 医疗器械飞行检查真实跑通 demo：image2 视觉资产、有来源依据的逐页内容稿、contact sheet 检查、PPTX 承载文件和最终讲稿。
- 完全脱敏的合成备用 demo：适合不展示法规或课堂具体材料的公开场景。
- image2 生成图片之后自动生成 contact sheet 的脚本。
- 自动把 image2 页面图片无拉伸地插入 PPTX 的脚本。
- README 顶部效果图、演示 GIF 和 social-preview 素材。
- 方便手动下载的 release ZIP。
- Windows PowerShell 兼容的命令示例。

## 反馈

- 安装问题、脚本报错或 bug，请走 [Issues](https://github.com/uuoov/ppt-image-share-builder/issues)。
- demo 想法、课堂场景、提示词经验，可以发到 [Discussions](https://github.com/uuoov/ppt-image-share-builder/discussions/1)。

## License

MIT. See `LICENSE`.
