# WizTools visual identity

The selected Hand-built concept has been redrawn as vector paths. It is a refinement of option 3, rather than a pixel-exact trace of the generated preview. Individual letter angles and the angled amber hammer T retain the work-in-progress personality.

## Assets

- `static/images/wiztools-logo.svg`: warm white lettering for dark backgrounds.
- `static/images/wiztools-logo.png`: transparent 2040 × 525 export.
- `static/images/wiztools-logo-light.svg` and `.png`: charcoal lettering for light backgrounds.
- `static/images/wiztools-icon.svg` and `.png`: standalone hammer T; PNG is 256 × 256.
- `static/images/wiztools-logo-preview.png`: dark-background preview.

The SVGs contain paths, not font references or embedded bitmaps. Keep their aspect ratio. The descriptive title supplies an accessible label when used inline; use `alt="WizTools"` when embedded as an image.

Regenerate SVGs with `python3 scripts/build_logo.py`. PNG exports use ImageMagick, for example:

```sh
magick -background none static/images/wiztools-logo.svg -resize 2040x525 PNG32:static/images/wiztools-logo.png
```

## Hugo theme recommendation

Use Hextra for the site migration. Its documentation and blog layouts, sidebar navigation, table of contents, dark mode, and built-in search support the planned expansion.

Official documentation: https://imfing.github.io/hextra/docs/

Plan separate `content/projects/`, `content/docs/`, and `content/blog/` sections. Keep future documentation and blog sections out of the navigation until content is ready. Configure dark mode as the default and use the matching logo variants for theme switching. Preserve existing HTML URLs or generate aliases during content migration.

The site now uses Hextra v0.13.0 with dark mode by default. Migrated pages retain their legacy URLs; documentation and blog indexes remain drafts until their content is ready. See README.md for preview, authoring, and deployment instructions.
