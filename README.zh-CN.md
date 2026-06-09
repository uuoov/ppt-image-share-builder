# PPT Image Share Builder

[English](README.md) | 简体中文

把一个课程汇报主题、资料文件和参考 PPT 风格，转换成一套完整的“图片式 PPT 汇报”工作流：

- 有来源依据的逐页大纲
- 每一页的 image2 / 图片生成提示词
- 生成好的 PPT 页面图片
- 用于检查整体风格的缩略图总览
- 可直接练习的限时汇报稿
- 根据用户反馈进行局部重生成和修改

这是一个 Codex skill，适合学生、教师、研究者，以及任何需要从零散材料中做出课堂汇报、课程展示、讲座型 PPT 或报告型 PPT 的人。

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
  G --> H["按反馈重生成部分页面"]
  H --> I["写限时汇报稿"]
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
outputs/<topic-slug>-images/
  slide-01-cover.png
  slide-02-contents.png
  ...
  slide-13-closing.png
  contact-sheet-13-slides.jpg
```

实际文件名可以根据你的主题和语言调整。

## 安装方式

### Codex Desktop / Codex CLI

把这个仓库克隆到你的 Codex skills 目录即可。

Windows PowerShell：

```powershell
git clone https://github.com/uuoov/ppt-image-share-builder.git "$env:USERPROFILE\.codex\skills\ppt-image-share-builder"
```

macOS / Linux：

```bash
git clone https://github.com/uuoov/ppt-image-share-builder.git ~/.codex/skills/ppt-image-share-builder
```

然后重启 Codex，让它重新加载 skill 元数据。

## 快速开始

显式调用这个 skill：

```text
Use $ppt-image-share-builder to turn my course topic, source files, and reference PPT style into slide image prompts, generated slide images, and a 10-minute presentation script.
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
7. 最后写一份 10 分钟汇报稿。
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

### 6. 生成图片并保存

一般先生成前 3 页确认风格，再继续生成后续页面。图片会按页码保存，便于插入 PPT。

### 7. 做总览图并检查

生成缩略图总览，重点检查：

- 页数是否正确
- 风格是否统一
- 中文是否明显错误
- 页码是否正确
- 是否有重复文件
- 是否出现用户要求删除的内容，例如不该出现的 `Q&A`

### 8. 写限时汇报稿

汇报稿不是简单念 PPT，而是补充：

- 页面之间的过渡
- PPT 上没有展开的案例
- 资料来源背后的逻辑
- 面向课堂的口语表达

## 仓库结构

```text
ppt-image-share-builder/
  SKILL.md
  agents/
    openai.yaml
  references/
    workflow-checklist.md
    prompt-patterns.md
    qa-checklist.md
```

## 设计原则

- **资料先行**：法律、日期、数据、案例要有来源依据。
- **风格跟随**：新生成的页面要尽量贴近用户给的参考 PPT。
- **小步确认**：先生成少量页面确认风格，再批量继续。
- **中文友好**：中文图片生成容易出错，尽量控制小字数量。
- **隐私安全**：不要把用户的教材原文、私人姓名、课程文件或未公开材料上传到公开仓库。

## 和其他高星 Skill 的区别

| 类型 | 高星项目常见优势 | 本 Skill 的定位 |
| --- | --- | --- |
| Skill 合集 | 数量多，容易被搜索和安装 | 单一工作流，聚焦课程汇报 PPT |
| 官方示例库 | 标准清楚，有官方背书 | 更偏实际课堂任务和 Codex 桌面端工作流 |
| 工程类 agent skill | 有命令、脚本、质量门禁 | 更偏资料整理、图片生成、讲稿生成 |
| PPT 生成 skill | 可能直接生成 `.pptx` | 更强调参考风格、image2 提示词、总览 QA 和汇报稿 |

## 后续路线

值得继续增强的方向：

- 增加一个脱敏 demo，展示输入资料、生成图片总览和最终讲稿。
- 增加自动生成 contact sheet 的脚本。
- 增加把图片自动插入 PPTX 的脚本。
- 发布 release zip，方便用户下载。
- 增加 README 顶部效果图。
- 增加演示视频或 GIF。
- 投稿到相关 awesome skill 列表。

## 如何获得更多 Star

如果你希望这个 skill 被更多人点赞，最重要的是让别人一眼看懂、马上能用、相信效果。

建议：

1. 做一个完整脱敏示例。
2. 在 README 顶部放一张总览图。
3. 加一个一键安装说明。
4. 发布 release。
5. 做中英文双语文档。
6. 分享到 Codex / Agent Skills / PPT 自动化相关社区。
7. 提交到高质量 awesome list。
8. 明确一句话定位：  
   **把零散课程资料变成有来源、有风格、有图片、有讲稿的课堂汇报。**

不建议买星、刷星或互星。长期看，真实案例和清晰文档更有用。

## License

MIT. See `LICENSE`.
