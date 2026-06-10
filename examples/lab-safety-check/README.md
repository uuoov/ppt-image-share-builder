# Demo: Campus Lab Safety Risk Inspection

This is a privacy-safe simulated run that shows the intended handoff shape for `ppt-image-share-builder`.

The topic, sources, PPT page images, and script are synthetic. They do not contain private classroom materials, real student names, campus names, logos, or unpublished files.

In a real workflow, the PPT page images should be generated with image2 from the per-page prompts. The placeholder images here exist so the public repository can demonstrate the full chain:

```text
input notes -> image2 outline -> PPT page images -> contact sheet -> PPTX wrapper -> talk script
```

## Files

- `input-notes.md`: synthetic source notes
- `image2-outline.md`: sample per-page image2 prompt plan
- `10-minute-script.md`: sample timed talk script
- `images/`: placeholder PPT page images standing in for image2 outputs
- `contact-sheet-demo.jpg`: overview of the generated slides

## Preview

![Demo contact sheet](contact-sheet-demo.jpg)
