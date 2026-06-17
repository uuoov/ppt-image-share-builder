# Grill-Me Style Intake

Use this intake before planning, prompting image2, generating images, or building the PPTX. The goal is to ask enough up front that the user can get a useful one-pass result without knowing prompt engineering.

If the environment has a real `grill-me` or similar clarification skill/tool, use it. If not, run this built-in checklist.

## Required Before Work

Ask these in one compact message when they are missing and cannot be inferred safely:

```text
1. 主题和最终标题是什么？
2. 受众是谁？例如课程汇报、老师同学、企业培训、答辩。
3. 汇报时长或期望页数是多少？
4. 需要依据哪些资料文件、链接、教材章节或政策原文？
5. 参考 PPT 或期望风格是什么？可以给文件，也可以描述关键词。
6. 必须出现哪些关键词、案例、数据、岗位信息或结论？
7. 明确不要出现什么？例如 Q&A、虚假 logo、无意义 X/对勾、随机英文、过多装饰。
8. 最终要交付哪些文件？例如图片、contact sheet、PPTX、讲稿、README/demo。
```

Do not ask all eight again if the user already provided them. Confirm the missing items only.

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
- Proceed with stated assumptions for low-risk missing details: presenter name, date, exact page count, file naming, or whether to include a short agenda page.
- If the user asks for speed or says "直接做", ask at most one compact missing-requirements question, then proceed with assumptions.
- Keep the intake user-facing and plain. Avoid terms like "style lock", "prompt engineering", or "visual grammar" unless the user uses them.
- After intake, summarize the execution contract in 3-5 bullets, then start the one-pass workflow.

## Execution Contract Example

```text
我先按下面理解直接做：
- 主题：药品医疗器械飞行检查办法，10 分钟课程汇报
- 受众：医疗器械法规与工程伦理学课堂
- 资料：用户给的 PPT、教材原文、政策资料
- 风格：统一的现代监管/医疗器械视觉，不要 Q&A、随机英文、无意义标记
- 交付：逐页图片、总览图、PPTX、讲稿
```
