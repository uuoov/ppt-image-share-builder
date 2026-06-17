# One-Pass Delivery Playbook

Use this playbook when building or revising a multi-page image2 PPT image set, especially when the user is not a prompt expert.

## Goal

Make the workflow feel simple to the user by delivering a complete first version whenever possible.

Before the workflow starts, run the bounded grill-me style intake in `references/intake-grillme.md`. The intake should inspect provided materials, close essential decision branches, collect missing requirements in small batches, then let generation proceed in one pass by default.

The user should not need to understand prompt engineering or approve multiple rounds. Codex should run the quality gates internally:

1. Content-rich gate: the first delivered version must not be shallow.
2. Style-lock gate: pages should share one visual system from the start.
3. Cleanup gate: meaningless visual elements should be removed before PPTX delivery.

Only stop for user confirmation when:

- The source material or target topic is genuinely ambiguous.
- The user explicitly asks to approve the first pages before continuing.
- The visual generator repeatedly fails or produces unusable pages.
- A high-stakes factual claim cannot be verified.

## Gate 1: Content-Rich First Version

The first delivered version should prove both content depth and visual direction. Do not generate pages that are only decorative.

Minimum standard for each content page:

- A claim-style title, not just a topic label.
- 2-4 concrete points from the source material.
- At least one meaningful visual structure:
  - process
  - timeline
  - matrix
  - comparison table
  - case card
  - risk map
  - lifecycle loop
- A clear page role in the report arc.
- No filler panels, fake charts, or purely decorative icons.

For the full first version, include enough page variety to feel complete:

- Cover: proves visual tone.
- Agenda or structure page.
- Definition/background page.
- Process/framework page.
- Case/example page.
- Comparison/trend/application page when relevant.
- Summary and formal closing page.

If the user's topic is under-specified, infer a reasonable structure and state the assumption in the outline. Do not stop at a thin outline.

## Gate 2: Style Lock Before Generation

Create the style lock before generating the full image set:

```text
Style lock:
- Canvas: 16:9 PPT page image
- Palette: <dominant colors and accent rules>
- Background: <image/texture/gradient/cleanroom/etc.>
- Title system: <position, size, section marker, page number>
- Layout grammar: <cards/timeline/table/process/matrix rules>
- Icon style: <line/filled/3D/medical/academic>
- Text density: <short labels / compact table / no paragraphs>
- Forbidden elements: <Q&A, random English, fake logos, meaningless X marks, etc.>
```

Every page prompt must repeat the style lock. This prevents style drift without asking the user to supervise every page.

When the user gives feedback after delivery, translate it into an edit plan and keep the same style lock:

```text
Keep the established style lock exactly. Regenerate page <n> only.
Change: <specific user feedback>.
Do not change: palette, header, page marker, icon style, diagram grammar, and neighboring page rhythm.
Forbidden: random text, fake logos, stray X/check marks, unrelated icons, decorative charts without data meaning.
```

If two or more regenerated pages drift, stop generating and update the unified visual prompt before continuing.

## Gate 3: Meaningless Element Cleanup

Before final PPTX wrapping, inspect the contact sheet and individual problem pages.

Remove or regenerate pages with:

- Stray `X`, `?`, check marks, warning labels, arrows, badges, or labels that do not encode real meaning.
- Decorative charts that do not represent any source-backed trend, statistic, process, or comparison.
- Unrelated icons, objects, buildings, people, tools, seals, logos, QR codes, or watermarks.
- Random English words, pseudo-Chinese, garbled dates, or invented labels.
- Repeated page markers, inconsistent section numbers, or mismatched titles.
- Background objects that distract from the topic or imply false evidence.
- Any unrequested `Q&A` on a formal closing page.

For each suspect element, decide:

- **Keep** if it supports a source-backed claim or page role.
- **Regenerate** if it is baked into the image and visually distracting.
- **Document** if it is minor and the user prefers speed over another generation.

## User-Friendly Feedback Translation

If the user gives feedback after the first complete delivery, convert vague feedback into concrete actions:

| User says | Translate to |
| --- | --- |
| "太简单" | Add claims, examples, source-backed points, and richer diagram structure. |
| "不好看" | Improve the unified visual prompt, then regenerate failed or weak pages with stronger hierarchy, polished background, and fewer filler cards. |
| "风格不统一" | Rebuild style lock and regenerate drifted pages with the same title, palette, icon, and layout grammar. |
| "有奇怪标记" | Run meaningless element cleanup; remove stray marks, random icons, fake labels, and decorative junk. |
| "不够傻瓜式" | Reduce user decisions; deliver a complete version with assumptions and only ask for blocked information. |

## Simple User Prompt Template

When the user is unsure what to provide, ask for this compact input:

```text
主题：
受众：
汇报时长：
资料文件/链接：
参考 PPT 或喜欢的风格：
必须出现的关键词：
不要出现的内容：
是否需要先确认少量页面（可选，默认不需要）：
```

The final line is optional. If omitted, proceed with the full one-pass delivery by default.
