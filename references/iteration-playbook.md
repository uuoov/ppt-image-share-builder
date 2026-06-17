# Three-Pass Iteration Playbook

Use this playbook when building or revising a multi-page image2 PPT image set, especially when the user is not a prompt expert.

## Goal

Make the workflow feel simple to the user:

1. The first version should not be shallow.
2. Revision pages should not drift away from the approved style.
3. Final QA should remove meaningless visual elements before PPTX delivery.

## Pass 1: Content-Rich First Draft

The first batch should prove both content depth and visual direction. Do not generate pages that are only decorative.

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

For a first style sample, prefer 3 pages:

- Cover: proves visual tone.
- One dense content page: proves information handling.
- One diagram/case page: proves visual grammar.

If the user's topic is under-specified, infer a reasonable structure and state the assumption in the outline. Do not stop at a thin outline.

## Pass 2: Feedback Iteration With Style Lock

When the user gives feedback, translate it into an edit plan before generating again.

Create or update a style lock:

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

Every revision prompt must repeat the style lock and state only the local change:

```text
Keep the approved style lock exactly. Regenerate page <n> only.
Change: <specific user feedback>.
Do not change: palette, header, page marker, icon style, diagram grammar, and neighboring page rhythm.
Forbidden: random text, fake logos, stray X/check marks, unrelated icons, decorative charts without data meaning.
```

If two or more regenerated pages drift, stop generating and update the unified visual prompt before continuing.

## Pass 3: Meaningless Element Cleanup

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

Convert vague feedback into concrete actions:

| User says | Translate to |
| --- | --- |
| "太简单" | Add claims, examples, source-backed points, and richer diagram structure. |
| "不好看" | Regenerate style sample with stronger visual hierarchy, more polished background, and fewer filler cards. |
| "风格不统一" | Rebuild style lock and regenerate drifted pages with the same title, palette, icon, and layout grammar. |
| "有奇怪标记" | Run meaningless element cleanup; remove stray marks, random icons, fake labels, and decorative junk. |
| "不够傻瓜式" | Provide the user a short checklist of choices instead of asking them to write prompts. |

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
先做几页给我确认：
```

Then proceed with reasonable assumptions.
