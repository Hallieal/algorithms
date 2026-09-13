from pathlib import Path
import re


def replace(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'Expected text not found in {path}: {old}')
    p.write_text(text.replace(old, new), encoding='utf-8')


def sub_once(path, pattern, repl):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    text, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f'Expected one regex match in {path}: {pattern}')
    p.write_text(text, encoding='utf-8')

# Russian practice index: Hard pages are now bilingual.
replace('sorting-problems-ru.html', 'href="problem-top-k-frequent.html"', 'href="problem-top-k-frequent-ru.html"')
replace('sorting-problems-ru.html', 'href="problem-merge-without-space.html"', 'href="problem-merge-without-space-ru.html"')
replace('sorting-problems-ru.html', 'href="problem-closest-pair.html"', 'href="problem-closest-pair-ru.html"')

for href in (
    'problem-top-k-frequent-ru.html',
    'problem-merge-without-space-ru.html',
    'problem-closest-pair-ru.html',
):
    sub_once(
        'sorting-problems-ru.html',
        rf'(<a class="problem-card hard" href="{re.escape(href)}".*?<span class="problem-open">)Открыть решение · EN →(</span>)',
        r'\1Открыть решение →\2',
    )

replace(
    'sorting-problems-ru.html',
    'Слить два отсортированных массива на месте, рассматривая их как одну виртуальную последовательность.',
    'Разделить значения между двумя массивами и восстановить порядок с O(1) дополнительной памятью.',
)
replace(
    'sorting-problems-ru.html',
    'Страницы Medium доступны на русском и английском; остальные решения пока остаются на английском.',
    'Страницы Medium и Hard доступны на русском и английском; решения Easy пока остаются на английском.',
)

# English card should describe the new algorithm rather than the old gap-method presentation.
replace(
    'sorting-problems.html',
    'Merge two sorted arrays in place by viewing them as one virtual sequence and shrinking a comparison gap.',
    'Separate the values between two sorted arrays, then restore order with O(1) auxiliary space.',
)
replace(
    'sorting-problems.html',
    '<span class="problem-tag">gap method</span>',
    '<span class="problem-tag">heapsort</span>',
)

# Russian Applications should enter the Russian Hard pages.
replace('sorting-applications-ru.html', 'href="problem-top-k-frequent.html"', 'href="problem-top-k-frequent-ru.html"')
replace('sorting-applications-ru.html', 'href="problem-merge-without-space.html"', 'href="problem-merge-without-space-ru.html"')

for href in ('problem-top-k-frequent-ru.html', 'problem-merge-without-space-ru.html'):
    sub_once(
        'sorting-applications-ru.html',
        rf'(<div class="application-practice">\s*<span class="application-practice-label">)Практика · EN(</span>\s*<a href="{re.escape(href)}">)',
        r'\1Практика\2',
    )

print('Hard practice links synchronized.')
