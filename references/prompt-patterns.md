# Prompt Patterns

## Unified Visual Prompt

Start every image plan with one reusable visual system prompt:

```text
16:9 horizontal PPT page, professional classroom report style, matching the provided reference PPT.
White and pale-blue background, deep navy title, main blue accents, restrained green for positive/compliance signals, red only for risk warnings.
Use clean line icons, medical/technical/academic visual language as appropriate.
Chinese text must be horizontal, clear, and correctly spelled.
No real government logo, company logo, seal, watermark, QR code, or random extra text.
```

Adapt the subject matter and palette to the reference deck.

## Per-Page Prompt Shape

```text
Use case: scientific-educational or productivity-visual
Asset type: 16:9 PPT page image, page <n>
Primary request: <what the page explains>
Style: <reference PPT style>
Header: <section number, page title, page number>
Main composition: <layout>
Text (verbatim): <short required text>
Constraints: <must avoid, accuracy requirements>
```

## Text Density Rule

For image generation with Chinese:

- Prefer titles, labels, and short callouts.
- Avoid long paragraphs.
- For tables, use fewer rows and compact labels.
- If exact wording matters, recommend adding final text manually in PPT after image generation.

## Closing Page Patterns

Formal closing:

```text
Large title: "感谢垂听"
Theme title: "<full presentation title>"
Topic: "<topic subtitle>"
Small line: "欢迎批评指正"
Presenter: "<name>"
Do not include Q&A unless the user explicitly asks.
```

Q&A closing:

```text
Large title: "感谢聆听"
Subtitle: "欢迎批评指正｜Q&A"
```

Use only the pattern requested by the user.

## Revision Prompts

When regenerating a page image:

- Preserve the prior visual system.
- State exactly what changed.
- Repeat text that must not appear, such as `Do not include "Q&A"`.
- Regenerate only the affected page image unless the style has drifted across the image set.
