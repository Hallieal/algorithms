from pathlib import Path
import os
import re
import shutil

ROOT = Path('.')


def posix(path: Path) -> str:
    return path.as_posix()


def exists(path: str) -> bool:
    return (ROOT / path).exists()


# Build a complete old -> new path map before moving anything.
moves = {}

# Main Sorting pages.
if exists('sorting.html'):
    moves['sorting.html'] = 'sorting/index.html'
if exists('sorting-ru.html'):
    moves['sorting-ru.html'] = 'sorting/index-ru.html'
if exists('sorting-problems.html'):
    moves['sorting-problems.html'] = 'sorting/problems/index.html'
if exists('sorting-problems-ru.html'):
    moves['sorting-problems-ru.html'] = 'sorting/problems/index-ru.html'

# All problem pages.
for p in ROOT.glob('problem-*.html'):
    moves[p.name] = f'sorting/problems/{p.name.removeprefix("problem-")}'

# All other Sorting theory/placeholder pages.
for p in ROOT.glob('sorting-*.html'):
    if p.name in moves:
        continue
    moves[p.name] = f'sorting/{p.name.removeprefix("sorting-")}'

# Sorting-specific CSS.
for p in ROOT.glob('sorting-*.css'):
    moves[p.name] = f'sorting/styles/{p.name.removeprefix("sorting-")}'

# Sorting-specific SVG/PNG artwork used inside the chapter.
for pattern in ('sorting-*.svg', 'sorting-*.png'):
    for p in ROOT.glob(pattern):
        moves[p.name] = f'sorting/assets/{p.name}'

# Practice-specific assets.
for name in ('problems.css', 'hard-problems.css', 'problems.js'):
    if exists(name):
        moves[name] = f'sorting/problems/assets/{name}'

# Global shared assets.
if exists('styles.css'):
    moves['styles.css'] = 'assets/css/styles.css'
for name in ('language-switch.js', 'lecture-core.js'):
    if exists(name):
        moves[name] = f'assets/js/{name}'

# app.js is obsolete and explicitly says the current pages do not depend on it.
if exists('app.js'):
    (ROOT / 'app.js').unlink()

for p in list(ROOT.iterdir()):
    if not p.is_file():
        continue
    name = p.name
    if (
        name in {'logo.png', 'homepage-logo.png', 'logo-source-muted.png', 'apple-touch-icon.png'}
        or name.startswith('favicon')
        or name.startswith('topic-')
    ):
        moves[name] = f'assets/images/{name}'

# Save inverse map for rewriting content after git mv.
inverse = {new: old for old, new in moves.items()}

# Perform filesystem moves. git will recognize these as renames in the final commit.
for old, new in sorted(moves.items(), key=lambda item: item[0].count('/'), reverse=True):
    old_path = ROOT / old
    if not old_path.exists():
        continue
    new_path = ROOT / new
    new_path.parent.mkdir(parents=True, exist_ok=True)
    if new_path.exists():
        raise RuntimeError(f'Target already exists: {new}')
    shutil.move(str(old_path), str(new_path))

# Remove obsolete one-time translation artifacts from previous passes.
for name in (
    '.translate_problems_payload.py',
    '.translation_payload_1.txt',
    '.github/workflows/translate-practice.yml',
):
    p = ROOT / name
    if p.exists():
        p.unlink()


EXTERNAL_PREFIXES = (
    'http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:', '//', '#'
)


def split_suffix(value: str):
    m = re.match(r'^([^?#]*)(.*)$', value)
    return m.group(1), m.group(2)


def resolve_old(source_old: str, ref: str) -> str:
    return posix(Path(os.path.normpath(os.path.join(os.path.dirname(source_old), ref))))


def clean_relative(source_new: str, target_new: str) -> str:
    source_dir = os.path.dirname(source_new) or '.'
    # Prefer clean directory URLs for English index pages.
    if os.path.basename(target_new) == 'index.html':
        target_dir = os.path.dirname(target_new) or '.'
        rel_dir = os.path.relpath(target_dir, source_dir).replace(os.sep, '/')
        if rel_dir == '.':
            return './'
        return rel_dir.rstrip('/') + '/'
    return os.path.relpath(target_new, source_dir).replace(os.sep, '/')


def rewrite_url(value: str, source_old: str, source_new: str) -> str:
    value = value.strip()
    if not value or value.startswith(EXTERNAL_PREFIXES) or value.startswith('/'):
        return value
    path_part, suffix = split_suffix(value)
    if not path_part:
        return value
    old_target = resolve_old(source_old, path_part)
    new_target = moves.get(old_target, old_target)
    # Only rewrite references that point to a tracked local path or one of our moved paths.
    if not (ROOT / new_target).exists() and old_target not in moves:
        return value
    return clean_relative(source_new, new_target) + suffix


attr_re = re.compile(r'(?P<prefix>\b(?:href|src)\s*=\s*)(?P<quote>["\'])(?P<url>.*?)(?P=quote)', re.I)
css_url_re = re.compile(r'url\(\s*(?P<quote>["\']?)(?P<url>[^)"\']+)(?P=quote)\s*\)', re.I)

# Rewrite every HTML file using its pre-migration location as the reference base.
for path in ROOT.rglob('*.html'):
    new_rel = posix(path.relative_to(ROOT))
    old_rel = inverse.get(new_rel, new_rel)
    text = path.read_text(encoding='utf-8')

    def attr_sub(match):
        url = match.group('url')
        new_url = rewrite_url(url, old_rel, new_rel)
        return f"{match.group('prefix')}{match.group('quote')}{new_url}{match.group('quote')}"

    text = attr_re.sub(attr_sub, text)
    path.write_text(text, encoding='utf-8', newline='\n')

# Rewrite local url(...) references in CSS if any.
for path in ROOT.rglob('*.css'):
    new_rel = posix(path.relative_to(ROOT))
    old_rel = inverse.get(new_rel, new_rel)
    text = path.read_text(encoding='utf-8')

    def css_sub(match):
        url = match.group('url').strip()
        new_url = rewrite_url(url, old_rel, new_rel)
        quote = match.group('quote') or ''
        return f'url({quote}{new_url}{quote})'

    text = css_url_re.sub(css_sub, text)
    path.write_text(text, encoding='utf-8', newline='\n')

# Muted branding: preserve the original PNGs, change only presentation.
styles = ROOT / 'assets/css/styles.css'
css = styles.read_text(encoding='utf-8')
marker = '/* ---------- Muted brand artwork ---------- */'
if marker not in css:
    css += '''\n\n/* ---------- Muted brand artwork ---------- */\n.home-title-logo {\n  filter: saturate(.62) contrast(.93) brightness(.99);\n  opacity: .94;\n}\n\n.brand-mark-image {\n  filter: saturate(.70) contrast(.95) brightness(.99);\n  opacity: .95;\n}\n'''
styles.write_text(css, encoding='utf-8', newline='\n')

# Replace the old version-note README with a structural README.
readme = '''# Allan's Handbook of Algorithms (AHA)\n\nBilingual algorithm handbook published with GitHub Pages.\n\n## Repository structure\n\n```text\n/\n├── index.html\n├── index-ru.html\n├── assets/\n│   ├── css/\n│   ├── js/\n│   └── images/\n└── sorting/\n    ├── index.html\n    ├── index-ru.html\n    ├── *.html                 # theory pages\n    ├── styles/                # page-specific theory CSS\n    ├── assets/                # Sorting chapter artwork\n    └── problems/\n        ├── index.html\n        ├── index-ru.html\n        ├── *.html             # practice problems\n        └── assets/            # practice CSS / JS\n```\n\nThe same chapter structure can be reused for future topics such as graphs, dynamic programming, and binary search.\n\nLive site: https://hallieal.github.io/algorithms/\n'''
(ROOT / 'README.md').write_text(readme, encoding='utf-8', newline='\n')


# ---------------- Validation ----------------

def local_target_exists(source: Path, value: str) -> bool:
    value = value.strip()
    if not value or value.startswith(EXTERNAL_PREFIXES) or value.startswith('/'):
        return True
    path_part, _ = split_suffix(value)
    if not path_part:
        return True
    target = (source.parent / path_part).resolve()
    root_resolved = ROOT.resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError:
        return False
    if value.split('?', 1)[0].split('#', 1)[0].endswith('/'):
        return (target / 'index.html').exists()
    return target.exists()

broken = []
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    for match in attr_re.finditer(text):
        value = match.group('url')
        if not local_target_exists(path, value):
            broken.append((posix(path.relative_to(ROOT)), value))

if broken:
    preview = '\n'.join(f'{p}: {u}' for p, u in broken[:40])
    raise RuntimeError(f'Broken local links after migration:\n{preview}')

# Expected structure.
required = [
    'sorting/index.html',
    'sorting/index-ru.html',
    'sorting/introduction.html',
    'sorting/applications.html',
    'sorting/selection-insertion.html',
    'sorting/bubble.html',
    'sorting/merge.html',
    'sorting/quick.html',
    'sorting/problems/index.html',
    'sorting/problems/index-ru.html',
    'sorting/problems/k-smallest.html',
    'sorting/problems/k-smallest-ru.html',
    'sorting/problems/closest-pair.html',
    'sorting/problems/closest-pair-ru.html',
    'sorting/problems/assets/problems.css',
    'sorting/problems/assets/hard-problems.css',
    'sorting/problems/assets/problems.js',
    'assets/css/styles.css',
    'assets/js/language-switch.js',
    'assets/js/lecture-core.js',
    'assets/images/logo.png',
    'assets/images/homepage-logo.png',
    'assets/images/topic-sorting.png',
]
for name in required:
    if not (ROOT / name).exists():
        raise RuntimeError(f'Missing expected migrated path: {name}')

# The repository root should no longer contain flat Sorting/problem HTML pages.
flat = [p.name for p in ROOT.glob('sorting*.html')] + [p.name for p in ROOT.glob('problem-*.html')]
if flat:
    raise RuntimeError('Flat chapter pages remain at repository root: ' + ', '.join(flat))

print(f'Migrated {len(moves)} files.')
print('All HTML local links resolve successfully.')
print('Repository structure validated.')
