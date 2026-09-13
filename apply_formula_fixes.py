from pathlib import Path

FILES = [
    Path('sorting-merge.html'),
    Path('sorting-quick.html'),
    Path('sorting-merge-ru.html'),
    Path('sorting-quick-ru.html'),
]

OLD = 'Θ(loglinear)'
NEW = 'Θ(n log n)'

total = 0
missing = []
for path in FILES:
    if not path.exists():
        missing.append(str(path))
        continue
    text = path.read_text(encoding='utf-8')
    count = text.count(OLD)
    if count:
        path.write_text(text.replace(OLD, NEW), encoding='utf-8')
        total += count
        print(f'{path}: replaced {count} occurrence(s)')
    else:
        print(f'{path}: no {OLD!r} found (already fixed or different version)')

print(f'\nTotal replacements: {total}')
if missing:
    print('Missing files: ' + ', '.join(missing))
    raise SystemExit(2)
