---
name: ppt-image-share-builder
description: Build classroom sharing decks from a topic, source files, reference PPT style, and iterative user feedback. Use when Codex needs to create image-generation prompts, generate slide images, QA a contact sheet, and write a timed presentation script for a course report or lecture-style PPT.
---

# PPT Image Share Builder

Use this skill to reproduce the workflow of turning a course-sharing topic into:

- a sourced slide outline
- image-generation prompts for each PPT page
- generated slide images saved in the workspace
- a contact sheet for QA
- a timed oral presentation script
- iteration notes from user feedback

Keep the workflow source-backed and style-aware. Do not treat it as a generic image batch job.

## Workflow

1. **Collect Inputs**
   - Identify the topic, audience, target duration, expected slide count, language, and whether the result is a standalone deck or an appendix to an existing PPT.
   - Gather source files such as pasted text, `.docx`, `.pdf`, `.txt`, web links, official notices, and reference PPT files.
   - If the user provides keywords or “must cover” points, convert them into slide-level claims instead of just listing them.

2. **Extract And Normalize Sources**
   - For Chinese `.docx`, `.doc`, `.txt`, `.csv`, or government documents, prefer the user’s global extraction helper when available:

     ```powershell
     python C:\Users\m1342\.codex\tools\extract_text.py <file-or-folder> -o <output-folder>
     ```

   - On Windows PowerShell, do not place Chinese paths inside here-strings piped to Python. Pass paths via `sys.argv` or environment variables.
   - Use official or primary sources for recent laws, rules, standards, regulator notices, data, and case details. Browse when the fact could have changed.
   - Separate verified source facts from explanatory interpretation.

3. **Audit The Reference PPT**
   - Extract slide count, titles, text, fonts, theme colors, and layout rhythm from the reference PPT.
   - Render the PPT to images if possible and create a contact sheet.
   - Record style decisions: title system, page markers, dominant colors, icon style, table style, diagram grammar, footer/source handling, and visual density.
   - Preserve the reference deck’s visual language without copying unrelated content.

4. **Build The Narrative Spine**
   - Define the one-sentence thesis.
   - Create a slide list with: page role, claim title, evidence object, required text, visual structure, and speaking intent.
   - For 8-12 minute classroom reports, prefer 10-14 slides.
   - Include a closing page if the user expects a formal report deck.
   - Add case examples that are not already visible on the slides when they make the talk more credible.

5. **Create Image Prompts**
   - Write a single unified visual prompt first, then per-slide prompts.
   - Each slide prompt should include:
     - `页面标题`
     - `画面结构`
     - `必须出现的文字`
     - `image2 提示词`
   - Keep dense Chinese text short. For text-heavy slides, recommend using generated images as backgrounds and adding final text manually in PPT.
   - Never ask image generation to create official government logos, company logos, seals, QR codes, or watermarks unless the user provided verified assets and explicitly wants them.

6. **Generate Slide Images**
   - Use the built-in image generation tool by default for raster slide images.
   - Generate one slide at a time or in small batches, especially when Chinese text must be accurate.
   - Save project-bound images under a workspace folder such as:

     ```text
     outputs/<topic-slug>-images/
     ```

   - Use stable filenames:

     ```text
     slide-01-cover.png
     slide-02-contents.png
     ...
     contact-sheet-<n>-slides.jpg
     ```

7. **QA And Iterate**
   - Make a contact sheet after each major batch.
   - Inspect every full-size slide for:
     - wrong Chinese characters
     - missing or incorrect page numbers
     - Q&A text on non-Q&A closing pages
     - duplicated slide files
     - text overflow or unreadable small type
     - source facts that drifted from the outline
     - mismatched visual style
   - When user feedback changes content, update the outline and prompt file first, then regenerate only affected slides.
   - Remove duplicate generated variants from the final output folder, unless the user asks to keep alternatives.

8. **Write The Presentation Script**
   - Write a timed script after the slide content stabilizes.
   - Match the target duration. For a 10-minute report, use roughly:
     - cover and agenda: 40-60 seconds total
     - core concept/process: 3-4 minutes
     - cases/comparison: 3-4 minutes
     - career/relevance/summary: 2 minutes
   - Do not merely read slide text. Add spoken bridges, background logic, and selected cases not fully shown on the slides.
   - End with a concise closing line that matches the final slide wording.

## Output Files

Produce the following when requested:

- `<topic>_image2逐页大纲.md`
- `outputs/<topic-slug>-images/slide-XX-*.png`
- `outputs/<topic-slug>-images/contact-sheet-<n>-slides.jpg`
- `<topic>_10分钟汇报稿.md` or another duration-specific script

## Quality Bar

- The slide sequence should have a clear learning arc, not just decorative pages.
- The generated images should visually match the user’s reference PPT.
- Official claims, dates, statistics, and cases must be source-backed.
- The final folder should contain only the formal slide images and useful contact sheet, not duplicate variants.
- The script should sound like a classroom report, not a legal memo or copied textbook.

## References

- Read `references/workflow-checklist.md` when planning or auditing a full workflow.
- Read `references/prompt-patterns.md` when drafting image prompts or revising image-generation instructions.
- Read `references/qa-checklist.md` before final delivery.
