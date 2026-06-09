# PPT Image Share Builder

Turn a course topic, source files, and a reference PPT style into a complete image-based classroom presentation workflow:

- sourced slide outline
- per-slide image prompts
- generated slide images
- contact-sheet QA
- timed presentation script
- revision notes from user feedback

This is a Codex skill for students, teachers, researchers, and anyone who needs to make a polished lecture-style or report-style PPT from messy materials.

## Why This Skill Exists

Most AI deck workflows stop too early:

1. They summarize the source.
2. They generate a few pretty slides.
3. They leave the user to fix structure, visual consistency, citations, and the speaking script.

`ppt-image-share-builder` packages a fuller workflow:

```mermaid
flowchart LR
  A["Topic + source files"] --> B["Extract and verify source facts"]
  B --> C["Audit reference PPT style"]
  C --> D["Build narrative spine"]
  D --> E["Write image2 prompts"]
  E --> F["Generate slide images"]
  F --> G["Create contact sheet"]
  G --> H["Iterate selected slides"]
  H --> I["Write timed talk script"]
```

The skill is especially useful when the user has:

- a course topic
- a textbook excerpt or `.docx`
- pasted notes
- government/regulatory source material
- a sample PPT whose style should be followed
- a target speaking duration such as 8-10 minutes

## What It Produces

Typical output:

```text
<topic>_image2逐页大纲.md
<topic>_10分钟汇报稿.md
outputs/<topic-slug>-images/
  slide-01-cover.png
  slide-02-contents.png
  ...
  slide-13-closing.png
  contact-sheet-13-slides.jpg
```

The exact filenames can be adapted to the project language and topic.

## Install

### Codex Desktop / Codex CLI

Clone this repository directly into your Codex skills directory.

Windows PowerShell:

```powershell
git clone https://github.com/uuoov/ppt-image-share-builder.git "$env:USERPROFILE\.codex\skills\ppt-image-share-builder"
```

macOS / Linux:

```bash
git clone https://github.com/uuoov/ppt-image-share-builder.git ~/.codex/skills/ppt-image-share-builder
```

Restart Codex so it loads the new skill metadata.

### Development Install

If you are editing the skill locally, clone it anywhere and symlink or copy the folder into your Codex skills directory.

## Quick Start

Invoke the skill explicitly:

```text
Use $ppt-image-share-builder to turn my course topic, source files, and reference PPT style into slide image prompts, generated slide images, and a 10-minute presentation script.
```

A strong request usually includes:

```text
Topic: <your sharing topic>
Audience: <class / teacher / meeting>
Duration: <8-10 minutes>
Reference PPT: <path to sample deck>
Sources: <docx/pdf/txt/web links>
Required keywords: <terms that must appear>
Output: image prompts + slide images + script
```

## Example Prompt

```text
Use $ppt-image-share-builder.

I need a 10-minute classroom report about a regulation topic.
I have a reference PPT in the current folder and a textbook excerpt as a .docx file.
Please:
1. extract the source material,
2. audit the reference PPT style,
3. create a 12-14 page image2 outline,
4. generate the first 3 slide images for style confirmation,
5. continue after I approve,
6. make a contact sheet,
7. write the final talk script.
```

## Workflow Details

The skill follows these stages:

1. **Collect inputs**  
   Topic, audience, duration, slide count, reference PPT, source files, and must-use keywords.

2. **Extract and normalize sources**  
   Chinese `.docx`, `.txt`, `.csv`, and government-style documents are normalized before analysis. The skill warns against Windows PowerShell path-encoding pitfalls.

3. **Audit reference PPT style**  
   It extracts slide rhythm, title style, colors, fonts, page markers, chart/table style, and image language.

4. **Build the narrative spine**  
   It creates slide claims rather than just topic labels.

5. **Write image prompts**  
   It creates one unified visual prompt plus per-slide prompts with required text and composition.

6. **Generate and save slide images**  
   It generates one slide at a time or in small batches, then saves stable numbered files.

7. **QA with contact sheets**  
   It checks slide count, visible text, page numbers, duplicate variants, and style consistency.

8. **Write the timed script**  
   It writes a report script that adds spoken bridges and supporting cases instead of just reading the slides.

## Repository Layout

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

## Design Principles

- **Source-backed first**: facts, laws, dates, statistics, and cases should be tied to source notes.
- **Reference-style aware**: generated slides should match the user's existing PPT language.
- **Human-in-the-loop**: generate a few slides first, confirm the style, then continue.
- **Chinese text aware**: keep generated Chinese text short enough to inspect and fix.
- **Private by default**: do not publish user textbooks, generated course files, personal names, or classroom materials unless the user explicitly asks.

## How It Compares

This repository is a focused, single-purpose skill. High-star skill repositories tend to have broader distribution or stronger demo surfaces:

| Repository type | What they do well | Difference from this skill |
| --- | --- | --- |
| Curated skill lists | Many skills, easy discovery, install snippets | This repo is one focused workflow, not a collection |
| Official/example skill repos | Templates, specs, marketplace-style installation | This repo is practical and Codex-oriented, but not yet a marketplace package |
| Production agent-skill suites | Commands, quality gates, multi-agent workflows, docs, releases | This repo is narrower and tuned for presentation-image workflows |
| PPT-generation skills | Often assemble `.pptx` automatically and include runtime scripts | This repo emphasizes source extraction, style audit, image prompts, contact-sheet QA, and talk scripts |

## Roadmap

Useful next steps:

- Add a sanitized demo project with source notes, prompts, images, contact sheet, and script.
- Add helper scripts for contact-sheet generation and final-folder cleanup.
- Add an optional PPTX assembly helper that places generated images into slides.
- Add a release `.zip` for one-click manual installation.
- Add screenshots or an Open Graph cover image.
- Add a short demo video or animated GIF.
- Submit the skill to public skill directories or awesome lists after adding a demo.

## Tips For Getting More Stars

Stars usually come from clarity, usefulness, and proof. For this project, the highest-leverage steps are:

1. **Show a real sanitized example**  
   Add before/after materials, a contact sheet, and the final script.

2. **Make installation effortless**  
   Keep the clone command visible near the top. Add release downloads later.

3. **Make the outcome obvious in 10 seconds**  
   Put one screenshot/contact sheet near the top of the README.

4. **Target a clear niche**  
   "Turn course materials into sourced image-based PPT reports" is more memorable than "make PPTs."

5. **Publish where skill users look**  
   Share it with Codex/agent-skill communities and submit it to relevant awesome lists.

6. **Keep examples privacy-safe**  
   Do not use real student names, private course files, or unreleased classroom materials.

## License

MIT. See `LICENSE`.
