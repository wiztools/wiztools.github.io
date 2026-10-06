# WizTools.org

A Hugo static site using Hextra v0.13.0, with dark mode by default and the hand-built hammer-T identity.

## Local development

Requires Hugo Extended 0.162.0 and Go 1.27 (the versions used for verification).

```sh
hugo server --disableFastRender
```

Open http://localhost:1313/. The first build downloads the pinned Hextra module. Search JavaScript is bundled locally, with its license under `assets/js/vendor/`.

```sh
hugo --gc --minify --panicOnWarning
python3 scripts/check_site.py public
```

Generated files are written to `public/` and excluded from Git.

## Content

### PDF carousels

`/atelier/` uses the original PDF in `static/pdfs/atelier.pdf` and pre-rendered
slides in `static/images/atelier/`. The reusable shortcode provides native
horizontal scrolling and snapping, buttons, keyboard navigation, and a counter.
No browser PDF library is required. To regenerate slides after replacing the PDF,
use Poppler (remove any obsolete slides if the new PDF has fewer pages):

```sh
pdftoppm -jpeg -jpegopt quality=90 -scale-to 1600 static/pdfs/atelier.pdf static/images/atelier/slide
```

Embed another presentation using its own directory of page images:

```text
{{< pdf-carousel title="Atelier" images="images/atelier" pdf="pdfs/atelier.pdf" >}}
```

The slide artwork is displayed as images; selectable text and PDF links are
available through the original PDF link.

- `content/products.md`: the catalogue of 37 tools, 8 libraries, and the hosted Web Tester.
- `content/books.md`: books and local cover images.
- `content/tenets.md`, `history.md`, and `subwiz.md`: migrated informational pages.
- `content/_index.md` and `layouts/_shortcodes/wiz-home.html`: homepage.
- `assets/css/custom.css`: homepage styling.
- `static/images/`: logo variants, hammer icon, and book covers.
- `data/projects.json`: machine-readable inventory captured during migration; the published catalogue is maintained in Markdown.

The original `/products.html`, `/tenets.html`, `/history.html`, and `/subwiz.html` URLs remain canonical. Directory-style alternatives redirect to them. `/index.html` remains the homepage output.

Historical catalogue and author links were retained; their external destinations may have changed since the old site was last updated. Atelier is featured on the homepage with links to its presentation, source code, and GitHub Releases. The PHP OOP book uses the legacy homepage's featured Amazon link (the old sidebar linked to a different edition).

## Future documentation and blog

Both sections have draft indexes and are absent from production navigation and search. Create content with:

```sh
hugo new content --kind docs docs/restclient/getting-started.md
hugo new content --kind blog blog/first-post.md
hugo server --buildDrafts --disableFastRender
```

When a section is ready, remove `draft: true` from its `_index.md` and the pages to publish. Add the matching entry under `menu.main` in `hugo.yaml`:

```yaml
- name: Documentation
  pageRef: /docs
  weight: 3
- name: Blog
  pageRef: /blog
  weight: 4
```

Documentation uses Hextra's sidebar, table of contents, and syntax highlighting. Blog articles use Hextra's blog layout. The existing Blogger site stays linked as the blog archive; its posts have not been imported.

## Deployment

`.github/workflows/pages.yaml` builds and checks pull requests, and deploys pushes to `master` or manual runs to GitHub Pages. Configure the repository's **Settings → Pages → Source** to **GitHub Actions** before deploying.

The production `baseURL` remains `https://www.wiztools.org/`. The currently published site is served through Amazon S3/CloudFront. This migration does not change DNS or existing hosting. For a GitHub Pages cutover, configure the custom domain and DNS as a separate release step; for a Pages preview domain, override `baseURL` appropriately before publishing. Alternatively, upload `public/` to the existing static hosting.

## Logo

SVGs contain editable vector paths, with no external fonts. PNG wordmarks have transparent backgrounds. See `docs/logo-and-theme.md` and regenerate SVGs with `python3 scripts/build_logo.py`.
