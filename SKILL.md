---
name: ppt-image-share-builder
description: Build image2-first classroom sharing decks from a topic, source files, reference PPT style, and iterative user feedback. Use when Codex needs to create image2-ready per-slide prompts, generate polished PPT page images, QA a contact sheet, assemble those images into a PPTX, and write a timed presentation script for a course report or lecture-style PPT.
---

# PPT Image Share Builder

Use this skill for image2-first presentation work:

```text
source files + reference PPT style
  -> sourced slide outline
  -> image2-ready per-slide prompts
  -> generated 16:9 slide images
  -> contact-sheet QA
  -> full-bleed PPTX assembly
  -> timed speaking script
```

Keep the workflow source-backed, style-aware, and human-reviewed. Helper scripts are for post-generation steps; they do not replace image2.

## Core Rules

- Treat generated slide images as the visual source of truth for the final PPTX.
- Extract and verify source facts before writing prompts. Use official or primary sources for recent rules, cases, data, or dates.
- Match the user's reference PPT style: layout rhythm, title system, color palette, page markers, diagram grammar, and information density.
- Generate a small batch first when the user needs style confirmation, especially for Chinese slides.
- Keep generated Chinese text short. Recommend adding exact long text manually in PPT if precision matters.
- Do not generate government seals, company logos, QR codes, or watermarks unless the user supplied verified assets and explicitly requests them.
- On Windows PowerShell 5.x, avoid Bash-style command chaining such as `&&`; run multi-step commands separately.
- For Chinese paths, do not put non-ASCII path literals inside here-strings piped to native programs. Pass paths as arguments or use `-LiteralPath`.

## Workflow

1. **Collect inputs**
   - Topic, exact title, audience, duration, slide count, language, reference PPT, source files, and required keywords.
   - Convert required keywords into slide-level claims, not just a list.

2. **Extract sources**
   - For Chinese `.doc`, `.docx`, `.txt`, `.csv`, or government-style documents, use a reliable UTF-8 extraction path.
   - If the current environment provides a document extraction helper, prefer it over ad hoc encoding guesses.

3. **Plan the deck**
   - Build a thesis and slide sequence before prompting image2.
   - For 8-12 minute classroom reports, usually use 10-14 slides.
   - Read `references/workflow-checklist.md` when planning a full deck.

4. **Write image2 prompts**
   - Create one unified visual prompt, then per-slide prompts.
   - Each slide prompt should include title, required text, visual structure, style constraints, and forbidden text.
   - Read `references/prompt-patterns.md` when drafting or revising prompts.

5. **Generate and save images**
   - Use image2 or the available raster image-generation tool.
   - Save final images with stable names such as `slide-01-cover.png`, `slide-02-agenda.png`, and so on.
   - Regenerate only affected slides when user feedback is local.

6. **QA with a contact sheet**
   - Build a contact sheet after each major batch:

     ```powershell
     python scripts\make_contact_sheet.py --input-dir outputs\<topic-slug>-images -o outputs\<topic-slug>-images\contact-sheet.jpg
     ```

   - Read `references/qa-checklist.md` before final delivery.

7. **Assemble PPTX**
   - After the final images are approved, insert them as full-bleed slides:

     ```powershell
     python scripts\images_to_pptx.py --input-dir outputs\<topic-slug>-images -o <topic>.pptx
     ```

   - Do not rebuild the visual design in native PPT shapes unless the user explicitly asks for editable slides.

8. **Write the talk script**
   - Write the script after slide content stabilizes.
   - Add spoken bridges, background logic, and selected examples that are not fully written on the slides.
   - Match the requested duration and final closing wording.

## Expected Outputs

- `<topic>_image2逐页大纲.md`
- `outputs/<topic-slug>-images/slide-XX-*.png`
- `outputs/<topic-slug>-images/contact-sheet-*.jpg`
- `<topic>.pptx`
- `<topic>_<duration>汇报稿.md`
