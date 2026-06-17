# Grill-Me Style Intake

Use this intake before planning, prompting image2, generating images, or building the PPTX. The goal is to ask enough up front that the user can get a useful one-pass result without knowing prompt engineering.

If the environment has a real `grill-me` or similar clarification skill/tool, use it. If not, run this bounded built-in version.

## Architecture

Run intake as a bounded decision tree, not a long generic questionnaire:

1. Inspect what the user already gave: messages, attached files, source paths, reference PPTs, existing outline files, and prior feedback.
2. Mark each essential branch as `[OPEN]` or `[RESOLVED]`.
3. Ask only about branches that are still `[OPEN]` and cannot be inferred safely.
4. Ask 1-3 questions per batch. If `request_user_input` is available, use it with the recommended answer first; otherwise ask concise chat questions.
5. After each answer, commit the decision explicitly and close the branch.
6. Stop asking when the essential branches are resolved or when low-risk assumptions are enough to proceed.

This skill is not an unbounded interrogation mode. It should protect one-pass delivery, not delay it.

## Essential Branches

Resolve these before work when they are missing and cannot be inferred safely:

```text
[OPEN] 主题和最终标题
[OPEN] 受众和使用场景：课程汇报、老师同学、企业培训、答辩等
[OPEN] 汇报时长或期望页数
[OPEN] 资料范围：文件、链接、教材章节、政策原文、案例来源
[OPEN] 参考 PPT 或期望风格
[OPEN] 必须出现的关键词、案例、数据、岗位信息或结论
[OPEN] 明确不要出现的内容：Q&A、虚假 logo、无意义 X/对勾、随机英文、过多装饰等
[OPEN] 最终交付物：图片、contact sheet、PPTX、讲稿、README/demo 等
```

Do not ask all eight again if the user already provided them. Confirm the missing `[OPEN]` branches only.

## Question Batch Pattern

Prefer small batches with defaults:

```text
我先把能从资料里确定的部分关掉了，还差 2 个关键分支：
1. 汇报时长按 10 分钟处理可以吗？默认我会做 12-14 页。
2. 结尾页是否固定写“感谢垂听”？默认删除 Q&A。
```

If the user asks for speed or says "直接做", ask at most one compact missing-requirements batch, then proceed with recorded assumptions.

## Decision Log Before Work

Before moving into planning, summarize the intake result:

```text
开工决策：
- [RESOLVED] 主题：药品医疗器械飞行检查办法
- [RESOLVED] 受众：医疗器械法规与工程伦理学课堂
- [RESOLVED] 时长：10 分钟，约 12-14 页
- [RESOLVED] 风格：统一的现代监管/医疗器械视觉
- [ASSUMED] 交付：页面图片、总览图、PPTX、讲稿

开放风险：
- 长段政策原文不直接放进图片，必要时本地叠加精确文字。

信心：MEDIUM/HIGH
```

## Optional Defaults

Use these defaults unless the user specifies otherwise:

- Language: match the user's language.
- Delivery mode: one-pass full version.
- Aspect ratio: 16:9.
- Output: page images, contact sheet, full-bleed PPTX, and timed speaking script when the user is making a report.
- Verification: run contact-sheet QA and regenerate failed pages only.
- Text style: short Chinese labels in images; exact long text can be composed locally before export.

## Clarification Rules

- Ask before work when missing information would likely cause a wrong deck: topic, audience, duration/page count, source scope, reference style, required/forbidden content, or output format.
- Do not ask if the answer can be found by inspecting provided files or the current workspace.
- Proceed with stated assumptions for low-risk missing details: presenter name, date, exact page count, file naming, or whether to include a short agenda page.
- Keep the intake user-facing and plain. Avoid terms like "style lock", "prompt engineering", or "visual grammar" unless the user uses them.
- Do not keep grilling after essential branches are resolved. Start the one-pass workflow.
- After intake, summarize the execution contract, open risks, and confidence level, then start the one-pass workflow.

## Execution Contract Example

```text
我先按下面理解直接做：
- 主题：药品医疗器械飞行检查办法，10 分钟课程汇报
- 受众：医疗器械法规与工程伦理学课堂
- 资料：用户给的 PPT、教材原文、政策资料
- 风格：统一的现代监管/医疗器械视觉，不要 Q&A、随机英文、无意义标记
- 交付：逐页图片、总览图、PPTX、讲稿
```
