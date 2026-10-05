"""Check migrated routes and every local link/asset in a Hugo production build."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
import json

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
required = ('index.html', 'products.html', 'tenets.html', 'history.html', 'subwiz.html',
            'books/index.html', 'favicon.svg', 'images/wiztools-logo.svg')
errors = [f'Missing migrated route: {p}' for p in required if not (root / p).is_file()]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value:
                self.urls.append(value)

for page in root.rglob('*.html'):
    parser = Links()
    parser.feed(page.read_text())
    for url in parser.urls:
        parsed = urlsplit(url)
        if parsed.netloc and parsed.netloc != 'www.wiztools.org':
            continue
        if parsed.scheme not in ('', 'https', 'http') or not parsed.path:
            continue
        path = unquote(parsed.path)
        target = root / path.lstrip('/') if path.startswith('/') else page.parent / path
        if not target.is_file() and not (target / 'index.html').is_file():
            errors.append(f'{page.relative_to(root)}: broken local URL {url}')

indexes = list(root.glob('en.search-data*.json'))
if not indexes:
    errors.append('Missing search index')
else:
    index = json.loads(indexes[0].read_text())
    if not index or '/products.html' not in index:
        errors.append('Search index does not contain migrated products')
for hidden in ('docs/index.html', 'blog/index.html'):
    if (root / hidden).exists():
        errors.append(f'Future draft section was published: {hidden}')

if errors:
    print('\n'.join(sorted(set(errors))))
    raise SystemExit(1)
print(f'PASS: {len(required)} required routes/assets and local links across {len(list(root.rglob("*.html")))} HTML pages')
