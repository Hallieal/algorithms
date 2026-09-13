from pathlib import Path
import re

ROOT = Path('.')
SHARED = '<script src="lecture-interactions.js"></script>'
changed = []

for path in sorted(ROOT.glob('sorting-*.html')):
    text = path.read_text(encoding='utf-8')
    original = text

    def refactor_script(match):
        body = match.group(1)
        if 'button[data-reveal]' not in body or 'sidebarLinks' not in body or 'updateProgress' not in body:
            return match.group(0)

        reveal_pos = body.find('button[data-reveal]')
        event_start = body.rfind('document.addEventListener', 0, reveal_pos)
        close_pos = body.rfind('})();')
        if event_start < 0 or close_pos < event_start:
            raise RuntimeError(f'Could not isolate common lecture JS in {path.name}')

        # Include a nearby section comment when there is one, but never consume
        # algorithm-specific code just because an older comment exists farther up.
        comment_start = body.rfind('/*', 0, event_start)
        start = comment_start if comment_start >= 0 and event_start - comment_start < 500 else event_start

        kept = body[:start].rstrip() + '\n\n})();\n'
        return '<script>\n' + kept + '</script>'

    text = re.sub(r'<script>\s*(.*?)\s*</script>', refactor_script, text, flags=re.S)

    if SHARED not in text and 'reading-progress' in text:
        if '<script src="language-switch.js"></script>' in text:
            text = text.replace('<script src="language-switch.js"></script>', SHARED + '\n<script src="language-switch.js"></script>', 1)
        else:
            text = text.replace('</body>', SHARED + '\n</body>', 1)

    if path.name == 'sorting-quick.html':
        text = re.sub(
            r'<div class="next-part">\s*<h3>Next section: Counting Sort</h3>.*?<a class="next-part-link" href="sorting-counting\.html">Counting Sort →</a>\s*</div>',
            '<div class="next-part">\n<h3>Advanced topics are planned next</h3>\n<p>Counting Sort and the remaining advanced sections are part of the roadmap and will be published later.</p>\n<a class="next-part-link" href="sorting.html">Return to the Sorting overview →</a>\n</div>',
            text,
            count=1,
            flags=re.S,
        )
    elif path.name == 'sorting-quick-ru.html':
        text = re.sub(
            r'<div class="next-part">\s*<h3>Следующий раздел:.*?</h3>.*?<a class="next-part-link" href="sorting-counting-ru\.html">.*?</a>\s*</div>',
            '<div class="next-part">\n<h3>Дальше — запланированные продвинутые темы</h3>\n<p>Сортировка подсчётом и остальные продвинутые разделы входят в план развития и будут опубликованы позже.</p>\n<a class="next-part-link" href="sorting-ru.html">Вернуться к списку тем →</a>\n</div>',
            text,
            count=1,
            flags=re.S,
        )

    if text != original:
        path.write_text(text, encoding='utf-8', newline='\n')
        changed.append(path.name)

# Validation
for path in sorted(ROOT.glob('sorting-*.html')):
    text = path.read_text(encoding='utf-8')
    if SHARED in text:
        assert 'const sidebarLinks' not in text, path.name
        assert 'function updateProgress()' not in text, path.name
        # The inline script may still contain algorithm-specific click handlers,
        # but reveal-button handling must now be centralized.
        inline_scripts = re.findall(r'<script>\s*(.*?)\s*</script>', text, flags=re.S)
        assert not any('button[data-reveal]' in s for s in inline_scripts), path.name

quick = (ROOT / 'sorting-quick.html').read_text(encoding='utf-8')
quick_ru = (ROOT / 'sorting-quick-ru.html').read_text(encoding='utf-8')
assert 'href="sorting-counting.html"' not in quick
assert 'href="sorting-counting-ru.html"' not in quick_ru
assert 'Return to the Sorting overview' in quick
assert 'Вернуться к списку тем' in quick_ru

print('Updated:', ', '.join(changed) if changed else 'none')
