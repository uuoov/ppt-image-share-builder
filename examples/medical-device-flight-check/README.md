# Demo: Medical Device Flight Check

This is a real end-to-end demo run for `ppt-image-share-builder`.

The topic is a Chinese classroom report on the regulatory logic of medical-device unannounced inspections. The run used public regulatory cases plus a desensitized classroom source extract, generated full 16:9 page candidates with image2, selected the strongest pages through contact-sheet QA, then wrapped the final image set in PPTX.

```text
source extract + public cases
  -> image2-ready outline
  -> generated 16:9 PPT page candidates
  -> selected final PPT page images
  -> contact sheet QA
  -> PPTX wrapper
  -> 10-minute talk script
```

## Files

- `image2-outline.md`: page-by-page prompt and source plan
- `10-minute-script.md`: timed Chinese presentation script
- `images/`: final selected image2 PPT page images
- `contact-sheet-demo.jpg`: overview for deck-level QA
- `demo-deck.pptx`: full-bleed PPTX wrapper around the final images

## Preview

![Demo contact sheet](contact-sheet-demo.jpg)
